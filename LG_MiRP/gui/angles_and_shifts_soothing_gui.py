"""
Author: Alina Levitin
Date: 17/04/24
Updated: 18/04/24

Two GUI classes (master and frame) to unifi PHI/Rot (angle smoothing)
The method of angle smoothing is in and extraction is located in LG_MiRP/methods/angle_smoothing

"""
from ..gui_base import LgFrameBase, LgMasterGui
from ..methods import smooth_angles, smooth_xy_shifts


class SmoothingGui(LgMasterGui):
    """
    ...
    Inherits from LgMasterGui
    """

    def __init__(self, label):
        super().__init__()
        if label == 'angles':
            self.add_job_name("Angle (PHI/Rot) smoothing")
        elif label == "shifts":
            self.add_job_name("XY shifts smoothing")
        frame = SmoothingFrame(self, label)
        frame.grid(row=1, column=0, sticky="NSEW")
        self.mainloop()


class SmoothingFrame(LgFrameBase):
    """
    ...
    Inherits from LgFrameBase
    """

    def __init__(self, master, label):
        """
        :param master: the master gui in which the frame will be displayed
        """
        super().__init__(master)
        # Creates an entry for run_it000_data.star file
        star_file_input = self.add_file_entry('star', 'Select a run_it001_data.star file', row=1)

        # Creates an entry for output directory
        output_path = self.add_directory_entry('Select output directory', row=2)

        self.add_run_button(lambda: self.run_function(label=label, star_file_input=star_file_input,
                                                      id_label='rlnAngleRot',
                                                      output_path=output_path),
                            row=3)

        self.add_show_results_button(command=self.show_result, row=4, text="Show results")
        # Imports a themed image at the bottom
        self.add_image_by_name(label)

    def run_function(self, label, star_file_input, output_path, id_label=None, cutoff=None):
        if label == 'angles':
            self.output = smooth_angles(star_file_input=star_file_input, id_label=id_label, output_path=output_path,
                                        cutoff=cutoff)
        elif label == 'shifts':
            self.output = smooth_xy_shifts(star_file_input=star_file_input, output_path=output_path)

    def add_image_by_name(self, label):
        if label == 'angles':
            self.add_image(image_name="rot_unification.jpg", new_size=600, row=5)
        elif label == 'shifts':
            self.add_image(image_name="shifts_unification.jpg", new_size=600, row=5)
