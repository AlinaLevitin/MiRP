"""
Author: Alina Levitin
Date: 15/04/24
Updated: 15/04/24

Methods for angles and shifts manipulation

shifts: _rlnOriginX, _rlnOriginY, _rlnOriginZ are set to 0
(_rlnAngleRot is kept same)
angles: _rlnAnglePsi, _rlnAngleTilt are set to priors: _rlnAnglePsiPrior, _rlnAngleTiltPrior

"""
import os

import starfile


def keep_PHI_reset_angles_and_translations(star_file_input, output_directory):
    # Read the STAR file and convert it to a pandas DataFrame
    data = starfile.read(star_file_input.get())

    particles_dataframe = data['particles']
    data_optics_dataframe = data['optics']

    # Reset PHI to 0
    if '_rlnAnglePsiPrior' in particles_dataframe.columns and '_rlnAngleTiltPrior' in particles_dataframe.columns:
        particles_dataframe['_rlnAnglePsi'] = particles_dataframe['_rlnAnglePsiPrior']
        particles_dataframe['_rlnAngleTilt'] = particles_dataframe['_rlnAngleTiltPrior']

    # Reset translations to 0
    translation_columns = ['_rlnOriginX', '_rlnOriginY', '_rlnOriginZ']
    for col in translation_columns:
        if col in particles_dataframe.columns:
            particles_dataframe[col] = 0.0

    # Write the modified DataFrame back to a new STAR file
    os.chdir(output_directory.get())
    new_particles_star_file_data = {'optics': data_optics_dataframe, 'particles': particles_dataframe}
    new_star_file = star_file_input.get().replace('.star', '_keep_PHI_reset_shifts_angles_to_priors.star')
    starfile.write(new_particles_star_file_data, new_star_file)

    print(f"Updated STAR file saved as: {new_star_file} at {output_directory.get()}")
