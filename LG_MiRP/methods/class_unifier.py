"""
Author: Alina Levitin
Date: 14/03/24
Updated: 31/3/24

Method to unify classes by protofilament numbers after 3D-classification
The method counts how many times each class was assigned to segments of the same MT and assign the most common class
to all the MT segments
"""
import os

import starfile
import matplotlib.pyplot as plt


def class_unifier(star_file_input, output_path):

    # Read data from "run_it001_data.star" using starfile

    data = starfile.read(star_file_input.get())
    particles_dataframe = data['particles']
    data_optics_dataframe = data['optics']

    micrographs = particles_dataframe['rlnMicrographName'].unique()

    for micrograph in micrographs:
        mask = particles_dataframe['rlnMicrographName'] == micrograph
        micrograph_star = particles_dataframe.loc[mask]
        total_number_of_mts = micrograph_star['rlnHelicalTubeID'].max()
        print(f'{micrograph} contains {total_number_of_mts} MTs')

        for MT in range(1, total_number_of_mts + 1):
            # creating a mask to filter only the micrographs for the id of the MT
            mask2 = micrograph_star['rlnHelicalTubeID'] == MT
            MT_star_data = micrograph_star.loc[mask2]

            if not MT_star_data.empty:

                most_common_class = MT_star_data['rlnClassNumber'].value_counts().idxmax()

                number_of_appearances = MT_star_data['rlnClassNumber'].value_counts().max()

                print(f'For MT {MT}, the most common class is {most_common_class} It appears {number_of_appearances} times\n', '=' * 100)

                for index, row in particles_dataframe.iterrows():
                    if micrograph in row['rlnMicrographName'] and MT == row['rlnHelicalTubeID']:
                        particles_dataframe.loc[index, 'rlnClassNumber'] = most_common_class

    new_particles_star_file_data = {'optics': data_optics_dataframe, 'particles': particles_dataframe}

    os.chdir(output_path.get())
    output_file = 'run_it001_data_most_common_class.star'
    try:
        starfile.write(new_particles_star_file_data, output_file)
        print(f'Saved STAR file run_it001_data_most_common_class at {output_path.get()}')
    except NameError:
        print(f"File names {output_file} already exists, delete old file and try again")
        raise NameError("File already exists")


def classes_distribution(star_file_input):
    """
    A method to generate a histogram from number of segments per MT

    :param star_file_input: particles star file from entry
    :return: matplotlib histogram fig
    """

    try:
        # Try to read the STAR file
        particles_star_file_data = starfile.read(star_file_input.get())
        particles_dataframe = particles_star_file_data['particles']

        # Access the 'rlnMicrographName' column and get unique values
        classes_value_counts = particles_dataframe['rlnClassNumber'].value_counts()

        # Continue with further processing
        # ...

    except FileNotFoundError:
        # Handle the case where the specified STAR file does not exist
        print("Error: The specified STAR file does not exist.")
        # Optionally, you can raise the error again if needed
        raise

    classes = classes_value_counts.index
    values = classes_value_counts.values

    # # Create a Matplotlib figure and axes
    fig, ax = plt.subplots()

    ax.pie(values, labels=classes, autopct='%1.1f%%', startangle=140)
    #
    # Plot pie chart

    # Add labels and title
    ax.set_xlabel('%')
    ax.set_ylabel('Classes')
    ax.set_title('Class distribution')
    #
    return fig
