"""
Author: Alina Levitin
Date: 17/04/24
Updated: 18/04/24

Two GUI classes (master and frame) to unifi PHI/Rot (angle smoothing)
The method of angle smoothing is in and extraction is located in LG_MiRP/methods/angle_smoothing

"""
from ..gui_base import LgFrameBase, LgMasterGui
from ..methods import SmoothAnglesOrShifts


class SmoothingGui(LgMasterGui):
    """
    ...
    Inherits from LgMasterGui
    """

    def __init__(self, method):
        super().__init__()
        if method == 'angles':
            self.add_job_name("Angle (PHI/Rot) smoothing")
        elif method == "shifts":
            self.add_job_name("XY shifts smoothing")
        frame = SmoothingFrame(self, method)
        frame.grid(row=1, column=0, sticky="NSEW")
        self.mainloop()


class SmoothingFrame(LgFrameBase):
    """
    ...
    Inherits from LgFrameBase
    """

    def __init__(self, master, method):
        """
        :param master: the master gui in which the frame will be displayed
        """
        super().__init__(master)
        self.method = method

        # Creates an entry for run_it000_data.star file
        self.star_file_input = self.add_file_entry('star', 'Select a run_it0xx_data.star file', row=1)

        # Creates an entry for output directory
        self.output_path = self.add_directory_entry('Select output directory', row=2)

        self.add_run_button(self.run_function, row=3)

        # Adding entry and button to show results
        result_number = self.add_number_entry(entry_name='Results to show (random):', row=4)
        self.add_show_results_button(lambda: self.show_result(int(result_number.get())), row=4, text="Show results")

        # Imports a themed image at the bottom
        self.add_image_by_name(self.method)

    def run_function(self):

        function = SmoothAnglesOrShifts(self.star_file_input, self.output_path, self.method, cutoff=None)

        self.output = function.smooth_angles_or_shifts()

    def add_image_by_name(self, function):
        if function == 'angles':
            self.add_image(image_name="rot_unification.jpg", new_size=600, row=5)
        elif function == 'shifts':
            self.add_image(image_name="shifts_unification.jpg", new_size=600, row=5)
