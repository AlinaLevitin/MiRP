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

from .methods_utils import is_relion_installed


def rescale_and_crop_image(path, new_pixel_size, new_box_size, output_directory):
    """
    A method to rescale and crop the reference images
    :param path: path for the references
    :param new_pixel_size: selected pixel size after particle extraction
    :param new_box_size: The box size after particle extraction
    :param output_directory: selected directory for output
    :return: Generates rescaled and cropped images of the references from the PF_number_refs_4xbin_tub_only_5-56Apix
                folder
    """
    # Folder with the original references
    optional_references = {
                            "References/PF_number_refs_4xbin_tub_only_5-56Apix": 5.56,
                            "References/13pf/kinesin_ref": 6.136
                            }

    # Original pixel size
    original_pixel_size = optional_references[path]

    original_pixel_size_name = str(original_pixel_size).replace(".", "-")
    # generating a new name for the references according to the selected pixel size (new_pixel_size) in a new folder
    # named new_references
    new_pixel_size_name = str(new_pixel_size.get()).replace(".", "-")
    output_path = os.path.join(output_directory.get(), "new_references")

    # generating two new folder for rescaled and cropped references (for 3D Classification use the cropped references
    output_scaled_path = os.path.join(output_path, "rescaled_references")
    output_cropped_path = os.path.join(output_path, "cropped_references")

    # Creating new directories for the outputs
    if "new_references" not in os.listdir(output_directory.get()):
        os.mkdir(output_path)

    if "rescaled_references" not in os.listdir(output_path):
        os.mkdir(output_scaled_path)

    if "cropped_references" not in os.listdir(output_path):
        os.mkdir(output_cropped_path)

    # Accessing the references
    reference_directory = os.listdir(path)

    # Iterates over the references and selects only mrc files
    for input_file in reference_directory:

        if input_file.endswith(".mrc"):
            # Checking if there is relion installed on this computer
            if is_relion_installed():
                # Generating new names for the output files
                output_file = input_file.replace(original_pixel_size_name, new_pixel_size_name)
                cropped_output_file = output_file.replace('.mrc', f'{new_box_size}_boxed.mrc')

                # Generating paths for the output files
                output_scaled_file_path = os.path.join(output_scaled_path, output_file)
                output_cropped_file_path = os.path.join(output_cropped_path, cropped_output_file)

                # Rescale the image using relion_image_handles
                rescale_command = f"relion_image_handler --i {os.path.join(path, input_file)} --angpix {original_pixel_size} --rescale_angpix {float(new_pixel_size.get())} --o {os.path.join(output_scaled_path, output_scaled_file_path)}"
                subprocess.run(rescale_command, shell=True, check=True)

                # Crop the rescaled image using relion_image_handles
                crop_command = f"relion_image_handler --i {os.path.join(output_scaled_path, output_scaled_file_path)} --new_box {int(new_box_size.get())} --o {os.path.join(output_cropped_path, output_cropped_file_path)}"
                subprocess.run(crop_command, shell=True, check=True)

            else:
                print("Relion is not installed on this computer.")
