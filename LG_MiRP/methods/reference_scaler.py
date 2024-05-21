"""
Author: Alina Levitin
Date: 01/04/24
Updated: 09/04/24

Method to rescale the references before 3D-classification
The method is utilizing relion_image_handler method to first rescale and the crop image
This method is used in rescale_references_gui
"""

import subprocess
import os

import numpy as np
import mrcfile
from scipy.ndimage import zoom

from .method_base import MethodBase, print_done_decorator


class ReferenceScaler(MethodBase):

    def __init__(self, path, output_path, new_box_size, new_pixel_size):
        self.path = path
        self.output_path = output_path.get()
        self.new_box_size = new_box_size.get()
        self.new_pixel_size = new_pixel_size.get()

    @print_done_decorator
    def rescale_and_crop_image(self, method='relion'):
        """
        A method to rescale and crop the reference images.
        :param method: 'relion' or 'scipy'
        :return: Generates rescaled and cropped images of the references.
        """
        output_directory = os.path.join(self.output_path, "new_references")

        # Create the output directory if it does not exist
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        else:
            self.delete_folder_contents(output_directory)

        if method == 'relion':
            output_scaled_path = os.path.join(output_directory, "rescaled_references")
            output_cropped_path = os.path.join(output_directory, "cropped_references")
            os.makedirs(output_scaled_path, exist_ok=True)
            os.makedirs(output_cropped_path, exist_ok=True)
        elif method == 'scipy':
            output_scaled_path = os.path.join(output_directory, "resampled_references")
            os.makedirs(output_scaled_path, exist_ok=True)
        else:
            raise ValueError("Unsupported method. Choose 'relion' or 'scipy'.")

        # Accessing the references
        reference_directory = os.listdir(self.path)

        # Iterates over the references and selects only mrc files
        for input_mrc in reference_directory:
            if input_mrc.endswith(".mrc"):
                if method == 'relion':
                    self.relion_rescale(input_mrc)
                elif method == 'scipy':
                    self.scipy_rescale(input_mrc)
                else:
                    raise ValueError("Unsupported method. Choose 'relion' or 'scipy'.")

    # @progress_bar_decorator
    def scipy_rescale(self, input_mrc):
        output_resampled_path = os.path.join(self.output_path, "new_references", "resampled_references")
        input_file_path = os.path.join(self.path, input_mrc)
        new_box_size = int(self.new_box_size)
        new_pixel_size = float(self.new_pixel_size)

        with mrcfile.open(input_file_path, 'r', permissive=True) as mrc:
            original_data = mrc.data
            voxel_size = mrc.voxel_size
            voxel_size_array = np.array([voxel_size['x'], voxel_size['y'], voxel_size['z']])

        # Calculate the zoom factors
        zoom_factors = tuple(voxel_size_array / new_pixel_size)

        # Resample the data
        resampled_data = zoom(original_data, zoom_factors, mode='nearest')

        # Calculate the crop or pad sizes to achieve the desired final box size
        crop_pad_sizes = (np.array(new_box_size) - np.array(resampled_data.shape)) // 2

        # Crop or pad the resampled data to achieve the desired final box size
        if np.any(crop_pad_sizes < 0):
            # If crop is needed
            cropped_data = np.zeros(new_box_size, dtype=resampled_data.dtype)
            crop_sizes = np.array(resampled_data.shape) - np.array(new_box_size)
            crop_slices = [slice(max(0, size // 2), max(0, size // 2 + dim)) for size, dim in zip(crop_sizes, new_box_size)]
            cropped_data[tuple(crop_slices)] = resampled_data
            final_data = cropped_data
        else:
            # If pad is needed
            pad_widths = [(max(0, size), max(0, size)) for size in crop_pad_sizes]
            final_data = np.pad(resampled_data, pad_widths, mode='constant')

        voxel_size_rounded = np.round(voxel_size['x'], decimals=4)
        original_pixel_size_name = str(voxel_size_rounded).replace(".", "-")
        new_pixel_size_name = str(new_pixel_size).replace(".", "-")

        output_file = input_mrc.replace(original_pixel_size_name, new_pixel_size_name)
        output_mrc = output_file.replace('.mrc', f'_{new_box_size}pix_resampled.mrc')
        output_resampled_path_mrc = os.path.join(output_resampled_path, output_mrc)

        # Save the resampled data to a new MRC file
        with mrcfile.new(output_resampled_path_mrc, overwrite=True) as mrc:
            mrc.set_data(final_data)
            mrc.voxel_size = (new_pixel_size, new_pixel_size, new_pixel_size)

        print(f'{output_resampled_path_mrc} was saved')

    # @progress_bar_decorator
    def relion_rescale(self, input_mrc):
        input_file_path = os.path.join(self.path, input_mrc)
        output_scaled_path = os.path.join(self.output_path, "new_references", "rescaled_references")
        output_cropped_path = os.path.join(self.output_path, "new_references", "cropped_references")

        with mrcfile.open(input_file_path, 'r', permissive=True) as mrc:
            original_pixel_size = mrc.voxel_size['x']

        voxel_size_rounded = np.round(original_pixel_size, decimals=4)
        original_pixel_size_name = str(voxel_size_rounded).replace(".", "-")
        new_pixel_size_name = str(self.new_pixel_size).replace(".", "-")

        output_file = input_mrc.replace(original_pixel_size_name, new_pixel_size_name)
        cropped_output_file = output_file.replace('.mrc', f'_{self.new_box_size}px_boxed.mrc')

        output_scaled_file_path = os.path.join(output_scaled_path, output_file)
        output_cropped_file_path = os.path.join(output_cropped_path, cropped_output_file)

        if self.is_relion_installed():
            rescale_command = f"relion_image_handler --i {input_file_path} --angpix {original_pixel_size} --rescale_angpix {float(self.new_pixel_size)} --o {output_scaled_file_path}"
            subprocess.run(rescale_command, shell=True, check=True)
            crop_command = f"relion_image_handler --i {output_scaled_file_path} --new_box {int(self.new_box_size)} --o {output_cropped_file_path}"
            subprocess.run(crop_command, shell=True, check=True)
        else:
            print("Relion is not installed on this computer.")
