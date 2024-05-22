"""
Author: Alina Levitin
Date: 15/04/24
Updated: 15/04/24

Methods for angles and shifts manipulation

shifts: _rlnAngleRot, _rlnOriginX, _rlnOriginY, _rlnOriginZ are set to 0
angles: _rlnAnglePsi, _rlnAngleTilt are set to priors: _rlnAnglePsiPrior, _rlnAngleTiltPrior

"""
import os

import starfile

from .method_base import MethodBase, print_done_decorator


class ResetAnglesAndShifts(MethodBase):

    def __init__(self, star_file_input, output_directory, rot=None, x=None, y=None, z=None, psi=None, tilt=None):
        self.star_file_input = star_file_input.get()
        self.star_file_name = os.path.basename(self.star_file_input)
        self.output_directory = output_directory
        self.rot = rot
        self.x = x
        self.y = y
        self.z = z
        self.psi = psi
        self.tilt = tilt

    @print_done_decorator
    def reset_angles_and_translations(self):
        # Read the STAR file and convert it to a pandas DataFrame
        data = starfile.read(self.star_file_input)

        particles_dataframe = data['particles']
        data_optics_dataframe = data['optics']

        name = []

        # Reset PHI/Rot to 0
        if self.rot == '0' and 'rlnAngleRot' in particles_dataframe.columns:
            particles_dataframe['rlnAngleRot'] = 0.0
            name.append('rot_0')

        # Reset PSI and TILT to match PRIORS (assuming the prior columns exist in the DataFrame)
        # Adjust column names according to the actual column names in the STAR file
        if self.psi == 'prior' and 'rlnAnglePsiPrior' in particles_dataframe.columns:
            particles_dataframe['rlnAnglePsi'] = particles_dataframe['rlnAnglePsiPrior']
            name.append('psi_prior')

        if self.tilt == 'prior' and 'rlnAngleTiltPrior' in particles_dataframe.columns:
            particles_dataframe['rlnAngleTilt'] = particles_dataframe['rlnAngleTiltPrior']
            name.append('tilt_prior')

        # Reset translations to 0
        if self.x == '0' and 'rlnOriginXAngst' in particles_dataframe.columns:
            particles_dataframe['rlnOriginXAngst'] = 0.0
            name.append('x_0')

        if self.y == '0' and 'rlnOriginYAngst' in particles_dataframe.columns:
            particles_dataframe['rlnOriginYAngst'] = 0.0
            name.append('y_0')

        if self.z == '0' and 'rlnOriginZ' in particles_dataframe.columns:
            particles_dataframe['rlnOriginZAngst'] = 0.0
            name.append('z_0')

        # Write the modified DataFrame back to a new STAR file
        os.chdir(self.output_directory)
        new_particles_star_file_data = {'optics': data_optics_dataframe, 'particles': particles_dataframe}
        new_star_file = self.star_file_name.replace('.star', f'{"_".join(name)}.star')
        starfile.write(new_particles_star_file_data, new_star_file)

        print(f"Updated STAR file saved as: {new_star_file} at {self.output_directory}")
