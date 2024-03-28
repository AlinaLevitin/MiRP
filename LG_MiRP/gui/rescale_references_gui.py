"""
Author: Alina Levitin
Date: 28/03/24
Updated: 28/3/24

Two GUI classes (master and frame) for class unification and extraction
The method of ... is located in LG_MiRP/methods/...
"""
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from ..gui_base import LgFrameBase, LgMasterGui
from ..methods import rescale_and_crop_image


class RescaleReferencesGui(LgMasterGui):
    def __init__(self):
        super().__init__()
        self.add_job_name("Rescale References")
        frame = RescaleReferenceFrame(self)
        frame.grid(row=1, column=0, sticky="NSEW")
        self.mainloop()


class RescaleReferenceFrame(LgFrameBase):
    def __init__(self, master):
        """
        :param master: the master gui in which the frame will be displayed
        """
        super().__init__(master)
        # Adds the job name at the top row
        self.add_sub_job_name("Rescale References", row=0)

        input_pixel_size = self.add_number_entry("Pixel size", row=1)

        input_box_size = self.add_number_entry("Box size", row=2)

        output_directory = self.add_directory_entry('Select output directory', row=3)
        # Creates a "Run" button that uses the segment average method
        self.add_run_button(lambda: rescale_and_crop_image(
                                                           input_pixel_size,
                                                           input_box_size,
                                                           output_directory
                                                           ),
                            row=4)

        # Imports a themed image at the bottom
        self.add_image("default_image.jpg", new_size=600, row=5)
