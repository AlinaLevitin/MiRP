"""
Author: Alina Levitin
Date: 17/04/24
Updated: 18/04/24

Two GUI classes (master and frame) to correct PHI/Rot and shifts
The method of angle smoothing is in and extraction is located in LG_MiRP/methods/angle_shifts_correction

"""
from ..gui_base import LgFrameBase, LgMasterGui
from ..methods import AnglesAndShiftsCorrection


class AngleShiftsCorrectionGui(LgMasterGui):
    """
    ...
    Inherits from LgMasterGui
    """

    def __init__(self):
        super().__init__()
        self.add_job_name("angles and shifts correction")
        frame = AngleShiftsCorrectionFrame(self)
        frame.grid(row=1, column=0, sticky="NSEW")
        self.mainloop()


class AngleShiftsCorrectionFrame(LgFrameBase):
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
        self.star_file_input = self.add_file_entry('star', 'Select a run_it0xx_data_class_corrected.star file', row=1)

        # Creates an entry for output directory
        self.output_path = self.add_directory_entry('Select output directory', row=2)

        self.pf_number = self.add_number_entry("Number of proto-filaments", row=3)

        self.add_run_button(self.run_function, row=4)

        result_number = self.add_number_entry(entry_name='Results to show (random):', row=5, default_value=10)
        self.add_show_results_button(lambda: self.show_result(int(result_number.get())), row=5, text="Show results")

        # Imports a themed image at the bottom
        self.add_image(image_name="angles_and_shifts_correction.jpg", new_size=600, row=6)

    def run_function(self):
        function = AnglesAndShiftsCorrection(self.star_file_input, self.pf_number, self.output_path)
        self.output = function.adjust_angles_and_translations()
