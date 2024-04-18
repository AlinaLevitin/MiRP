"""
Author: Alina Levitin
Date: 15/04/24
Updated: 15/04/24

Methods for angles and shifts correction before high resolution reconstruction

"""

import os
import math
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

    # Iterate through each particle and adjust angles and translations
    for index, row in particles_dataframe.iterrows():
        class_assignment = int(row.get('rlnClassNumber', 0))

        if 2 <= class_assignment <= 19:
            rise = class_assignment - 1
            phi = row.get('rlnAngleRot', 0) + rise * helical_twist
            cos_val = math.cos(math.radians(-phi))
            sin_val = math.sin(math.radians(-phi))

            # Calculate and adjust translations
            row['rlnOriginXAngst'] += cos_val * rise * helical_rise / pixel_size
            row['rlnOriginYAngst'] += sin_val * rise * helical_rise / pixel_size
            row['rlnAngleRot'] = phi

    # Write the modified DataFrame back to a new STAR file
    os.chdir(output_directory.get())
    new_particles_star_file_data = {'optics': data_optics_dataframe, 'particles': particles_dataframe}
    new_star_file = star_file_input.get().replace('.star', '_angles_shifts_corrected.star')
    starfile.write(new_particles_star_file_data, new_star_file)

    print(f"Updated STAR file saved as: {new_star_file} at {output_directory.get()}")

    return particles_dataframe
