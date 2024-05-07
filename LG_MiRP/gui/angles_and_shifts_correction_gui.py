"""
Author: Alina Levitin
Date: 17/04/24
Updated: 18/04/24

Two GUI classes (master and frame) to correct PHI/Rot and shifts
The method of angle smoothing is in and extraction is located in LG_MiRP/methods/angle_shifts_correction

"""
from ..gui_base import LgFrameBase, LgMasterGui
from ..methods import adjust_angles_and_translations


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
        star_file_input = self.add_file_entry('star', 'Select a run_it0xx_data_class_corrected.star file', row=1)

        # Creates an entry for output directory
        output_path = self.add_directory_entry('Select output directory', row=2)

        pf_number = self.add_number_entry("Number of proto-filaments", row=3)

        self.add_run_button(lambda: self.run_function(star_file_input=star_file_input,
                                                      pf_number=pf_number,
                                                      output_path=output_path),
                            row=4)

        self.add_show_results_button(command=self.show_result, row=5, text="Show results")
        # Imports a themed image at the bottom
        self.add_image(image_name="angles_and_shifts_correction.jpg", new_size=600, row=6)

    def run_function(self, star_file_input, pf_number, output_path):
        self.output = adjust_angles_and_translations(star_file_input=star_file_input,
                                                     pf_number=pf_number,
                                                     output_directory=output_path)
