"""
Author: Alina Levitin
Date: 12/05/24
Updated: 12/05/24


"""
import tkinter as tk

from ..gui_base import LgFrameBase, LgMasterGui, LGTopLevelBase
from ..methods import WedgeMaskGenerator


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
        self.input_star_file = self.add_file_entry('star', 'Select a particles.star file', row=1)

        self.microtubule_volume = self.add_file_entry('mrc', 'Select microtubule volume .mrc file', row=2)

        self.microtubule_mask = self.add_file_entry('mrc', 'Select microtubule mask .mrc file', row=3)

        self.fit_tubulin_pdb = self.add_file_entry('pdb', 'Select fit tubulin .pdb file', row=4)

        self.pf_number = self.add_number_entry("Proto-filament number", default_value='13', row=5)

        self.helical_twist = self.add_number_entry("Helical twist", default_value='0', row=6)

        self.helical_rise = self.add_number_entry("Helical rise (in Angstrom)", default_value='82', row=7)

        self.output_path = self.add_directory_entry('Select output directory', row=8)

        self.add_run_button(self.run_function, row=9)

        self.add_image(image_name='wedge_mask_generator.png', new_size=600, row=10)

    def run_function(self):
        function = WedgeMaskGenerator(self.input_star_file,
                                      self.microtubule_volume,
                                      self.microtubule_mask,
                                      self.fit_tubulin_pdb,
                                      self.pf_number,
                                      self.helical_twist,
                                      self.helical_rise,
                                      self.output_path
                                      )

        function.generate_wedge_mask()
