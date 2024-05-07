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


def adjust_angles_and_translations(star_file_input, pf_number, output_directory):
    # Read the STAR file and convert it to a pandas DataFrame
    data = starfile.read(star_file_input.get())

    particles_dataframe = data['particles']
    data_optics_dataframe = data['optics']

    pixel_size = float(data_optics_dataframe['rlnImagePixelSize'])

    pf_number = int(pf_number.get())

    # Calculate helical twist and rise
    helical_twist = 360 / pf_number
    helical_rise = (3 * 41) / pf_number

    for index, row in particles_dataframe.iterrows():
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
    os.chdir(output_directory.get())
    new_particles_star_file_data = {'optics': data_optics_dataframe, 'particles': particles_dataframe}
    new_star_file = star_file_input.get().replace('.star', '_angles_shifts_corrected.star')
    starfile.write(new_particles_star_file_data, new_star_file)

    print(f"Updated STAR file saved as: {new_star_file} at {output_directory.get()}")

    return particles_dataframe
