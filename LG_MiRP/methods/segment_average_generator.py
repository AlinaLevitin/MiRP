"""
Author: Alina Levitin
Date: 05/03/24
Updated: 18/04/24

Method to generate averages of segments of MTs after manual subset selection

"""
import os
import subprocess
import tensorflow as tf
import starfile
import mrcfile

from .methods_utils import is_relion_installed


def segment_average_generator(input_directory, output_directory, particles_star_file):
    """
    :param input_directory: input directory from entry
    :param output_directory: output directory from entry - usually the project directory
    :param particles_star_file: particles star file from entry
    """
    # ==================================================================================================================
    # Initializing:

    # Reading the particles.star file
    particles_star_file_data = starfile.read(particles_star_file.get())
    particles_dataframe = particles_star_file_data['particles']
    data_optics_dataframe = particles_star_file_data['optics']

    # Calculating background radius box for normalization by relion
    box_size = data_optics_dataframe['rlnImageSize']
    # box_size = int(int(image_size) / int(binning.get()))
    background_box_radius = 0.75 * box_size / 2

    # The input is a directory entry - .get() will get the path from the entry
    input_path = input_directory.get()
    output_path = os.path.join(output_directory.get(), "segment_averages")
    avg_path = os.path.join(output_path, "average_mrcs")
    norm_path = os.path.join(output_path, "norm_mrcs")

    # Creating a new directories for the outputs
    if "segment_averages" not in os.listdir(output_directory.get()):
        os.mkdir(output_path)

    if "average_mrcs" not in os.listdir(output_path):
        os.mkdir(avg_path)

    if "norm_mrcs" not in os.listdir(output_path):
        os.mkdir(norm_path)

    # ==================================================================================================================

    # Starting to iterate over mrcs files

    # Setting an empty list for the final averages-normalized mrcs files that will be saved in new_particles.star file
    new_avg_norm_images_names = []

    # Iterate over each micrograph stack in the directory path
    for dir_path, _, filenames in os.walk(input_path):
        for micrograph_stack_file in filenames:

            # for all mrcs files in the directory path
            if micrograph_stack_file.endswith(".mrcs"):
                # Generates a path for the mrcs file
                micrograph_stack_path = os.path.join(dir_path, micrograph_stack_file)
                # Using mrcfile library, opens the mrcs file and converts it to a tensorFlow tensor
                with mrcfile.open(micrograph_stack_path) as mrc:
                    # Check the dimensions of the MRC file
                    if mrc.header.nz > 1:
                        mrc_data = tf.convert_to_tensor(mrc.data, dtype=tf.float32)
                        print('Working on', micrograph_stack_file)

                        # Generates a path for each star file of each mrcs file
                        star_file_path = micrograph_stack_path.replace(".mrcs", "_extract.star")
                        # Using starfile library reads the star file and converts it to pandas DataFrame
                        star_data = starfile.read(star_file_path)
                        # Finds the maximum number of MTs in each star file using rlnHelicalTubeID
                        number_of_MTs_in_stack = star_data['rlnHelicalTubeID'].max()
                        print(f'{micrograph_stack_file} contains {number_of_MTs_in_stack} MTs\n', '-' * 100)

                        # loops over the MTs in the mrcs file according to their ID (rlnHelicalTubeID)
                        for MT in range(1, number_of_MTs_in_stack + 1):
                            # creating a mask to filter only the micrographs for the id of the MT
                            mask = star_data['rlnHelicalTubeID'] == MT
                            # filters the star file data for the selected MT ID
                            MT_star_data = star_data.loc[mask]
                            # checks if the data is not empty
                            if not MT_star_data.empty:
                                # extracts the number of segments
                                MT_number_of_segments = MT_star_data.shape[0]
                                # marks the starting and ending points of each MT according to the pandas DataFrame
                                # index
                                MT_start = MT_star_data.index[0]
                                MT_end = MT_star_data.index[-1]
                                print(f'MT number {MT} in {micrograph_stack_file} contains {MT_number_of_segments} number of segments'
                                      f' from {MT_start} to {MT_end}')
                                # selects the corresponding micrographs assuming theis numbering are the same as the DataFrame index
                                # uses the starting and ending points of each MT and the helical rise divided by pixels
                                # this is temporary since in my practice-data I didn't have helical rise

                                # Temporary: (delete this for real data)
                                helical_rise: int = 1
                                pixel = 1

                                # slicing the dataframe according to  the start and end of a microtubule
                                MT_stack = mrc_data[MT_start:MT_end:]
                                # performs a "Z-stack" according to the mean intensity in each pixel
                                # ========================================================================================================

                                # AVERAGE:

                                # Averaging the intensity of pixels in the mrcs stack file
                                MT_stack_average = tf.reduce_mean(MT_stack, axis=0)
                                # =======================================================================================================

                                # NORMALIZATION

                                # Normalization so all values will be between 0 and 1 and removing background (minimum
                                # intensity)
                                normalized_matrix = (MT_stack_average - tf.reduce_min(MT_stack_average)) / (
                                        tf.reduce_max(MT_stack_average) - tf.reduce_min(MT_stack_average))

                                # converts the tensorFlow tensor to numpy - this is the new mrc containing all the
                                # segments of a
                                # specific MT according to its ID (rlnHelicalTubeID) in a mrcs file of extracted
                                # particles from relion
                                MT_stack_norm_average_array = normalized_matrix.numpy()

                                # The new mrcs files of the averages:
                                avg_file = os.path.join(avg_path, f'{micrograph_stack_file}_avg_MT_{MT}.mrcs')

                                # Saving the new mrc files (numpy matrix) using mrcfile library
                                with mrcfile.new(avg_file, overwrite=True) as mrcs:
                                    # Write the NumPy array to the MRC file
                                    mrcs.set_data(MT_stack_norm_average_array)
                                    print(f'Finished averaging MT {MT} in {micrograph_stack_file}\n'
                                          f'File was saved to {avg_file}')

                                # =======================================================================================================

                                # RELION NORMALIZATION

                                # setting a normalized file name
                                new_norm_name = f'{micrograph_stack_file.replace(".mrcs", "")}_norm_MT_{MT}.mrcs'
                                norm_file = os.path.join(norm_path, new_norm_name)

                                # checking if relion is installed (I was testing it on my personal computer that didn't
                                # have relion
                                # and was too lazy to comment this out everytime I changed computers)

                                if is_relion_installed():
                                    relion_preprocess_norm_args = ["relion_preprocess",
                                                                   "--norm",
                                                                   "true",
                                                                   "--bg_radius",
                                                                   str(background_box_radius),
                                                                   "--operate_on",
                                                                   str(avg_file),
                                                                   "--operate_out",
                                                                   str(norm_file)]

                                    subprocess.run(relion_preprocess_norm_args)
                                else:
                                    print("Relion is not installed on this computer.")

                                # Updating the file links (_rlnImageName) in the particles.star to the averaged
                                # normalized file names
                                # in the following manner:
                                # 000001@segment_averages/norm_mrcs/gc_Cin8_Aug07_18_1000_0000_Aug08_23.09.41_mc2_DW.mrcs_norm_MT_1.mrcs
                            for index, row in particles_dataframe.iterrows():
                                if micrograph_stack_file in row['rlnImageName'] and MT == row['rlnHelicalTubeID']:
                                    new_link = "/".join(['segment_averages', 'norm_mrcs', new_norm_name])
                                    particles_dataframe.loc[index, 'rlnMicrographName'] = new_link

                            print(f'Finished working on MT {MT} in {micrograph_stack_file} \n', '-' * 100)

                print(f'Finished working on {micrograph_stack_file} \n', '=' * 100)

    # particles_dataframe['filename'] = particles_dataframe['rlnImageName'].apply(lambda x: x.split('/')[-1])
    #
    # particles_dataframe_no_duplicates = particles_dataframe.drop_duplicates(subset=['filename'])

    # Generating a new star file named segment_average.star in the output directory
    # particles_dataframe['rlnImageName'] = new_avg_norm_images_names
    new_particles_star_file_data = {'optics': data_optics_dataframe, 'particles': particles_dataframe}

    os.chdir(output_path)
    output_file = 'segment_average.star'
    try:
        starfile.write(new_particles_star_file_data, output_file)
    except NameError:
        print(f"File names {output_file} already exists, delete old file and try again")
        raise NameError("File already exists")

    print("Processing complete.")

    return particles_dataframe
