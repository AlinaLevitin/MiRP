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

from .method_base import MethodBase, print_done_decorator


class AnglesAndShiftsCorrection(MethodBase):

    def __init__(self, star_file_input, pf_number, output_directory):
        self.star_file_input = star_file_input.get()
        self.star_file_name = os.path.basename(self.star_file_input)
        self.pf_number = int(pf_number.get())
        self.output_directory = output_directory.get()

    @print_done_decorator
    def adjust_angles_and_translations(self):
        # Read the STAR file and convert it to a pandas DataFrame
        data = starfile.read(self.star_file_input)

        input_particles_dataframe = data['particles']
        particles_dataframe = pd.DataFrame()
        data_optics_dataframe = data['optics']

        pixel_size = float(data_optics_dataframe['rlnImagePixelSize'])

        # Calculate helical twist and rise
        helical_twist = 360 / self.pf_number
        helical_rise = (3 * 41) / self.pf_number

        for index, row in input_particles_dataframe.iterrows():
            if pd.isnull(row['rlnAnglePsi']):
                pass
            else:
                helical_shift = math.radians(row['rlnAnglePsi'])
                helical_rise_pixels = helical_rise / pixel_size
                helical_twist_radians = math.radians(helical_twist)

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

        return particles_dataframe, input_particles_dataframe
