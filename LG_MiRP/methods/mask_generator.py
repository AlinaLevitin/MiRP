"""
Author: Alina Levitin
Date: 02/07/24
Updated: 28/07/24

Method to generate masks volume .mrc file in the form of a wedge or a cylindrical cutout
"""
import os
import numpy as np
import mrcfile
from Bio.PDB import PDBParser
from Bio.PDB.Structure import Structure

from ..methods_base.method_base import MethodBase, print_done_decorator
from ..methods_base.particles_starfile import ParticlesStarfile


class MaskGenerator(MethodBase):
    """
    Inherits from MethodBase class located in method_base.py
    """

    def __init__(self,
                 input_star_file,
                 microtubule_volume,
                 microtubule_mask,
                 fit_tubulin_pdb,
                 pf_number,
                 helical_twist,
                 helical_rise,
                 output_path
                 ):
        """
        Using the pixel_size from optics data block from the input_star_file, your microtubule+kinesin volume and the
        mask used during high resolution reconstruction and a pdb file where a tubulin structure was fit to the
        microtubule volume to generate a series of masks in the shape of wedges or cylindrical cutouts according to the
        protofilament number (pf_number), helical_twist and a helical_rise at a selected output_path.
        """

        particles_star_file_data = ParticlesStarfile(input_star_file.get())
        self.particles_dataframe = particles_star_file_data.particles_dataframe
        self.data_optics_dataframe = particles_star_file_data.particles_dataframe
        self.pixel_size = particles_star_file_data.pixel_size
        self.microtubule_volume = microtubule_volume.get()
        self.microtubule_mask = microtubule_mask.get()
        self.fit_tubulin_pdb = fit_tubulin_pdb.get()
        self.pf_number = int(pf_number.get())
        self.helical_twist = int(helical_twist.get())
        self.helical_rise = int(helical_rise.get())
        self.output_path = output_path.get()

    @print_done_decorator
    def generate_cylindrical_cutout_mask(self):
        """
        Generates cylindrical cutout masks for microtubule data.
        """

        # Parse the PDB file to get the tubulin structure
        parser = PDBParser(QUIET=True)
        structure: Structure = parser.get_structure('tubulin', self.fit_tubulin_pdb)

        # Calculate the center of gravity for the structure
        com = self.calc_geometric_center(structure)

        # Load microtubule volume and mask
        vol = mrcfile.mmap(self.microtubule_volume, 'r', permissive=True)
        mask = mrcfile.mmap(self.microtubule_mask, 'r', permissive=True)

        # Apply the mask to the volume data
        vol_data = vol.data * mask.data
        voxel_size = vol.voxel_size
        header = vol.header
        vol_dim = np.asarray(vol_data.shape)

        # Generate radial matrix for cylindrical coordinate transformation
        size = vol_dim[0] // 2
        x, y = np.meshgrid(np.arange(-size + 1, size + 1), np.arange(-size + 1, size + 1))
        radmatrix = np.remainder(np.arctan2(x, y) + 2 * np.pi, 2 * np.pi) - 2 * np.pi
        zline = np.arange(-size + 1, size + 1)

        # Create a cosine mask filter for edge smoothing
        edge_resolution = 20
        edge_width = self.pixel_size * np.ceil(edge_resolution / (2 * self.pixel_size))
        cosmask_filter = np.fft.fftshift(self.spherical_cosmask(vol_dim, 0, edge_width / self.pixel_size))
        cosmask_filter_fft = np.fft.fftn(cosmask_filter) / np.sum(cosmask_filter)

        # Prepare the output directory for storing cutouts
        output_directory = os.path.join(self.output_path, "pf_cylindrical_cutouts")
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        else:
            self.delete_folder_contents(output_directory)

        # Iterate over the number of protofilaments to generate cutouts
        for pf in range(1, self.pf_number + 1):
            # Calculate initial angles and positions
            theta0 = np.arctan2(com[0], com[1]) + np.deg2rad(pf * (360 / self.pf_number))
            z0 = (com[2] + self.helical_rise * self.pf_number) / self.pixel_size
            zsubunits = (zline - z0) * self.pixel_size / self.helical_rise
            theta = np.deg2rad((-self.helical_twist) * zsubunits) + theta0

            # Initialize a wedge mask with ones
            wedge = np.ones(vol_dim.tolist())
            fudge = np.deg2rad(360.0 / (self.pf_number * 2))

            # Apply wedge masking based on angles
            for i in range(len(theta)):
                temp1 = np.remainder(theta[i] - fudge + 2 * np.pi, 2 * np.pi) - 2 * np.pi
                temp2 = np.remainder(theta[i] + fudge + 2 * np.pi, 2 * np.pi) - 2 * np.pi
                angles = [temp1, temp2]
                if max(angles) - min(angles) > 2 * fudge + .2:
                    above = max(angles)
                    below = min(angles)
                    inds = np.logical_or(radmatrix > above, radmatrix < below)
                else:
                    above = min(angles)
                    below = max(angles)
                    inds = np.logical_and(radmatrix > above, radmatrix < below)
                wedge[i, :, :][inds] = 0

            # Apply cosine mask filter to the wedge mask
            soft_m = np.real(np.fft.ifftn(cosmask_filter_fft * np.fft.fftn(wedge)))
            soft_m[soft_m < 0] = 0

            # Create output directory for each protofilament
            pf_dir = os.path.join(output_directory, f'{pf}')
            if not os.path.isdir(pf_dir):
                os.mkdir(pf_dir)

            # Save the masked volume as an MRC file
            output_mrc = os.path.join(pf_dir, f'pf{pf}_cylindrical_cutout.mrc')
            with mrcfile.new(output_mrc, overwrite=True) as mrc:
                mrc.set_data(soft_m.astype(np.float32))
                mrc.voxel_size = voxel_size

            print(f'Saved cylindrical cutout at {output_mrc}')

    @print_done_decorator
    def generate_wedge_mask(self):
        """
        Generates wedge masks for microtubule data.
        """

        # Parse the PDB file to get the tubulin structure
        parser = PDBParser(QUIET=True)
        structure: Structure = parser.get_structure('tubulin', self.fit_tubulin_pdb)

        # Calculate the center of gravity for the structure
        com = self.calc_geometric_center(structure)

        # Load microtubule volume and mask
        vol = mrcfile.mmap(self.microtubule_volume, 'r', permissive=True)
        mask = mrcfile.mmap(self.microtubule_mask, 'r', permissive=True)

        # Apply the mask to the volume data
        vol_data = vol.data * mask.data
        voxel_size = vol.voxel_size
        header = vol.header
        vol_dim = np.asarray(vol_data.shape)

        # Generate radial matrix for cylindrical coordinate transformation
        size = vol_dim[0] // 2
        x, y = np.meshgrid(np.arange(-size + 1, size + 1), np.arange(-size + 1, size + 1))
        radmatrix = np.remainder(np.arctan2(x, y) + 2 * np.pi, 2 * np.pi) - 2 * np.pi
        zline = np.arange(-size + 1, size + 1)

        # Create a cosine mask filter for edge smoothing
        edge_resolution = 20
        edge_width = self.pixel_size * np.ceil(edge_resolution / (2 * self.pixel_size))
        cosmask_filter = np.fft.fftshift(self.spherical_cosmask(vol_dim, 0, edge_width / self.pixel_size))
        cosmask_filter_fft = np.fft.fftn(cosmask_filter) / np.sum(cosmask_filter)

        # Prepare the output directory for storing wedges
        output_directory = os.path.join(self.output_path, "pf_wedges")
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        else:
            self.delete_folder_contents(output_directory)

        # Iterate over the number of protofilaments to generate wedges
        for pf in range(1, self.pf_number + 1):
            # Calculate initial angles and positions
            theta0 = np.arctan2(com[0], com[1]) + np.deg2rad(pf * (360 / self.pf_number))
            z0 = (com[2] + self.helical_rise * self.pf_number) / self.pixel_size
            zsubunits = (zline - z0) * self.pixel_size / self.helical_rise
            theta = np.deg2rad((-self.helical_twist) * zsubunits) + theta0

            # Initialize a wedge mask with zeros
            wedge = np.zeros(vol_dim.tolist())
            fudge = np.deg2rad(360.0 / (self.pf_number * 2))

            # Apply wedge masking based on angles
            for i in range(len(theta)):
                temp1 = np.remainder(theta[i] - fudge + 2 * np.pi, 2 * np.pi) - 2 * np.pi
                temp2 = np.remainder(theta[i] + fudge + 2 * np.pi, 2 * np.pi) - 2 * np.pi
                angles = [temp1, temp2]
                if max(angles) - min(angles) > 2 * fudge + .2:
                    above = max(angles)
                    below = min(angles)
                    inds = np.logical_or(radmatrix > above, radmatrix < below)
                else:
                    above = min(angles)
                    below = max(angles)
                    inds = np.logical_and(radmatrix > above, radmatrix < below)
                wedge[i, :, :][inds] = 1

            # Apply cosine mask filter to the wedge mask
            soft_m = np.real(np.fft.ifftn(cosmask_filter_fft * np.fft.fftn(wedge)))
            soft_m[soft_m < 0] = 0

            # Create output directory for each protofilament
            pf_dir = os.path.join(output_directory, f'{pf}')
            if not os.path.isdir(pf_dir):
                os.mkdir(pf_dir)

            # Save the masked volume as an MRC file
            output_mrc = os.path.join(pf_dir, f'pf{pf}_wedge.mrc')
            with mrcfile.new(output_mrc, overwrite=True) as mrc:
                mrc.set_data(soft_m.astype(np.float32))
                mrc.voxel_size = voxel_size

            print(f'Saved wedge at {output_mrc}')

