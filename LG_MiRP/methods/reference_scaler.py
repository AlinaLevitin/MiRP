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

from .methods_utils import is_relion_installed, delete_folder_contents


def rescale_and_crop_image(path, new_pixel_size, new_box_size, output_directory, method='relion'):
    """
    A method to rescale and crop the reference images
    :param method: relion of scipy
    :param path: path for the references
    :param new_pixel_size: selected pixel size after particle extraction
    :param new_box_size: The box size after particle extraction
    :param output_directory: selected directory for output
    :return: Generates rescaled and cropped images of the references from the PF_number_refs_4xbin_tub_only_5-56Apix
                folder
    """

    output_path = os.path.join(output_directory.get(), "new_references")

    # Creating new directories for the outputs
    if "new_references" not in os.listdir(output_directory.get()):
        os.mkdir(output_path)
    else:
        delete_folder_contents(output_path)

    if method == 'relion':
        # generating two new folder for rescaled and cropped references (for 3D Classification use the cropped references
        output_scaled_path = os.path.join(output_path, "rescaled_references")
        output_cropped_path = os.path.join(output_path, "cropped_references")

        os.mkdir(output_scaled_path)

        os.mkdir(output_cropped_path)

    else:
        output_scaled_path = os.path.join(output_path, "resampled_references")
        os.mkdir(output_scaled_path)

    # Accessing the references
    reference_directory = os.listdir(path)

    # Iterates over the references and selects only mrc files
    for input_file in reference_directory:

        if input_file.endswith(".mrc"):

            if method == 'relion':

                relion_rescale(path, output_path, input_file, new_box_size, new_pixel_size)
            else:
                scipy_rescale(output_path, input_file, new_box_size, new_pixel_size)


def scipy_rescale(output_path, input_file, new_box_size, new_pixel_size):

    output_resampled_path = os.path.join(output_path, "resampled_references")

    with mrcfile.open(input_file, 'r', permissive=True) as mrc:
        original_data = mrc.data
        voxel_size = mrc.voxel_size
        voxel_size_array = np.array([voxel_size['x'], voxel_size['y'], voxel_size['z']])

    # Calculate the current dimensions
    current_shape = original_data.shape

    # Calculate the zoom factors
    zoom_factors = tuple(voxel_size_array / float(new_pixel_size))

    # Resample the data
    resampled_data = zoom(original_data, zoom_factors, mode='nearest')

    # Calculate the crop or pad sizes to achieve the desired final box size
    crop_pad_sizes = (np.array(new_box_size) - np.array(resampled_data.shape)) // 2

    # Crop or pad the resampled data to achieve the desired final box size
    if np.any(crop_pad_sizes < 0):
        # If crop is needed
        cropped_data = np.zeros(new_box_size, dtype=resampled_data.dtype)

        crop_sizes = np.array(resampled_data.shape) - np.array(new_box_size)

        # Calculate the slice ranges for cropping or padding
        crop_slices = [slice(max(0, size // 2), max(0, size // 2 + dim)) for size, dim in zip(crop_sizes, new_box_size)]

        # Assign the resampled data to the appropriate slices in cropped_data
        cropped_data[tuple(crop_slices)] = resampled_data
        final_data = cropped_data
    else:
        # If pad is needed
        pad_widths = [(max(0, size), max(0, size)) for size in crop_pad_sizes]
        final_data = np.pad(resampled_data, pad_widths, mode='constant')

    original_pixel_size_name = str(voxel_size['x']).replace(".", "_")
    new_pixel_size_name = str(new_pixel_size.get()).replace(".", "_")

    output_file = input_file.replace(original_pixel_size_name, new_pixel_size_name)
    output_mrc = output_file.replace('.mrc', f'_{str(new_box_size.get())}pix_resampled.mrc')

    output_resampled_path_mrc = os.path.join(output_resampled_path, output_mrc)

    # Save the resampled data to a new MRC file
    with mrcfile.new(output_resampled_path_mrc, overwrite=True) as mrc:
        mrc.set_data(final_data)
        mrc.voxel_size = (new_pixel_size, new_pixel_size, new_pixel_size)


def relion_rescale(path, output_path, input_file, new_box_size, new_pixel_size):

    output_scaled_path = os.path.join(output_path, "rescaled_references")
    output_cropped_path = os.path.join(output_path, "cropped_references")

    with mrcfile.open(input_file, 'r', permissive=True) as mrc:
        original_pixel_size = mrc.voxel_size['x']

    original_pixel_size_name = str(original_pixel_size).replace(".", "_")
    # generating a new name for the references according to the selected pixel size (new_pixel_size) in a new folder
    # named new_references
    new_pixel_size_name = str(new_pixel_size.get()).replace(".", "_")

    output_file = input_file.replace(original_pixel_size_name, new_pixel_size_name)
    cropped_output_file = output_file.replace('.mrc', f'_{str(new_box_size.get())}pix_boxed.mrc')

    # Generating paths for the output files
    output_scaled_file_path = os.path.join(output_scaled_path, output_file)
    output_cropped_file_path = os.path.join(output_cropped_path, cropped_output_file)

    if is_relion_installed():
        # Rescale the image using relion_image_handles
        rescale_command = f"relion_image_handler --i {os.path.join(path, input_file)} --angpix {original_pixel_size} --rescale_angpix {float(new_pixel_size.get())} --o {output_scaled_file_path}"
        subprocess.run(rescale_command, shell=True, check=True)

        # Crop the rescaled image using relion_image_handles
        crop_command = f"relion_image_handler --i {os.path.join(output_scaled_path, output_scaled_file_path)} --new_box {int(new_box_size.get())} --o {output_cropped_file_path}"
        subprocess.run(crop_command, shell=True, check=True)

    else:
        print("Relion is not installed on this computer.")