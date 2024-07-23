import numpy as np
import mrcfile
import os
from Bio.PDB import PDBParser
from .method_base import MethodBase, print_done_decorator
from .volume_mrc import VolumeMrc


class KinesinMaskGenerator(MethodBase):
    def __init__(self, fit_tubulin_pdb, microtubule_volume, output_path, sphere_radius, x_interval):
        self.fit_tubulin_pdb = fit_tubulin_pdb.get()
        self.microtubule_volume = microtubule_volume.get()
        self.output_path = output_path.get()
        self.pixel_size = None
        self.sphere_radius = float(sphere_radius.get())
        self.x_interval = float(x_interval.get())  # 8 nm or any other value

    @print_done_decorator
    def generate_multiple_spheres(self):
        try:
            # Parse the PDB file to get the tubulin structure
            parser = PDBParser(QUIET=True)
            structure = parser.get_structure('structure', self.fit_tubulin_pdb)

            # Extract chain K and residue 427
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

            # Load microtubule volume
            vol = VolumeMrc(self.microtubule_volume)
            vol_dim = np.asarray(vol.shape)
            self.pixel_size = vol.pixel
            print(f"Pixel size: {self.pixel_size}")

            # Create an empty volume
            combined_mask = np.zeros(vol_dim, dtype=np.float32)

            # Iterate through x-coordinates
            min_x = 0
            max_x = vol_dim[0]
            x_positions = np.arange(min_x, max_x, self.x_interval / self.pixel_size)

            for x in x_positions:
                # Calculate the center for each sphere
                center = np.array([int(x), vol_dim[1] // 2, vol_dim[2] // 2])
                print(f"Creating sphere at x={x} (voxel coordinates: {center})")

                # Create a spherical mask
                sphere_radius_vox = self.sphere_radius / self.pixel_size
                spherical_mask = self.create_spherical_mask(vol_dim, center, sphere_radius_vox)

                # Combine masks
                combined_mask = np.maximum(combined_mask, spherical_mask)

            # Apply cosine mask filter
            edge_resolution = 20
            edge_width = self.pixel_size * np.ceil(edge_resolution / (2 * self.pixel_size))
            cosmask_filter = np.fft.fftshift(self.spherical_cosmask(vol_dim, 0, edge_width / self.pixel_size))
            cosmask_filter_fft = np.fft.fftn(cosmask_filter) / np.sum(cosmask_filter)
            soft_m = np.real(np.fft.ifftn(np.fft.fftn(combined_mask) * cosmask_filter_fft))
            soft_m[soft_m < 0] = 0
            print(f"Softened mask stats: min={np.min(soft_m)}, max={np.max(soft_m)}, mean={np.mean(soft_m)}")

            # Save the masked volume as an MRC file
            output_directory = os.path.join(self.output_path, "spherical_masks")
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)
            else:
                self.delete_folder_contents(output_directory)
            output_mrc = os.path.join(output_directory, 'multiple_spheres_x_axis.mrc')
            with mrcfile.new(output_mrc, overwrite=True) as mrc:
                mrc.set_data(soft_m.astype(np.float32))
                mrc.voxel_size = vol.voxel_size

            print(f'Saved spherical mask with multiple spheres along x-axis at {output_mrc}')
        except Exception as e:
            print(f"Error in generate_multiple_spheres: {e}")

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
