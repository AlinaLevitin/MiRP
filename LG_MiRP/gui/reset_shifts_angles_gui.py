"""
Author: Alina Levitin
Date: 15/04/24
Updated: 17/07/24

Two GUI classes (master and frame) for shifts and angle reset
The method of shifts and angle reset is in and extraction is located in LG_MiRP/methods/reset_angles_shifts

shifts: _rlnAngleRot, _rlnOriginX, _rlnOriginY, _rlnOriginZ are set to 0
angles: _rlnAnglePsi, _rlnAngleTilt are set to priors: _rlnAnglePsiPrior, _rlnAngleTiltPrior
"""
from ..gui_base import LgFrameBase, LgMasterGui, check_parameters
from ..methods import ResetAnglesAndShifts
from ..methods_base import ParticlesStarfile


class ResetShiftsAnglesGui(LgMasterGui):
    """
    Inherits from LgMasterGui
    """
    def __init__(self, name):
        super().__init__(name)
        frame = ResetShiftsAnglesFrame(self)
        frame.grid(row=1, column=0, sticky="NSEW")
        self.mainloop()


class ResetShiftsAnglesFrame(LgFrameBase):
    """
    Inherits from LgFrameBase
    """
    def __init__(self, master):
        """
        :param master: the master gui in which the frame will be displayed
        """
        super().__init__(master)

        self.add_sub_job_name("Reset shifts and angles to 0/prior")

        # Creates an entry for run_it000_data.star file
        self.input_star_file = self.add_file_entry('star', 'Select a run_it0xx_data.star file', row=1)

        # Setting up dropdown menus for shits and angles
        shifts_rot_options = ['0', None]
        angles_options = ['prior', None]

        self.x = self.add_method_combobox(row=2, options=shifts_rot_options, text='Manipulation to x (rlnOriginXAngst)')
        self.y = self.add_method_combobox(row=3, options=shifts_rot_options, text='Manipulation to y (rlnOriginYAngst)')
        self.z = self.add_method_combobox(row=4, options=shifts_rot_options, text='Manipulation to z (rlnOriginZ)')
        self.rot = self.add_method_combobox(row=5, options=shifts_rot_options, text='Manipulation to rot (rlnAngleRot)')
        self.tilt = self.add_method_combobox(row=6, options=angles_options, text='Manipulation to rot (rlnAngleTilt)')
        self.psi = self.add_method_combobox(row=7, options=angles_options, text='Manipulation to rot (rlnAnglePsi)')

        # Creates an entry for output directory
        self.output_directory = self.add_directory_entry('Select output directory', row=8)

        # Creates a "Run" button that uses the class unification and extraction method
        self.add_run_button(row=9)

        self.result_number = self.add_number_entry(entry_name='Results to show (random):', row=10, default_value=10)
        self.add_show_results_button(self.show_plots, row=10, text="Show results")

        # Imports a themed image at the bottom
        self.add_image(new_size=600, row=11)

    @check_parameters(['input_star_file', 'output_directory', 'rot', 'x', 'y', 'z', 'psi', 'tilt'])
    def run_function(self):
        """
        Setting up the class, checking if the parameters are all filled (prints in the terminal if something is missing)
        and running the function with the parameters
        """
        function = ResetAnglesAndShifts(self.input_star_file, self.output_directory)
        self.input, self.output = function.reset_angles_and_translations(rot=self.rot,
                                                                         x=self.x,
                                                                         y=self.y,
                                                                         z=self.z,
                                                                         psi=self.psi,
                                                                         tilt=self.tilt)

    def show_plots(self):

        if not self.input_star_file.get():
            print('No star file was chosen, please select a run_it0xx_data.star file')
        elif self.output.empty:
            print('Showing input only')
            input_starfile = ParticlesStarfile(self.input_star_file.get())
            self.input = input_starfile.particles_dataframe
            self.show_input_angle_and_shifts_plot(int(self.result_number.get()))
        else:
            print('Showing input and output')
            self.show_angle_and_shifts_plot(int(self.result_number.get()))