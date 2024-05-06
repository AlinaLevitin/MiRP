"""
Author: Alina Levitin
Date: 14/03/24
Updated: 02/04/24

Method to unify classes by protofilament numbers after 3D-classification
The method counts how many times each class was assigned to segments of the same MT and assign the most common class
to all the MT segments.
Then it separates the segments according to their class to STAR files using all the data from run_it000_data.star file
meaning it resets all the angles to prior
"""
import os

import starfile
import matplotlib.pyplot as plt


def class_unifier_extractor(star_file_input0, star_file_input1, output_path, step):

    # Read data from "run_it000_data.star" using starfile
    data0 = starfile.read(star_file_input0.get())
    particles_dataframe0 = data0['particles']

    # Read data from "run_it001_data.star" using starfile
    data1 = starfile.read(star_file_input1.get())
    particles_dataframe1 = data1['particles']
    data_optics_dataframe1 = data1['optics']

    # Takes only the unique micrographs from the star file
    micrographs = particles_dataframe1['rlnMicrographName'].unique()

    # Iterates over the micrographs
    for micrograph in micrographs:
        # Filters the dataframe according to the micrograph name
        mask = particles_dataframe1['rlnMicrographName'] == micrograph
        micrograph_star = particles_dataframe1.loc[mask]
        # Fines the number of MTs in the micrograph
        total_number_of_mts = micrograph_star['rlnHelicalTubeID'].max()
        print(f'{micrograph} contains {total_number_of_mts} MTs')

        # Iterates over the MTs in the micrograph
        for MT in range(1, total_number_of_mts + 1):
            # creating a mask to filter only the micrographs for the id of the MT
            mask2 = micrograph_star['rlnHelicalTubeID'] == MT
            MT_star_data = micrograph_star.loc[mask2]

            # Some MTs are missing so to avoid errors we continue only with MTs with data
            if not MT_star_data.empty:

                # Counts how many segments were classified as a specific class
                classes = MT_star_data['rlnClassNumber'].value_counts()

                # Takes the class that appeared the most times
                most_common_class = classes.idxmax()

                # Number of segments classified at this class
                number_of_appearances = classes.max()

                # Total number of segments
                total_number = classes.shape[0]

                print(f'For MT {MT}, the most common class is {most_common_class} It appears {number_of_appearances}'
                      f'out of {total_number} times\n', '=' * 100)

                # Iterates over the entire original dataframe and replacing the class with the most common class
                # for all segments of the MT in the micrograph using all other data from run_it000_data.star
                # This resets the angles to prior
                for index, row in particles_dataframe0.iterrows():
                    if micrograph in row['rlnMicrographName'] and row['rlnHelicalTubeID'] == MT:
                        particles_dataframe0.loc[index, 'rlnClassNumber'] = most_common_class

    original_data_star_name = star_file_input1.get()

    # EXTRACTING THE SEGMENTS TO SEPARATE STAR FILES ACCORDING TO THEIR CLASS

    number_of_classes = particles_dataframe1['rlnClassNumber'].max()
    # TODO: add if step=seam_check(one star) or pf_number(seperate)
    # Iterates over the number of classes
    for i in range(number_of_classes + 1):

        # Filtering the datarfame for the specific class i
        mask_class = particles_dataframe0['rlnClassNumber'] == i
        class_particles = particles_dataframe0.loc[mask_class]

        print(f"There are {class_particles.shape[0]} segments of class {i}")

        # Generating a new STAR file using the optics from run_it001_data.star and the new particels (segments) data
        # with corrected classes after unification

        new_particles_star_file_data = {'optics': data_optics_dataframe1, 'particles': class_particles}

        os.chdir(output_path.get())
        output_file = f'{original_data_star_name}_class_{i}.star'
        try:
            starfile.write(new_particles_star_file_data, output_file)
            print(f'Saved STAR file {output_file} at {output_path.get()}')
        except NameError:
            print(f"File names {output_file} already exists, delete old file and try again")
            raise NameError("File already exists")


def classes_distribution(star_file_input):
    """
    A method to generate a histogram from number of segments per MT

    :param star_file_input: particles star file from entry
    :return: matplotlib pie % fig
    """

    try:
        # Try to read the STAR file
        particles_star_file_data = starfile.read(star_file_input.get())
        particles_dataframe = particles_star_file_data['particles']

        # Access the 'rlnClassNumber' column and get unique values
        classes_value_counts = particles_dataframe['rlnClassNumber'].value_counts()

    except FileNotFoundError:
        # Handle the case where the specified STAR file does not exist
        print("Error: The specified STAR file does not exist.")
        # Optionally, you can raise the error again if needed
        raise

    # The classes and the nuber of their appearances (values)
    classes = classes_value_counts.index
    values = classes_value_counts.values

    # Create a Matplotlib figure and axes
    fig, ax = plt.subplots()

    # Plot pie chart
    ax.pie(values, labels=classes, autopct='%1.1f%%', startangle=140)

    # Add labels and title
    ax.set_xlabel('Classes %')
    ax.set_title('Class distribution')

    return fig
