"""
Author: Alina Levitin
Date: 15/04/24
Updated: 15/04/24

Two GUI classes (master and frame) for shifts and angle reset
The method of shifts and angle reset is in and extraction is located in LG_MiRP/methods/reset_angles_shifts

shifts: _rlnAngleRot, _rlnOriginX, _rlnOriginY, _rlnOriginZ are set to 0
angles: _rlnAnglePsi, _rlnAngleTilt are set to priors: _rlnAnglePsiPrior, _rlnAngleTiltPrior
"""
from ..gui_base import LgFrameBase, LgMasterGui
from ..methods import reset_angles_and_translations


class ResetShiftsAnglesGui(LgMasterGui):
    """
    ...
    Inherits from LgMasterGui
    """
    def __init__(self):
        super().__init__()
        self.add_job_name("Reset shifts to 0 and angles to prior")
        frame = ResetShiftsAnglesFrame(self)
        frame.grid(row=1, column=0, sticky="NSEW")
        self.mainloop()


class ResetShiftsAnglesFrame(LgFrameBase):
    """
    ...
    Inherits from LgFrameBase
    """
    def __init__(self, master):
        """
        :param master: the master gui in which the frame will be displayed
        """
        super().__init__(master)
        # Creates an entry for run_it000_data.star file
        input_star_file = self.add_file_entry('star', 'Select a run_it001_data.star file', row=1)

        # Creates an entry for output directory
        output_directory = self.add_directory_entry('Select output directory', row=2)

        # Creates a "Run" button that uses the class unification and extraction method
        self.add_run_button(lambda: reset_angles_and_translations(input_star_file, output_directory),
                            row=3)

        # Imports a themed image at the bottom
        self.add_image(new_size=600, row=4)
