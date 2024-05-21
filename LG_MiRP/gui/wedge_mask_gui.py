"""
Author: Alina Levitin
Date: 12/05/24
Updated: 12/05/24


"""
import tkinter as tk

from ..gui_base import LgFrameBase, LgMasterGui, LGTopLevelBase
from ..methods import segment_average_generator, method_base


class WedgeMasksGui(LgMasterGui):
    """
    A class for the segment average master gui
    Inherits from LgMasterGui
    """
    def __init__(self):
        super().__init__()
        self.add_job_name("Generate Wedge Masks")
        frame1 = WedgeMasksFrame(self)
        frame1.grid(row=1, column=0, sticky="NSEW")
        self.mainloop()


class WedgeMasksFrame(LgFrameBase):
    """
    ...
    Inherits from LgFrameBase
    """

    def __init__(self, master):
        """
        :param master: the master gui in which the frame will be displayed
        """
        super().__init__(master)
        input_star_file = self.add_file_entry('star', 'Select a run_data.star file', row=1)

        input_pf_number = self.add_number_entry("Pixel size", row=1)

        self.add_image("segment_average.jpg", new_size=600, row=7)
