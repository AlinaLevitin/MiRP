"""
Author: Alina Levitin
Date: 05/03/24
Version: 1.0

Class to generate averages of segments of MTs.
Need to provide a title and an image(optional)
"""
import os
import subprocess
import tensorflow as tf
import starfile
import mrcfile


def preprocess_segment_averages(directory, particles_star_file, binning):
    """

    :param binning:
    :param directory:
    :param particles_star_file:
    :param helical_rise: (in angstrem)
    :param box_size: (in pixels, ~600A (432 pixels if 1.39A/pixel) ->
    Re-scaled size (pixels): *Original particle box size/4* 432/4=108)
    :return:
    """
    # Initializing:

    # Reading the particles.star file
    print(particles_star_file.get())
    particles_star_file_data = starfile.read(particles_star_file.get())
    particles_dataframe = particles_star_file_data['particles']
    data_optics_dataframe = particles_star_file_data['optics']

    # Calculating background radius box for normalization by relion
    image_size = data_optics_dataframe['rlnImageSize']
    box_size = int(int(image_size)/int(binning.get()))
    background_box_radius = 0.75 * box_size / 2

    # The input is a directory entry - .get() will get the path from the entry
    path = directory.get()

    # Setting an empty list for the final averages-normalized mrcs files that will be saved in new_particles.star file
    new_image_name = []

    # Iterate over each micrograph stack in the directory path
    for micrograph_stack_file in os.listdir(path):

        # for all mrcs files in the directory path
        if micrograph_stack_file.endswith(".mrcs"):
            # Generates a path for the mrcs file
            micrograph_stack_path = os.path.join(path, micrograph_stack_file)
            # Using mrcfile library, opens the mrcs file and converts it to a tensorFlow tensor
            with mrcfile.open(micrograph_stack_path) as mrc:
                mrc_data = tf.convert_to_tensor(mrc.data, dtype=tf.float32)

            print('Working on', micrograph_stack_file)

            # Generates a path for each star file of each mrcs file
            star_file_path = micrograph_stack_path.replace(".mrcs", "_extract.star")
            # Using starfile library reads the star file and converts it to pandas DataFrame
            star_data = starfile.read(star_file_path)
            # Finds the maximum number of MTs in each star file using rlnHelicalTubeID
            number_of_MTs_in_stack = star_data['rlnHelicalTubeID'].max()
            print(f'{micrograph_stack_file} contains {number_of_MTs_in_stack} MTs')

            # loops over the MTs in the mrcs file according to their ID (rlnHelicalTubeID)
            for MT in range(1, number_of_MTs_in_stack + 1):
                # creating a mask to filter only the micrographs for the id of the MT
                mask = star_data['rlnHelicalTubeID'] == MT
                # filters the star file data for the selected MT ID
                MT_star_data = star_data.loc[mask]
                # extracts the number of segments
                MT_number_of_segments = MT_star_data.shape[0]
                # marks the starting and ending points of each MT according to the pandas DataFrame index
                MT_start = MT_star_data.index[0]
                MT_end = MT_star_data.index[-1]
                print(f'MT number {MT} in {micrograph_stack_file} contains {MT_number_of_segments} number of segments'
                      f' from {MT_start} to {MT_end}')
                # selects the corresponding micrographs assuming theis numbering are the same as the DataFrame index
                # uses the starting and ending points of each MT and the helical rise divided by pixels
                # this is temporary since in my play-data I didn't have helical rise

                # Temporary: (delete this for real data)
                helical_rise: int = 82
                pixel = 1.1

                MT_stack = mrc_data[MT_start:MT_end:int(helical_rise/pixel), :]
                # performs a "Z-stack" according to the mean intensity in each pixel

                # Averaging the intensity of pixels in the mrcs stack file
                MT_stack_average = tf.reduce_mean(MT_stack, axis=0)

                normalized_matrix = (MT_stack_average - tf.reduce_min(MT_stack_average)) / (tf.reduce_max(MT_stack_average) - tf.reduce_min(MT_stack_average))

                # converts the tensorFlow tensor to numpy - this is the new mrc containing all the segments of a
                # specific MT according to its ID (rlnHelicalTubeID) in a mrcs file of extracted particles from relion
                MT_stack_norm_average_array = normalized_matrix.numpy()

                # The new mrcs files of the averages:
                avg_file = f'{micrograph_stack_file}_avg_MT_#{MT}.mrcs'

                # Saving the new mrc files (numpy matrix) using mrcfile library
                with mrcfile.new(f'{avg_file}', overwrite=True) as mrcs:
                    # Write the NumPy array to the MRC file
                    mrcs.set_data(MT_stack_norm_average_array)
                    print(f'Finished averaging MT {MT} in {micrograph_stack_file}\n'
                          f'File was saved to {os.path.join(os.getcwd(), avg_file)}')

                # Normalization

                # relion_preprocess --norm true --bg_radius $background_box_radius
                # --operate_on f'{micrograph_stack_file}_avg_MT_#{MT}.mrc'
                # --operate_out f'{micrograph_stack_file}_norm_MT_#{MT}.mrc'

                norm_file = f'{micrograph_stack_file}_norm_MT_#{MT}.mrcs'

                relion_preprocess_norm_args = ["relion_preprocess",
                                               "--norm", "true",
                                               "--bg_radius",
                                               str(background_box_radius),
                                               "--operate_on",
                                               str(avg_file),
                                               "--operate_out",
                                               str(norm_file)]

                # subprocess.run(relion_preprocess_norm_args)

                for index, row in particles_dataframe.iterrows():
                    if micrograph_stack_file in row['rlnImageName'] and MT == row['rlnHelicalTubeID']:
                        new_image_name.append(row['rlnImageName'].replace(micrograph_stack_file, avg_file))

                print(f'Finished working on MT {MT} in {micrograph_stack_file} \n', '-' * 100)

        print(f'Finished working on {micrograph_stack_file} \n', '=' * 100)

    particles_dataframe['rlnImageName'] = new_image_name
    print(particles_dataframe['rlnImageName'])

    print("Processing complete.")
