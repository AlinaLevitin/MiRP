"""
Author: Alina Levitin
Date: 17/04/24
Updated: 17/04/24

Two GUI classes (master and frame) to unifi PHI/Rot (angle smoothing)
The method of angle smoothing is in and extraction is located in LG_MiRP/methods/angle_smoothing

"""
from ..gui_base import LgFrameBase, LgMasterGui
from ..methods import smooth_angles


class AngleSmoothingGui(LgMasterGui):
    """
    ...
    Inherits from LgMasterGui
    """
    def __init__(self):
        super().__init__()
        self.add_job_name("Angle (PHI/Rot) smoothing")
        frame = AngleSmoothingFrame(self)
        frame.grid(row=1, column=0, sticky="NSEW")
        self.mainloop()


class AngleSmoothingFrame(LgFrameBase):
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
        star_file_input = self.add_file_entry('star', 'Select a run_it001_data.star file', row=1)

        # Creates an entry for output directory
        output_path = self.add_directory_entry('Select output directory', row=2)

        # Creates a "Run" button that uses the class unification and extraction method
        self.add_run_button(lambda: smooth_angles(star_file_input=star_file_input,
                                                  id_label='rlnAngleRot',
                                                  output_path=output_path),
                            row=3)

        # Imports a themed image at the bottom
        self.add_image(image_name="Rot_unification.jpg", new_size=600, row=4)
