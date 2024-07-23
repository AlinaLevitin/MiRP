import numpy as np
import mrcfile
import os
from Bio.PDB import PDBParser, Structure
from .method_base import MethodBase, print_done_decorator
from .volume_mrc import VolumeMrc

class KinesinMaskGenerator(MethodBase):
    def __init__(self, fit_tubulin_pdb, microtubule_volume, output_path, sphere_radius):
        self.fit_tubulin_pdb = fit_tubulin_pdb.get()
        self.microtubule_volume = microtubule_volume.get()
        self.output_path = output_path.get()
        self.pixel_size = None
        self.sphere_radius = float(sphere_radius.get())

    @print_done_decorator
    def generate_spherical_mask(self):
        try:
            # Parse the PDB file to get the tubulin structure
            parser = PDBParser(QUIET=True)
            structure = parser.get_structure('structure', self.fit_tubulin_pdb)

            # Extract chain K
            chain_K = None
            for model in structure:
                for chain in model:
                    if chain.get_id() == 'K':
                        chain_K = chain
                        break
                if chain_K is not None:
                    break

            if chain_K is None:
                raise ValueError("Chain K not found in the structure")

            # Calculate geometric center of chain K
            com = self.calc_geometric_center(chain_K)
            print(f"Geometric center of chain K: {com}")

            # Load microtubule volume and mask
            vol = VolumeMrc(self.microtubule_volume)
            vol_dim = np.asarray(vol.shape)
            self.pixel_size = vol.pixel

            # Convert geometric center to voxel coordinates
            com_voxel = np.round(com / self.pixel_size).astype(int)
            print(f"Geometric center in voxel coordinates (before clipping): {com_voxel}")

            # Adjust the geometric center if it is too close to the edge
            com_voxel = np.clip(com_voxel, self.sphere_radius, vol_dim - self.sphere_radius - 1)
            print(f"Adjusted geometric center in voxel coordinates: {com_voxel}")

            # Create a spherical mask
            sphere_radius_vox = self.sphere_radius / self.pixel_size
            spherical_mask = self.create_spherical_mask(vol_dim, com_voxel, sphere_radius_vox)
            print(f"Spherical mask stats: min={np.min(spherical_mask)}, max={np.max(spherical_mask)}, mean={np.mean(spherical_mask)}")

            # Apply cosine mask filter
            edge_resolution = 40
            edge_width = self.pixel_size * np.ceil(edge_resolution / (2 * self.pixel_size))
            cosmask_filter = np.fft.fftshift(self.spherical_cosmask(vol_dim, 0, edge_width / self.pixel_size))
            cosmask_filter_fft = np.fft.fftn(cosmask_filter) / np.sum(cosmask_filter)
            soft_m = np.real(np.fft.ifftn(cosmask_filter_fft * np.fft.fftn(spherical_mask)))
            soft_m[soft_m < 0] = 0
            print(f"Softened mask stats: min={np.min(soft_m)}, max={np.max(soft_m)}, mean={np.mean(soft_m)}")

            # Save the masked volume as an MRC file
            output_directory = os.path.join(self.output_path, "spherical_masks")
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)
            else:
                self.delete_folder_contents(output_directory)
            output_mrc = os.path.join(output_directory, 'spherical_mask.mrc')
            with mrcfile.new(output_mrc, overwrite=True) as mrc:
                mrc.set_data(soft_m.astype(np.float32))
                mrc.voxel_size = vol.voxel_size

            print(f'Saved spherical mask at {output_mrc}')
        except Exception as e:
            print(f"Error in generate_spherical_mask: {e}")

    @staticmethod
    def calc_geometric_center(chain):
        """
        Calculates the geometric center of a chain.

        :param chain: (Bio.PDB.Chain): A chain containing residues and atoms.
        :return center: (numpy array): The coordinates of the geometric center.
        """
        atom_coords = [atom.get_coord() for residue in chain for atom in residue]
        center = np.mean(atom_coords, axis=0)
        return center

    @staticmethod
    def create_spherical_mask(grid_size, center, radius):
        center = np.round(center).astype(int)
        center = np.clip(center, 0, np.array(grid_size) - 1)

        x = np.arange(grid_size[0])
        y = np.arange(grid_size[1])
        z = np.arange(grid_size[2])
        xx, yy, zz = np.meshgrid(x, y, z, indexing='ij')

        distance = np.sqrt((xx - center[0]) ** 2 + (yy - center[1]) ** 2 + (zz - center[2]) ** 2)

        mask = np.zeros(grid_size, dtype=np.float32)
        mask[distance <= radius] = 1

        print(f"Distance array stats: min={np.min(distance)}, max={np.max(distance)}, mean={np.mean(distance)}")
        print(f"Mask stats: min={np.min(mask)}, max={np.max(mask)}, mean={np.mean(mask)}")
        print(f"Spherical mask created with center: {center} and radius: {radius} Angstrom")

        return mask
