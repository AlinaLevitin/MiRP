import os
import tensorflow as tf
import starfile
import mrcfile


def preprocess_segment_averages(directory, particles_star_file, box_size: int = 58):

    # Calculate background radius box for normalization
    background_box_radius = 0.75 * box_size / 2

    # The input is a directory entry - .get() will get the path from the entry
    path = directory.get()
    MT_image_name = []

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
                # uses the starting and ending points of each MT and the box size
                # whereas the box size is the distance in pixels that represents a tubulin dimer
                MT_stack = mrc_data[MT_start:MT_end:box_size, :]
                # performs a "Z-stack" according to the mean intensity in each pixel
                MT_stack_average = tf.reduce_mean(MT_stack, axis=0)
                # converts the tensorFlow tensor to numpy - this is the new mrc containing all the segments of a
                # specific MT according to its ID (rlnHelicalTubeID) in a mrcs file of extracted particles from relion
                MT_stack_average_array = MT_stack_average.numpy()

                # Saving the new mrc files (numpy matrix) using mrcfile library
                with mrcfile.new(f'{micrograph_stack_file}_MT_#{MT}.mrc', overwrite=True) as mrc:
                    # Write the NumPy array to the MRC file
                    mrc.set_data(MT_stack_average_array)
                print(f'Finished working on MT {MT} in {micrograph_stack_file} \n', '=' * 100)

    particles_star_file_data = starfile.read(particles_star_file.get())
    particles_dataframe = particles_star_file_data['particles']

    print(particles_dataframe['rlnImageName'])

    print("Processing complete.")
