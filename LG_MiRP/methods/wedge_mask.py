import os
import numpy as np
import mrcfile
import starfile
from Bio.PDB import PDBParser
from Bio.PDB.Structure import Structure

from .method_base import MethodBase, print_done_decorator


class WedgeMaskGenerator(MethodBase):

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

        particles_star_file_data = starfile.read(input_star_file.get())
        self.particles_dataframe = particles_star_file_data['particles']
        self.data_optics_dataframe = particles_star_file_data['optics']
        self.pixel_size = self.data_optics_dataframe['rlnImagePixelSize'].iloc[0]
        self.microtubule_volume = microtubule_volume.get()
        self.microtubule_mask = microtubule_mask.get()
        self.fit_tubulin_pdb = fit_tubulin_pdb.get()
        self.pf_number = int(pf_number.get())
        self.helical_twist = int(helical_twist.get())
        self.helical_rise = int(helical_rise.get())
        self.output_path = output_path.get()

    @print_done_decorator
    def generate_wedge_mask(self):
        parser = PDBParser(QUIET=True)
        structure: Structure = parser.get_structure('tubulin', self.fit_tubulin_pdb)
        com = self.calc_center_of_gravity(structure)

        vol = mrcfile.mmap(self.microtubule_volume, 'r', permissive=True)
        mask = mrcfile.mmap(self.microtubule_mask, 'r', permissive=True)
        vol_data = vol.data * mask.data
        voxel_size = vol.voxel_size
        header = vol.header
        vol_dim = np.asarray(vol_data.shape)

        size = vol_dim[0] // 2
        x, y = np.meshgrid(np.arange(-size + 1, size + 1), np.arange(-size + 1, size + 1))
        radmatrix = np.remainder(np.arctan2(x, y) + 2 * np.pi, 2 * np.pi) - 2 * np.pi
        zline = np.arange(-size + 1, size + 1)

        edge_resolution = 20
        edge_width = self.pixel_size * np.ceil(edge_resolution / (2 * self.pixel_size))
        cosmask_filter = np.fft.fftshift(self.spherical_cosmask(vol_dim, 0, edge_width / self.pixel_size))
        cosmask_filter_fft = np.fft.fftn(cosmask_filter) / np.sum(cosmask_filter)

        output_directory = os.path.join(self.output_path, "pf_wedges")

        # Create the output directory if it does not exist
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        else:
            self.delete_folder_contents(output_directory)

        for pf in range(1, self.pf_number + 1):
            theta0 = np.arctan2(com[0], com[1]) + np.deg2rad(pf * (360/self.pf_number))
            z0 = (com[2] + self.helical_rise * self.pf_number) / self.pixel_size
            zsubunits = (zline - z0) * self.pixel_size / self.helical_rise
            theta = np.deg2rad((-self.helical_twist) * zsubunits) + theta0

            wedge = np.zeros(vol_dim.tolist())

            fudge = np.deg2rad(360.0 / (self.pf_number * 2))

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

            soft_m = np.real(np.fft.ifftn(cosmask_filter_fft * np.fft.fftn(wedge)))
            soft_m[soft_m < 0] = 0

            pf_dir = os.path.join(output_directory, f'{pf}')
            if not os.path.isdir(pf_dir):
                os.mkdir(pf_dir)

            output_mrc = os.path.join(pf_dir, f'pf{pf}_wedge.mrc')

            with mrcfile.new(output_mrc, overwrite=True) as mrc:
                mrc.set_data(soft_m.astype(np.float32))
                mrc.voxel_size = voxel_size
                mrc.header.nxstart

            print(f'Saved wedge at {output_mrc}')

    @staticmethod
    def spherical_cosmask(n, mask_radius, edge_width, origin=None):
        """mask = spherical_cosmask(n, mask_radius, edge_width, origin)
        """

        if type(n) is int:
            n = np.array([n])

        sz = np.array([1, 1, 1])
        sz[0:np.size(n)] = n[:]

        szl = -np.floor(sz / 2)
        szh = szl + sz

        x, y, z = np.meshgrid(np.arange(szl[0], szh[0]),
                              np.arange(szl[1], szh[1]),
                              np.arange(szl[2], szh[2]), indexing='ij', sparse=True)

        r = np.sqrt(x * x + y * y + z * z)

        m = np.zeros(sz.tolist())

        #    edgezone = np.where( (x*x + y*y + z*z >= mask_radius) & (x*x + y*y + z*z <= np.square(mask_radius + edge_width)))

        edgezone = np.all(
            [(x * x + y * y + z * z >= mask_radius), (x * x + y * y + z * z <= np.square(mask_radius + edge_width))],
            axis=0)
        m[edgezone] = 0.5 + 0.5 * np.cos(2 * np.pi * (r[edgezone] - mask_radius) / (2 * edge_width))
        m[np.all([(x * x + y * y + z * z <= mask_radius * mask_radius)], axis=0)] = 1

        #    m[ np.where(x*x + y*y + z*z <= mask_radius*mask_radius)] = 1

        return m

    @staticmethod
    def calc_center_of_gravity(structure):
        x_sum, y_sum, z_sum = 0, 0, 0
        total_weight = 0

        for model in structure:
            for chain in model:
                for residue in chain:
                    for atom in residue:
                        # Get the atom coordinates
                        atom_coord = atom.get_coord()
                        # Get the atom weight (assuming it's stored in B-factor)
                        atom_weight = atom.get_bfactor()
                        # Accumulate the weighted sum of coordinates
                        x_sum += atom_coord[0] * atom_weight
                        y_sum += atom_coord[1] * atom_weight
                        z_sum += atom_coord[2] * atom_weight
                        # Accumulate the total weight
                        total_weight += atom_weight

        # Calculate the center of gravity
        center_of_gravity = np.array([x_sum / total_weight, y_sum / total_weight, z_sum / total_weight])

        return center_of_gravity
