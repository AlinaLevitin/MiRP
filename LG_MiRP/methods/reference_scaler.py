import subprocess
import os


def rescale_and_crop_image(new_pixel_size, new_box_size, output_directory):

        path = "PF_number_refs_4xbin_tub_only_5-56Apix"
        original_pixel_size = 5.56
        new_pixel_size_name = str(new_pixel_size.get()).replace(".", "-")
        output_path = os.path.join(output_directory.get(), "new_references")

        output_scaled_path = os.path.join(output_path, "rescaled_references")
        output_cropped_path = os.path.join(output_path, "cropped_references")

        # Creating a new directories for the outputs
        if "new_references" not in os.listdir(output_directory.get()):
            os.mkdir(output_path)

        if "rescaled_references" not in os.listdir(output_path):
            os.mkdir(output_scaled_path)

        if "cropped_references" not in os.listdir(output_path):
            os.mkdir(output_cropped_path)

        reference_directory = os.listdir(path)

        print(reference_directory)

        for input_file in reference_directory:

            if input_file.endswith(".mrcs"):

                output_file = input_file.replace("5-56Apix", f"{new_pixel_size_name}Apix")
                cropped_output_file = output_file.replace('.mrc', f'{new_box_size}_boxed.mrc')

                output_scaled_file_path = os.path.join(output_scaled_path, output_file)
                output_cropped_file_path = os.path.join(output_cropped_path, cropped_output_file)

                # Rescale the image
                rescale_command = f"relion_image_handler --i {input_file.get()} --angpix {original_pixel_size} --rescale_angpix {new_pixel_size.get()} --o {output_scaled_file_path}"
                subprocess.run(rescale_command, shell=True, check=True)

                # Crop the rescaled image
                crop_command = f"relion_image_handler --i {output_scaled_file_path} --new_box {new_box_size.get()} --o {output_cropped_file_path}"
                subprocess.run(crop_command, shell=True, check=True)
