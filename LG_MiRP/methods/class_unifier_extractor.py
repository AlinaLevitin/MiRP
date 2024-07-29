"""
Author: Alina Levitin
Date: 14/03/24
Updated: 29/07/24

Method to unify classes by protofilament numbers or location of seam after 3D-classification
The method counts how many times each class was assigned to segments of the same MT and assign the most common class
to all the MT segments.
For protofilament number it then it separates the segments according to their class to STAR files using all the data
from run_it000_data.star file meaning it resets all the angles to prior.
For Seam-check it will generate a single file with unified class numbers incorporated in the run_itxx_data.star file
therefore will reset the angles and shifts to prior
"""
import os
import datetime

import starfile
import matplotlib.pyplot as plt

from ..methods_base.method_base import MethodBase, print_done_decorator
from ..methods_base.particles_starfile import ParticlesStarfile, groupby_micrograph_and_helical_id


class ClassUnifierExtractor(MethodBase):
    """

    """

    def __init__(self, star_file_input0, star_file_input1, output_path, cutoff, step):
        self.star_file_input0 = star_file_input0.get()
        self.star_file_input1 = star_file_input1.get()
        # Read data from "run_it000_data.star" using starfile
        data0 = ParticlesStarfile(self.star_file_input0)
        self.particles_dataframe0 = data0.particles_dataframe

        # Read data from "run_it0xx_data.star" using starfile
        data1 = ParticlesStarfile(self.star_file_input1)
        self.particles_dataframe1 = data1.particles_dataframe
        self.data_optics_dataframe1 = data1.optics_dataframe
        self.star_file_name = os.path.basename(self.star_file_input1)
        self.output_path = output_path.get()
        self.cutoff = float(cutoff.get())
        self.bad_mts = 0
        self.step = step

    @print_done_decorator
    def class_unifier_extractor(self):

        # Takes only the unique micrographs from the star file
        class_unified_particles_dataframe = self.unify_class_numbers()

        original_data_star_name = self.star_file_name.replace('.star', '')

        if self.step == 'pf_number_check':
            # EXTRACTING THE SEGMENTS TO SEPARATE STAR FILES ACCORDING TO THEIR CLASS
            number_of_classes = class_unified_particles_dataframe['rlnClassNumber'].unique().tolist()

            # Iterates over the number of classes
            for i in number_of_classes:

                # Filtering the datarfame for the specific class i
                mask_class = class_unified_particles_dataframe['rlnClassNumber'] == i
                class_particles = class_unified_particles_dataframe.loc[mask_class]

                total_MTs_of_class_i = len(groupby_micrograph_and_helical_id(class_particles))

                print(f"There are {total_MTs_of_class_i} MTs of class {i}")

                # Generating a new STAR file using the optics from run_it001_data.star and the new particles (segments)
                # data with corrected classes after unification

                new_particles_star_file_data = {'optics': self.data_optics_dataframe1, 'particles': class_particles}

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
            new_particles_star_file_data = {'optics': self.data_optics_dataframe1, 'particles': class_unified_particles_dataframe}

            os.chdir(self.output_path.get())
            output_file = f'{original_data_star_name}_class_corrected.star'
            try:
                starfile.write(new_particles_star_file_data, output_file)
                print(f'Saved STAR file {output_file} at {self.output_path.get()}')
            except NameError:
                print(f"File names {output_file} already exists, delete old file and try again")
                raise NameError("File already exists")

        self.generate_report(class_unified_particles_dataframe)

    def unify_class_numbers(self):
        """
        Finds the most common class for each MT and assigns it to all MT segments.
        Since it updates the run_it00_data.star with the most common classes from run_itxx_data.star file, this also
        resets all angles and shifts to prior

        :return: updated particles dataframe with original angles and shifts
        """
        # Group by 'rlnMicrographName' and 'rlnHelicalTubeID'
        grouped_data = groupby_micrograph_and_helical_id(self.particles_dataframe1)

        for (micrograph, MT), MT_dataframe in grouped_data:
            # Get the most common class number in the current MT segment
            most_common_class = MT_dataframe['rlnClassNumber'].mode().iloc[0]

            # Log the information
            number_of_appearances = MT_dataframe[MT_dataframe['rlnClassNumber'] == most_common_class].shape[0]
            total_number = len(MT_dataframe)
            proportion = number_of_appearances / total_number
            print(f'MT {MT} in {micrograph}:')
            print(f'The most common class is {most_common_class}')
            print(f'It appears {number_of_appearances} out of {total_number} times')
            print('=' * 100)

            # Apply the most common class number to all segments of the MT in the original dataframe
            if proportion >= self.cutoff:
                # Apply the most common class number to all segments of the MT in the original dataframe
                mask = (self.particles_dataframe0['rlnMicrographName'] == micrograph) & (
                        self.particles_dataframe0['rlnHelicalTubeID'] == MT)
                self.particles_dataframe0.loc[mask, 'rlnClassNumber'] = most_common_class
            else:
                # Discard the MT segments by removing them from the original dataframe
                mask = (self.particles_dataframe0['rlnMicrographName'] == micrograph) & (
                        self.particles_dataframe0['rlnHelicalTubeID'] == MT)
                self.particles_dataframe0 = self.particles_dataframe0[~mask]
                self.bad_mts += 1

        print(f"{self.bad_mts} out of {len(grouped_data)} MTs were omitted since they didn't meet the cutoff requirement")

        return self.particles_dataframe0

    @staticmethod
    def classes_distribution_fig(input_particles_dataframe):
        """
        A method to generate a histogram from number of segments per MT

        :return: matplotlib pie % fig
        """

        # Access the 'rlnClassNumber' column and get unique values
        classes_value_counts = input_particles_dataframe['rlnClassNumber'].value_counts()

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

    def generate_report(self, class_unified_particles_dataframe):
        """
        Generates a report file with details about the input files, date, optics dataframe, number of MTs, number of segments,
        distribution of the classes, the cutoff, and the MTs that didn't reach the cutoff.

        :param class_unified_particles_dataframe: Dataframe with unified class numbers
        """
        report_path = os.path.join(self.output_path, 'class_unification_report.txt')
        total_segments = len(class_unified_particles_dataframe)
        total_MTs = len(groupby_micrograph_and_helical_id(class_unified_particles_dataframe))
        total_MTs_before_cutoff = len(groupby_micrograph_and_helical_id(self.particles_dataframe1))

        with open(report_path, 'w') as report_file:
            report_file.write(f"Class Unification Report\n")
            report_file.write(f"Step: {self.step}\n")
            report_file.write(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            report_file.write(f"Input file 0: {self.star_file_input0}\n")
            report_file.write(f"Input file 1: {self.star_file_input1}\n")
            report_file.write(f"Output path: {self.output_path}\n")
            report_file.write(f"Cutoff: {self.cutoff}\n")
            report_file.write(f"Number of MTs (before cutoff): {total_MTs_before_cutoff}\n")
            report_file.write(f"Number of MTs (after cutoff): {total_MTs}\n")
            report_file.write(f"Number of segments: {total_segments}\n")
            report_file.write(f"Optics Dataframe:\n{self.data_optics_dataframe1.to_string()}\n\n")

            class_counts = class_unified_particles_dataframe['rlnClassNumber'].value_counts()
            report_file.write(f"Class Distribution:\n")
            for class_number, count in class_counts.items():
                mt_count = len(groupby_micrograph_and_helical_id(class_unified_particles_dataframe[
                                                                     class_unified_particles_dataframe[
                                                                         'rlnClassNumber'] == class_number]))
                report_file.write(f"Class {class_number}: {count} segments, {mt_count}/{total_MTs} MTs "
                                  f"[({round((mt_count/total_MTs)*100, 2)}]%)\n")

            report_file.write(f"\n{self.bad_mts} MTs out of {total_MTs_before_cutoff} total MTs "
                              f"did not meet the cutoff ({self.cutoff}):\n")
            for (micrograph, MT), MT_dataframe in groupby_micrograph_and_helical_id(self.particles_dataframe1):
                most_common_class = MT_dataframe['rlnClassNumber'].mode().iloc[0]
                number_of_appearances = MT_dataframe[MT_dataframe['rlnClassNumber'] == most_common_class].shape[0]
                total_number = len(MT_dataframe)
                proportion = number_of_appearances / total_number
                if proportion < self.cutoff:
                    report_file.write(f'MT {MT} in {micrograph} did not meet the cutoff with proportion {proportion}\n')

        print(f'Report generated at {report_path}')
