"""
Author: Alina Levitin
Date: 01/04/24
Updated: 27/05/24

Method to rescale the references before 3D-classification
The method is utilizing relion_image_handler method to first rescale and the crop image
This method is used in rescale_references_gui
"""

import subprocess
import os

import numpy as np
from scipy.ndimage import zoom
import mrcfile

from .method_base import MethodBase, print_done_decorator
from .volume_mrc import VolumeMrc


class ReferenceScaler(MethodBase):

    def __init__(self, path, output_path, new_box_size, new_pixel_size, method):
        self.path = path.get()
        self.output_path = output_path.get()
        self.new_box_size = new_box_size.get()
        self.new_pixel_size = new_pixel_size.get()
        self.method = method.get()

        self.output_directory = None
        self.reference_files = self.get_references()

    @print_done_decorator
    def rescale_and_crop_image(self, directory, step):
        """
        A method to rescale and crop the reference images.
        :return: Generates rescaled and cropped images of the references.
        """

        self.output_directory = os.path.join(self.output_path, f'{directory}\\{step}')

        if self.perform_checks():

            # Create the output directory if it does not exist
            if not os.path.exists(self.output_directory):
                os.makedirs(self.output_directory)
            else:
                self.delete_folder_contents(self.output_directory)

            print(f"Rescaling .mrc files using {self.method}")

            # Iterate over the gathered .mrc files
            for input_mrc in self.reference_files:
                if self.method == 'relion':
                    output_scaled_path = os.path.join(self.output_directory, "rescaled_references")
                    output_cropped_path = os.path.join(self.output_directory, "cropped_references")
                    os.makedirs(output_scaled_path, exist_ok=True)
                    os.makedirs(output_cropped_path, exist_ok=True)
                    self.relion_rescale(input_mrc)
                elif self.method == 'scipy':
                    output_scaled_path = os.path.join(self.output_directory, "resampled_references")
                    os.makedirs(output_scaled_path, exist_ok=True)
                    self.scipy_rescale(input_mrc)
                else:
                    raise ValueError("Unsupported method. Choose 'relion' or 'scipy'.")

    def scipy_rescale(self, input_mrc):
        output_resampled_path = os.path.join(self.output_directory, "resampled_references")
        new_box_size = int(self.new_box_size)
        new_pixel_size = float(self.new_pixel_size)

        volume = VolumeMrc(input_mrc)
        original_data = volume.data
        voxel_size = volume.voxel_size

        # Calculate the zoom factors
        zoom_factors = tuple(np.array([voxel_size['x'], voxel_size['y'], voxel_size['z']]) / new_pixel_size)

        # Resample the data
        resampled_data = zoom(original_data, zoom_factors, mode='nearest')

        # Calculate the crop or pad sizes to achieve the desired final box size
        crop_pad_sizes = (np.array(new_box_size) - np.array(resampled_data.shape)) // 2

        # Crop or pad the resampled data to achieve the desired final box size
        if np.any(crop_pad_sizes < 0):
            # If crop is needed
            cropped_data = np.zeros(new_box_size, dtype=resampled_data.dtype)
            crop_sizes = np.array(resampled_data.shape) - np.array(new_box_size)
            crop_slices = [slice(max(0, size // 2), max(0, size // 2 + dim)) for size, dim in
                           zip(crop_sizes, new_box_size)]
            cropped_data[tuple(crop_slices)] = resampled_data
            final_data = cropped_data
        else:
            # If pad is needed
            pad_widths = [(max(0, size), max(0, size)) for size in crop_pad_sizes]
            final_data = np.pad(resampled_data, pad_widths, mode='constant')

        voxel_size_rounded = np.round(voxel_size['x'], decimals=4)
        original_pixel_size_name = str(voxel_size_rounded).replace(".", "-")
        new_pixel_size_name = str(new_pixel_size).replace(".", "_")

        output_file = os.path.basename(input_mrc).replace(original_pixel_size_name, new_pixel_size_name)
        output_mrc = output_file.replace('.mrc', f'_{new_box_size}_pix_resampled.mrc')
        output_resampled_path_mrc = os.path.join(output_resampled_path, output_mrc)

        # Save the resampled data to a new MRC file
        with mrcfile.new(output_resampled_path_mrc, overwrite=True) as mrc:
            mrc.set_data(final_data)
            mrc.voxel_size = (new_pixel_size, new_pixel_size, new_pixel_size)

        print(f'{output_resampled_path_mrc} was saved')

    def relion_rescale(self, input_mrc):
        input_file_path = os.path.join(self.path, input_mrc)
        output_scaled_path = os.path.join(self.output_directory, "rescaled_references")
        output_cropped_path = os.path.join(self.output_directory, "cropped_references")

        volume = VolumeMrc(input_file_path)
        original_pixel_size = volume.pixel

        voxel_size_rounded = np.round(original_pixel_size, decimals=4)
        original_pixel_size_name = str(voxel_size_rounded).replace(".", "-")
        new_pixel_size_name = str(self.new_pixel_size).replace(".", "-")

        output_file = input_mrc.replace(original_pixel_size_name, new_pixel_size_name)
        cropped_output_file = output_file.replace('.mrc', f'_{self.new_box_size}px_boxed.mrc')

        output_scaled_file_path = os.path.join(output_scaled_path, output_file)
        output_cropped_file_path = os.path.join(output_cropped_path, cropped_output_file)

        rescale_command = f"relion_image_handler --i {input_file_path} --angpix {original_pixel_size} --rescale_angpix {float(self.new_pixel_size)} --o {output_scaled_file_path}"
        crop_command = f"relion_image_handler --i {output_scaled_file_path} --new_box {int(self.new_box_size)} --o {output_cropped_file_path}"

        subprocess.run(rescale_command, shell=True, check=True)
        print(rescale_command.__doc__)
        subprocess.run(crop_command, shell=True, check=True)
        print(crop_command.__doc__)

    def perform_checks(self, input_background_wedge_map=None):
        # Check if RELION is installed
        if self.method == 'relion' and not self.is_relion_installed():
            print("Relion is not installed on this computer.\nTry rescaling using scipy")
            return False
        elif self.method == 'relion' and self.is_relion_installed():
            return True
        elif self.method == 'scipy':
            return True

        # Determine if self.path is a directory or a file

        if not self.reference_files:
            print("No .mrc files found in the specified path.")
            return False

    def get_references(self):

        reference_files = []

        if os.path.isdir(self.path):
            # Accessing the references
            for root, dirs, files in os.walk(self.path):
                for file in files:
                    if file.endswith(".mrc"):
                        reference_files.append(os.path.join(root, file))
        elif os.path.isfile(self.path) and self.path.endswith(".mrc"):
            # Treating the single .mrc file as a list with one file
            reference_files = [self.path]
            self.path = os.path.dirname(self.path)
        else:
            raise ValueError("The specified path is neither a directory nor a .mrc file.")

        return reference_files

