import os

import pandas as pd
import starfile


def extract_most_likely_classes(input_directory, output_directory):

    input_path = input_directory.get()
    output_path = os.path.join(output_directory.get(), "class_extraction")

    if "segment_averages" not in os.listdir(output_directory.get()):
        os.mkdir(output_path)

    # Read input star files
    input_star_file_prior_path = os.path.join(input_path, 'run_it000_data.star')
    input_star_data_prior = starfile.read(input_star_file_prior_path)

    input_star_file_classes_path = os.path.join(input_path, 'run_it001_data.star')
    input_star_data_classes = starfile.read(input_star_file_classes_path)

    # Filter rows containing '.mrc' in 'rlnImageName'
    input_star_data = input_star_data[input_star_data['rlnImageName'].str.contains('.mrcs')]
    corrected_class_3D_star_data = corrected_class_3D_star_data[corrected_class_3D_star_data['rlnImageName'].str.contains('.mrc')]

    # Extract individual star files for different PF numbers and reset all columns except 3D class
    for pf_number in range(11, 17):
        # Filter rows based on PF number
        pf_data = corrected_class_3D_star_data[corrected_class_3D_star_data['rlnClassNumber'] == pf_number]

        # Output file name
        pf_class_star_file = f'{class_3D_star_file}_r_{pf_number}pf_class.star'

        # Write filtered data to output file
        starfile.write(pf_data, pf_class_star_file)

        print(f'Star files generated for {pf_number}pf class:')
        print(pf_class_star_file)
        print(len(pf_data))

# # Example usage:
# input_star_file = 'run_it000_data.star'
# class_3D_star_file = 'run_it001_data.star'
# corrected_class_3D_star_file = 'run_it001_data_corrected01.star'
# extract_most_likely_classes(input_star_file, class_3D_star_file, corrected_class_3D_star_file)
