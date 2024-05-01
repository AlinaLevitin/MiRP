"""
Author: Alina Levitin
Date: 17/04/24
Updated: 18/04/24

Two GUI classes (master and frame) to unifi PHI/Rot (angle smoothing)
The method of angle smoothing is in and extraction is located in LG_MiRP/methods/angle_smoothing

"""
from ..gui_base import LgFrameBase, LgMasterGui
from ..methods import smooth_angles_or_shifts


class SmoothingGui(LgMasterGui):
    """
    ...
    Inherits from LgMasterGui
    """

    def __init__(self, function):
        super().__init__()
        if function == 'angles':
            self.add_job_name("Angle (PHI/Rot) smoothing")
        elif function == "shifts":
            self.add_job_name("XY shifts smoothing")
        frame = SmoothingFrame(self, function)
        frame.grid(row=1, column=0, sticky="NSEW")
        self.mainloop()


class SmoothingFrame(LgFrameBase):
    """
    ...
    Inherits from LgFrameBase
    """

    def __init__(self, master, function):
        """
        :param master: the master gui in which the frame will be displayed
        """
        super().__init__(master)
        # Creates an entry for run_it000_data.star file
        star_file_input = self.add_file_entry('star', 'Select a run_it0xx_data.star file', row=1)

        # Creates an entry for output directory
        output_path = self.add_directory_entry('Select output directory', row=2)

        self.add_run_button(lambda: self.run_function(function=function,
                                                      star_file_input=star_file_input,
                                                      output_path=output_path),
                            row=3)

        # Adding entry and button to show results
        result_number = self.add_number_entry(entry_name='Results to show (random):', row=4)
        self.add_show_results_button(lambda: self.show_result(int(result_number.get())), row=4, text="Show results")

        # Imports a themed image at the bottom
        self.add_image_by_name(function)

    def run_function(self, function, star_file_input, output_path, cutoff=None):
        self.output = smooth_angles_or_shifts(star_file_input=star_file_input,
                                              function=function,
                                              output_path=output_path,
                                              cutoff=cutoff)

    def add_image_by_name(self, function):
        if function == 'angles':
            self.add_image(image_name="rot_unification.jpg", new_size=600, row=5)
        elif function == 'shifts':
            self.add_image(image_name="shifts_unification.jpg", new_size=600, row=5)
