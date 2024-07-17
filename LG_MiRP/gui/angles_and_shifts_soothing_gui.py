"""
Author: Alina Levitin
Date: 17/04/24
Updated: 17/07/24

Two GUI classes (master and frame) to unifi PHI/Rot (angle smoothing)
The method of angle smoothing is in and extraction is located in LG_MiRP/methods/angle_smoothing

"""
from ..gui_base import LgFrameBase, LgMasterGui, check_parameters
from ..methods import SmoothAnglesOrShifts


class SmoothingGui(LgMasterGui):
    """
    ...
    Inherits from LgMasterGui
    """

    def __init__(self, name):
        super().__init__(name)
        frame = SmoothingFrame(self)
        frame.grid(row=1, column=0, sticky="NSEW")
        self.mainloop()


class SmoothingFrame(LgFrameBase):
    """
    ...
    Inherits from LgFrameBase
    """

    def __init__(self, master):
        """
        :param master: the master gui in which the frame will be displayed
        """
        super().__init__(master)

        self.add_sub_job_name("Angle (PHI/Rot) or XY shifts smoothing")

        options = ['angles', 'shifts']

        self.method = self.add_method_combobox(row=1, options=options, on_method_change=True)

        # Creates an entry for run_it000_data.star file
        self.star_file_input = self.add_file_entry('star', 'Select a run_it0xx_data.star file', row=2)

        # Creates an entry for output directory
        self.output_path = self.add_directory_entry('Select output directory', row=3)

        self.add_run_button(row=4)

        # Adding entry and button to show results
        result_number = self.add_number_entry(entry_name='Results to show (random):', row=5, default_value=10)
        self.add_show_results_button(lambda: self.show_angle_and_shifts_plot(int(result_number.get())), row=5, text="Show results")

        # Imports a themed image at the bottom
        self.add_image_by_name()

    @check_parameters(['input_star_file', 'output_directory', 'method'])
    def run_function(self):

        function = SmoothAnglesOrShifts(self.star_file_input, self.output_path, self.method, cutoff=None)

        self.input, self.output = function.smooth_angles_or_shifts()

    def on_method_change(self, event):
        self.add_image_by_name()

    def add_image_by_name(self):
        image_name = ""
        if self.method.get() == 'angles':
            image_name = "rot_unification.jpg"
        elif self.method.get() == 'shifts':
            image_name = "shifts_unification.jpg"

        if image_name:
            self.add_image(image_name=image_name, new_size=600)

