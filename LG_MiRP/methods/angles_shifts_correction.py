"""
Author: Alina Levitin
Date: 15/04/24
Updated: 15/04/24

Methods for angles and shifts correction before high resolution reconstruction

"""

import os
import math
import pandas as pd
import starfile

from ..methods_base.method_base import MethodBase, print_done_decorator
from ..methods_base.particles_starfile import ParticlesStarfile


class AnglesAndShiftsCorrection(MethodBase):
    """
    Inherits from MethodBase class in method_base_py
    """

    def __init__(self, star_file_input, pf_number, output_directory):
        """
        Reads the star_file_input then corrects the angles according to the pf_number and creates an output star file at
        the output_directory path

        :param star_file_input: star file after 3D classification when checking the seam (seam_check)
        :param pf_number: number of protofilaments (used to calculate twist and rise)
        :param output_directory: output path for output star file
        """
        self.star_file_input = star_file_input.get()
        self.star_file_name = os.path.basename(self.star_file_input)
        self.pf_number = int(pf_number.get())
        self.output_directory = output_directory.get()

    @print_done_decorator
    def adjust_angles_and_translations(self):
        """
        Corrects the angles and translations of the particles according to their class number and saves the corrected
        star file at the output path

        :return: original dataframe and corrected dataframe
        """

        # Getting the optics and particles data blocks
        file = ParticlesStarfile(self.star_file_input)

        particles_dataframe = file.particles_dataframe
        data_optics_dataframe = file.optics_dataframe

        # Getting the pixel size from the optics data block
        pixel_size = file.pixel_size

        # Calculate helical twist and rise
        helical_twist = 360 / self.pf_number
        helical_rise = (3 * 41) / self.pf_number

        # iterates over the rows in the particles data block
        for index, row in particles_dataframe.iterrows():
            # Skipped row that don't have rlnAnglePsi
            if pd.isnull(row['rlnAnglePsi']):
                print('No angels to correct!')
                pass
            else:
                helical_shift = math.radians(row['rlnAnglePsi'])
                helical_rise_pixels = helical_rise / pixel_size

                if row['rlnClassNumber'] in range(1, 14):
                    new_x = row['rlnOriginXAngst'] + math.cos(-helical_shift) * (row['rlnClassNumber'] * helical_rise_pixels)
                    new_y = row['rlnOriginYAngst'] + math.sin(-helical_shift) * (row['rlnClassNumber'] * helical_rise_pixels)
                    new_phi = row['rlnAngleRot'] + helical_twist

                elif row['rlnClassNumber'] == 14:
                    new_x = row['rlnOriginXAngst'] + -41 * math.cos(-helical_shift) * (row['rlnClassNumber'] * helical_rise_pixels)
                    new_y = row['rlnOriginYAngst'] + -41 * math.sin(-helical_shift) * (row['rlnClassNumber'] * helical_rise_pixels)
                    new_phi = row['rlnAngleRot']

                else:
                    new_x = row['rlnOriginXAngst'] + -41 * math.cos(-helical_shift) + math.cos(-helical_shift) * (row['rlnClassNumber'] * helical_rise_pixels)
                    new_y = row['rlnOriginYAngst'] + -41 * math.sin(-helical_shift) + math.sin(-helical_shift) * (row['rlnClassNumber'] * helical_rise_pixels)
                    new_phi = row['rlnAngleRot'] + helical_twist

                # Update the DataFrame with adjusted coordinates
                particles_dataframe.loc[index, 'rlnOriginXAngst'] = new_x
                particles_dataframe.loc[index, 'rlnOriginYAngst'] = new_y
                particles_dataframe.loc[index, 'rlnAngleRot'] = new_phi

        # Write the modified DataFrame back to a new STAR file
        os.makedirs(self.output_directory, exist_ok=True)
        os.chdir(self.output_directory)
        new_particles_star_file_data = {'optics': data_optics_dataframe, 'particles': particles_dataframe}
        new_star_file = self.star_file_name.replace('.star', '_angles_shifts_corrected.star')
        starfile.write(new_particles_star_file_data, new_star_file)

        print(f"Updated STAR file saved as: {new_star_file} at {self.output_directory}")

        return ParticlesStarfile(self.star_file_input).particles_dataframe, particles_dataframe
