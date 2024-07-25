"""
Author: Alina Levitin
Date: 15/04/24
Updated: 15/07/24

Methods for angles and shifts manipulation during initial seam assignment step

shifts: rlnOriginX, rlnOriginY, rlnOriginZ (I'm not sure if Z exists)
angles: rlnAngleRot, rlnAnglePsi, rlnAngleTilt

If set to 0 then the values are set to 0, if set to prior then are set to priors (rlnAnglePsiPrior, rlnAngleTiltPrior)
if none, then untouched.

"""
import os

import starfile

from .method_base import MethodBase, print_done_decorator


class ResetAnglesAndShifts(MethodBase):
    """
        Method inherits from MethodBase class in method_base.py
    """

    def __init__(self, star_file_input, output_directory):
        """
        Takes the star_file_input and resets rot (rlnAngleRot), x (rlnOriginX), y (rlnOriginY) and z (rlnOriginZ), and
        sets psi (rlnAnglePsi) and tilt (rlnAngleTilt) to prior (rlnAnglePsiPrior and rlnAngleTiltPrior accordingly)
        then generates an output star file ot output_directory

        :param star_file_input: star file
        :param output_directory: output path
        """
        self.star_file_input = star_file_input.get()
        self.star_file_name = os.path.basename(self.star_file_input)
        self.output_directory = output_directory.get()

    @print_done_decorator
    def reset_angles_and_translations(self, rot=None, x=None, y=None, z=None, psi=None, tilt=None):
        """
        Takes the star_file_input and resets rot (rlnAngleRot), x (rlnOriginX), y (rlnOriginY) and z (rlnOriginZ), and
        sets psi (rlnAnglePsi) and tilt (rlnAngleTilt) to prior (rlnAnglePsiPrior and rlnAngleTiltPrior accordingly)
        then generates an output star file ot output_directory

        :param x: 0 or None
        :param y: 0 or None
        :param z: 0 or None
        :param rot: 0 or None
        :param psi: prior or None
        :param tilt: prior or None
        """
        x = x.get()
        y = y.get()
        z = z.get()
        rot = rot.get()
        psi = psi.get()
        tilt = tilt.get()

        print(f"Initiating angels and shifts reset\n"
              f"Parameters:"
              f"rlnOriginXAngst = {x}\n"
              f"rlnOriginYAngst = {y}\n"
              f"rlnOriginZ = {z}\n"
              f"rlnAngleRot = {rot}\n"
              f"rlnAngleTilt = {tilt}\n"
              f"rlnAnglePsi = {psi}")

        # Read the STAR file and convert it to a pandas DataFrame
        data = starfile.read(self.star_file_input)

        particles_dataframe = data['particles']
        data_optics_dataframe = data['optics']

        # Set an empty list to use as parameters in the name of the final star file
        name = []

        # Reset PHI/Rot to 0
        if rot == '0' and 'rlnAngleRot' in particles_dataframe.columns:
            particles_dataframe['rlnAngleRot'] = 0.0
            name.append('rot_0')

        # Reset PSI and TILT to match PRIORS (assuming the prior columns exist in the DataFrame)
        # Adjust column names according to the actual column names in the STAR file
        if psi == 'prior' and 'rlnAnglePsiPrior' in particles_dataframe.columns:
            particles_dataframe['rlnAnglePsi'] = particles_dataframe['rlnAnglePsiPrior']
            name.append('psi_prior')
        elif 'rlnAnglePsiPrior' not in particles_dataframe.columns:
            print("There is no rlnAnglePsiPrior in the star file")

        if tilt == 'prior' and 'rlnAngleTiltPrior' in particles_dataframe.columns:
            particles_dataframe['rlnAngleTilt'] = particles_dataframe['rlnAngleTiltPrior']
            name.append('tilt_prior')
        elif 'rlnAngleTiltPrior' not in particles_dataframe.columns:
            print("There is no rlnAngleTiltPrior in the star file")

        # Reset translations to 0
        if x == '0' and 'rlnOriginXAngst' in particles_dataframe.columns:
            particles_dataframe['rlnOriginXAngst'] = 0.0
            name.append('x_0')
        elif 'rlnOriginXAngst' not in particles_dataframe.columns:
            print("There is no rlnOriginXAngst in the star file")

        if y == '0' and 'rlnOriginYAngst' in particles_dataframe.columns:
            particles_dataframe['rlnOriginYAngst'] = 0.0
            name.append('y_0')
        elif 'rlnOriginYAngst' not in particles_dataframe.columns:
            print("There is no rlnOriginYAngst in the star file")

        if z == '0' and 'rlnOriginZ' in particles_dataframe.columns:
            particles_dataframe['rlnOriginZAngst'] = 0.0
            name.append('z_0')
        elif 'rlnOriginZ' not in particles_dataframe.columns:
            print("There is no rlnOriginZ in the star file")

        # Write the modified DataFrame back to a new STAR file
        os.chdir(self.output_directory)
        new_particles_star_file_data = {'optics': data_optics_dataframe, 'particles': particles_dataframe}
        new_star_file = self.star_file_name.replace('.star', f'_{"_".join(name)}.star')
        starfile.write(new_particles_star_file_data, new_star_file)

        print(f"Updated STAR file saved as: {new_star_file} at {self.output_directory}")
