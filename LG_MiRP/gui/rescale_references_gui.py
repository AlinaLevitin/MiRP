"""
Author: Alina Levitin
Date: 28/03/24
Updated: 02/04/24

Two GUI classes (master and frame) for class reference rescaling
The method of reference rescaling is located in LG_MiRP/methods/reference_scaler
"""
from ..gui_base import LgFrameBase, LgMasterGui
from ..methods import rescale_and_crop_image


class RescaleReferencesGui(LgMasterGui):
    """
    ...
    Inherits from LgMasterGui
    """

    def __init__(self, path):
        super().__init__()
        self.add_job_name("Rescale References")
        frame1 = RescaleReferenceFrame(self, path)
        frame1.grid(row=1, column=0, sticky="NSEW")
        frame2 = LgFrameBase(self)
        frame2.grid(row=2, column=0, sticky="NSEW")
        frame2.add_sub_job_name("References")
        frame2.display_multiple_mrc_files(path, row=1)
        self.mainloop()


class RescaleReferenceFrame(LgFrameBase):
    """
    ...
    Inherits from LgFrameBase
    """

    def __init__(self, master, path):
        """
        :param master: the master gui in which the frame will be displayed
        """
        self.path = path
        super().__init__(master)
        # Adds the job name at the top row
        # self.add_sub_job_name("Rescale References", row=0)

        input_pixel_size = self.add_number_entry("Pixel size", row=1)

        input_box_size = self.add_number_entry("Box size", row=2)

        output_directory = self.add_directory_entry('Select output directory', row=3)
        # Creates a "Run" button that uses the segment average method
        self.add_run_button(lambda: rescale_and_crop_image(self.path,
                                                           input_pixel_size,
                                                           input_box_size,
                                                           output_directory
                                                           ),
                            row=4)
