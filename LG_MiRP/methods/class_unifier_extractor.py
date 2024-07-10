"""
Author: Alina Levitin
Date: 14/03/24
Updated: 02/04/24

Method to unify classes by protofilament numbers or location of seam after 3D-classification
The method counts how many times each class was assigned to segments of the same MT and assign the most common class
to all the MT segments.
For protofilament number it then it separates the segments according to their class to STAR files using all the data
from run_it000_data.star file meaning it resets all the angles to prior
"""
import os

import starfile
import matplotlib.pyplot as plt
from .method_base import MethodBase, print_done_decorator


class ClassUnifierExtractor(MethodBase):

    def __init__(self, star_file_input0, star_file_input1, output_path, step):
        self.star_file_input0 = star_file_input0.get()
        self.star_file_input1 = star_file_input1.get()
        self.star_file_name = os.path.basename(self.star_file_input1)
        self.output_path = output_path.get()
        self.step = step

    @print_done_decorator
    def class_unifier_extractor(self):

        # Read data from "run_it000_data.star" using starfile
        data0 = starfile.read(self.star_file_input0)
        particles_dataframe0 = data0['particles']

        # Read data from "run_it0xx_data.star" using starfile
        data1 = starfile.read(self.star_file_input1)
        particles_dataframe1 = data1['particles']
        data_optics_dataframe1 = data1['optics']

        # Takes only the unique micrographs from the star file
        class_unified_particles_dataframe = self.update_class_numbers(particles_dataframe0, particles_dataframe1)

        original_data_star_name = self.star_file_name.replace('.star', '')

        if self.step == 'pf_number_check':
            # EXTRACTING THE SEGMENTS TO SEPARATE STAR FILES ACCORDING TO THEIR CLASS
            number_of_classes = class_unified_particles_dataframe['rlnClassNumber'].unique().tolist()

            # Iterates over the number of classes
            for i in number_of_classes:

                # Filtering the datarfame for the specific class i
                mask_class = class_unified_particles_dataframe['rlnClassNumber'] == i
                class_particles = class_unified_particles_dataframe.loc[mask_class]

                print(f"There are {class_particles.shape[0]} segments of class {i}")

                # Generating a new STAR file using the optics from run_it001_data.star and the new particels (segments)
                # data with corrected classes after unification

                new_particles_star_file_data = {'optics': data_optics_dataframe1, 'particles': class_particles}

                os.chdir(self.output_path)
                output_file = f'{original_data_star_name}_class_{i}.star'
                try:
                    starfile.write(new_particles_star_file_data, output_file)
                    print(f'Saved STAR file {output_file} at {self.output_path}')
                except NameError:
                    print(f"File names {output_file} already exists, delete old file and try again")
                    raise NameError("File already exists")

        elif self.step == 'seam_check':
            # EXTRACTING THE SEGMENTS TO A SINGLE STAR FILES WITH CORRECTED CLASSES
            new_particles_star_file_data = {'optics': data_optics_dataframe1, 'particles': class_unified_particles_dataframe}

            os.chdir(self.output_path.get())
            output_file = f'{original_data_star_name}_class_corrected.star'
            try:
                starfile.write(new_particles_star_file_data, output_file)
                print(f'Saved STAR file {output_file} at {self.output_path.get()}')
            except NameError:
                print(f"File names {output_file} already exists, delete old file and try again")
                raise NameError("File already exists")

    @staticmethod
    def update_class_numbers(particles_dataframe0, particles_dataframe1):
        """
        Finds the most common class for each MT and assigns it to all MT segments.
        Since it updates the it00_data.star with the most common classes from itxx_data.star file, this also resets all
        angles and shifts to prior

        :param particles_dataframe0: particles dataframe from it00_data.star file
        :param particles_dataframe1: particles dataframe from itxx_data.star file

        :return: updated particles dataframe with original angles and shifts
        """
        # Group by 'rlnMicrographName' and 'rlnHelicalTubeID'
        grouped_data = particles_dataframe1.groupby(['rlnMicrographName', 'rlnHelicalTubeID'])

        for (micrograph, MT), MT_dataframe in grouped_data:
            # Get the most common class number in the current MT segment
            most_common_class = MT_dataframe['rlnClassNumber'].mode().iloc[0]

            # Log the information
            number_of_appearances = MT_dataframe[MT_dataframe['rlnClassNumber'] == most_common_class].shape[0]
            total_number = len(MT_dataframe)
            print(f'MT {MT} in {micrograph}:')
            print(f'The most common class is {most_common_class}')
            print(f'It appears {number_of_appearances} out of {total_number} times')
            print('=' * 100)

            # Apply the most common class number to all segments of the MT in the original dataframe
            mask = (particles_dataframe0['rlnMicrographName'] == micrograph) & (
                    particles_dataframe0['rlnHelicalTubeID'] == MT)
            particles_dataframe0.loc[mask, 'rlnClassNumber'] = most_common_class

        return particles_dataframe0

    @staticmethod
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
