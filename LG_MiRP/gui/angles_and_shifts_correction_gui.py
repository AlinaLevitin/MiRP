"""
Author: Alina Levitin
Date: 17/04/24
Updated: 17/07/24

Two GUI classes (master and frame) to correct PHI/Rot and shifts
The method of angle smoothing is in and extraction is located in LG_MiRP/methods/angle_shifts_correction

"""
from ..gui_base import LgFrameBase, LgMasterGui, check_parameters
from ..methods import AnglesAndShiftsCorrection


class AngleShiftsCorrectionGui(LgMasterGui):
    """
    Inherits from LgMasterGui in master_gui.py
    """

    def __init__(self, name):
        super().__init__(name)
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

        # Adding a title label
        self.add_sub_job_name("angles and shifts correction")

        # Creates an entry for run_it000_data.star file
        self.input_star_file = self.add_file_entry('star', 'Select a run_it0xx_data_class_corrected.star file', row=1)

        # Creates an entry for output directory
        self.output_directory = self.add_directory_entry('Select output directory', row=2)

        # Adding a number entry for protofilament number
        self.pf_number = self.add_number_entry("Number of proto-filaments", row=3)

        # Adding a "Run" button that runs self.run_function
        self.add_run_button(row=4)

        # Adding a number entry for number of results to show, default is 10
        result_number = self.add_number_entry(entry_name='Results to show (random):', row=5, default_value=10)

        # Adding a button to show plots of angles and shifts as function of segments
        self.add_show_results_button(lambda: self.show_angle_and_shifts_plot(int(result_number.get())), row=5, text="Show results")

        # Imports a themed image at the bottom
        self.add_image(image_name="angles_and_shifts_correction.jpg", new_size=600, row=6)

    @check_parameters(['input_star_file', 'pf_number', 'output_directory'])
    def run_function(self):
        function = AnglesAndShiftsCorrection(self.input_star_file, self.pf_number, self.output_directory)
        self.output, self.input = function.adjust_angles_and_translations()
