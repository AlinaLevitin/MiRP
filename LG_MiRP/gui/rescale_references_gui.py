"""
Author: Alina Levitin
Date: 28/03/24
Updated: 02/04/24

Two GUI classes (master and frame) for class reference rescaling
The method of reference rescaling is located in LG_MiRP/methods/reference_scaler
"""
import tkinter as tk
from tkinter import ttk

from ..gui_base import LgFrameBase, LgMasterGui
from ..methods import ReferenceScaler


class RescaleReferencesGui(LgMasterGui):
    """
    ...
    Inherits from LgMasterGui
    """

    def __init__(self, path, name):
        super().__init__(name)
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
        self.add_sub_job_name("Rescale References", row=0)

        self.input_pixel_size = self.add_number_entry("Pixel size", row=1)

        self.input_box_size = self.add_number_entry("Box size", row=2)

        self.output_path = self.add_directory_entry('Select output directory', row=3)

        options = ['relion', 'scipy']

        self.method_var = self.add_method_combobox(row=4, options=options)

        # Creates a "Run" button that uses the segment average method
        self.add_run_button(command=self.run_function, row=5)

    def run_function(self):
        function = ReferenceScaler(self.path, self.output_path, self.input_box_size, self.input_pixel_size, self.method_var)

        function.rescale_and_crop_image()
