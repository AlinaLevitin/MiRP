import numpy as np
import mrcfile
import os
from Bio.PDB import PDBParser
from Bio.PDB.Structure import Structure
from .method_base import MethodBase, print_done_decorator

class KinesinMaskGenerator(MethodBase):
    def __init__(self, fit_tubulin_pdb, microtubule_volume, microtubule_mask, output_path, pixel_size, sphere_radius):
        self.fit_tubulin_pdb = fit_tubulin_pdb.get()
        self.microtubule_volume = microtubule_volume.get()
        self.microtubule_mask = microtubule_mask.get()
        self.output_path = output_path.get()
        self.pixel_size = float(pixel_size.get())
        self.sphere_radius = float(sphere_radius.get())

    @print_done_decorator
    def generate_spherical_mask(self):
        """
        Generates spherical masks for microtubule data.
        """

        try:
            # Parse the PDB file to get the tubulin structure
            parser = PDBParser(QUIET=True)
            structure: Structure = parser.get_structure('tubulin', self.fit_tubulin_pdb)

            # Calculate the center of gravity for the structure
            com = self.calc_center_of_gravity(structure)
            print(f"Center of gravity: {com}")

            # Load microtubule volume and mask
            with mrcfile.open(self.microtubule_volume, 'r') as vol:
                vol_data = vol.data
                voxel_size = vol.voxel_size
                vol_dim = np.asarray(vol_data.shape)
            with mrcfile.open(self.microtubule_mask, 'r') as mask:
                mask_data = mask.data

            # Ensure the mask and volume have the same dimensions
            mask_dim = np.asarray(mask_data.shape)
            if not np.all(vol_dim == mask_dim):
                raise ValueError("Volume and mask dimensions do not match")

            # Convert center of gravity to voxel coordinates
            com_voxel = np.round(com / self.pixel_size).astype(int)
            # Adjust the center of gravity if it is too close to the edge
            com_voxel = np.clip(com_voxel, self.sphere_radius, vol_dim - self.sphere_radius - 1)
            print(f"Adjusted center of mass in voxel coordinates: {com_voxel}")

            # Create a spherical mask with the specified radius centered at the COM
            sphere_radius_vox = self.sphere_radius / self.pixel_size
            spherical_mask = self.create_spherical_mask(vol_dim, com_voxel, sphere_radius_vox)

            # Check the contents of the spherical mask
            print(f"Spherical mask stats: min={np.min(spherical_mask)}, max={np.max(spherical_mask)}, mean={np.mean(spherical_mask)}")

            # Apply cosine mask filter to the spherical mask
            edge_resolution = 20
            edge_width = self.pixel_size * np.ceil(edge_resolution / (2 * self.pixel_size))
            cosmask_filter = np.fft.fftshift(self.spherical_cosmask(vol_dim, 0, edge_width / self.pixel_size))
            cosmask_filter_fft = np.fft.fftn(cosmask_filter) / np.sum(cosmask_filter)
            soft_m = np.real(np.fft.ifftn(cosmask_filter_fft * np.fft.fftn(spherical_mask)))
            soft_m[soft_m < 0] = 0

            # Check the contents of the softened mask
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
                mrc.voxel_size = voxel_size

            print(f'Saved spherical mask at {output_mrc}')
        except Exception as e:
            print(f"Error in generate_spherical_mask: {e}")

    @staticmethod
    def create_spherical_mask(grid_size, center, radius):
        """
        Create a spherical mask.

        :param grid_size: (tuple): The size of the grid (nx, ny, nz).
        :param center: (tuple): The center of the sphere (cx, cy, cz).
        :param radius: (float): The radius of the sphere.
        :return mask: (numpy array): The spherical mask.
        """
        # Convert center to integer and ensure it is within bounds
        center = np.round(center).astype(int)
        center = np.clip(center, 0, np.array(grid_size) - 1)  # Clip to avoid out-of-bounds issues

        # Create a grid of coordinates
        x = np.arange(grid_size[0])
        y = np.arange(grid_size[1])
        z = np.arange(grid_size[2])
        xx, yy, zz = np.meshgrid(x, y, z, indexing='ij')

        # Calculate distances from the center
        distance = np.sqrt((xx - center[0]) ** 2 + (yy - center[1]) ** 2 + (zz - center[2]) ** 2)

        # Create mask based on distance
        mask = np.zeros(grid_size, dtype=np.float32)
        mask[distance <= radius] = 1

        # Debugging: print statistics and a slice of the mask
        print(f"Distance array stats: min={np.min(distance)}, max={np.max(distance)}, mean={np.mean(distance)}")
        print(f"Mask stats: min={np.min(mask)}, max={np.max(mask)}, mean={np.mean(mask)}")
        print(f"Spherical mask created with center: {center} and radius: {radius}")
        print(f"Spherical mask (slice) sample: {mask[:, :, mask.shape[2] // 2]}")  # Display a central slice

        return mask
