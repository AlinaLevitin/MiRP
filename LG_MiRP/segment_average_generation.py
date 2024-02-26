import os
import tensorflow as tf
# import tensorflow_io as tfio
import starfile
import mrcfile
import pandas as pd

def preprocess_segment_averages(directory, box_size: int=58):
    # Calculate background radius box for normalization
    background_box_radius = 0.75 * box_size / 2

    path = directory.get()

    # Iterate over each micrograph stack in the directory
    for micrograph_stack_file in os.listdir(path):
        if micrograph_stack_file.endswith(".mrcs"):
            micrograph_stack_path = os.path.join(path, micrograph_stack_file)
            with mrcfile.open(micrograph_stack_path) as mrc:
                # Assuming it's a 3D volume, you can adjust the axis if it's different
                mrc_data = tf.convert_to_tensor(mrc.data, dtype=tf.float32)
            print('Working on', micrograph_stack_file)

            # Work out number of segments in stack from .star file
            star_file_path = micrograph_stack_path.replace(".mrcs", "_extract.star")
            star_data = starfile.read(star_file_path)
            number_of_MTs_in_stack = star_data['rlnHelicalTubeID'].max()
            print(f'{micrograph_stack_file} contains {number_of_MTs_in_stack} MTs')
            for MT in range(1, number_of_MTs_in_stack + 1):
                mask = star_data['rlnHelicalTubeID'] == MT
                MT_star_data = star_data.loc[mask]
                MT_number_of_segments = MT_star_data.shape[0]
                MT_start = MT_star_data.index[0]
                MT_end = MT_star_data.index[-1]
                print(f'MT number {MT} in {micrograph_stack_file} contains {MT_number_of_segments} number of segments'
                      f' from {MT_start} to {MT_end}')
                MT_stack = mrc_data[MT_start:MT_end:box_size, :]
                MT_stack_average = tf.reduce_mean(MT_stack, axis=0)
                MT_stack_average_array = MT_stack_average.numpy()

                with mrcfile.new('output.mrc', overwrite=True) as mrc:
                    # Write the NumPy array to the MRC file
                    mrc.set_data(MT_stack_average_array)

                print(f'Finished working on MT {MT} in {micrograph_stack_file} \n', '='*100)



    print("Processing complete.")

