"""
Author: Alina Levitin
Date: 26/05/24
Updated: 26/05/24


"""
import tkinter as tk

from ..gui_base import LgFrameBase, LgMasterGui, LGTopLevelBase
from ..methods import MicrotubuleSubtract


class MicrotubuleSubtractGui(LgMasterGui):
    """
    A class for the segment average master gui
    Inherits from LgMasterGui
    """

    def __init__(self):
        super().__init__()
        self.add_job_name("Generate Protofilament Particles from Wedges")
        frame1 = MicrotubuleSubtractFrame(self)
        frame1.grid(row=1, column=0, sticky="NSEW")
        self.mainloop()


class MicrotubuleSubtractFrame(LgFrameBase):
    """
    ...
    Inherits from LgFrameBase
    """

    def __init__(self, master):
        """
        :param master: the master gui in which the frame will be displayed
        """
        super().__init__(master)
        self.input_star_file = self.add_file_entry('star', 'Select a particles.star file', row=1)

        self.pf_number = self.add_number_entry("Proto-filament number", default_value='13', row=2)

        self.input_path = self.add_directory_entry('Select the "pf_wedges" directory', row=3)

        options = ['relion', 'numpy']

        self.method_var = self.add_method_combobox(row=4, options=options)

        self.add_run_button(self.run_function, row=5)

        self.add_image(image_name='wedge_mask_generator.png', new_size=600, row=10)

    def run_function(self):
        function = MicrotubuleSubtract(input_star_file=self.input_star_file,
                                       pf_number=self.pf_number,
                                       input_wedge_directory=self.input_path,
                                       method=self.method_var
                                       )

        function.subtract_microtubule()
