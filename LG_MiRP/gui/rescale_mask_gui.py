"""
Author: Alina Levitin
Date: 28/03/24
Updated: 02/04/24

Two GUI classes (master and frame) for class reference rescaling
The method of reference rescaling is located in LG_MiRP/methods/reference_scaler
"""

from ..gui_base import LgFrameBase, LgMasterGui
from ..methods import ReferenceScaler


class RescaleMaskGui(LgMasterGui):
    """
    ...
    Inherits from LgMasterGui
    """

    def __init__(self, name):
        super().__init__(name)
        frame = RescaleMaskFrame(self)
        frame.grid(row=1, column=0, sticky="NSEW")
        self.mainloop()


class RescaleMaskFrame(LgFrameBase):
    """
    ...
    Inherits from LgFrameBase
    """

    def __init__(self, master):
        """
        :param master: the master gui in which the frame will be displayed
        """
        super().__init__(master)
        # Adds the job name at the top row
        self.add_sub_job_name("Rescale Mask", row=0)

        self.input_file = self.add_file_entry(entry_type='mrc', entry_name='Choose mask .mrc file', row=1)

        self.input_pixel_size = self.add_number_entry("Pixel size", row=2)

        self.input_box_size = self.add_number_entry("Box size", row=3)

        self.output_path = self.add_directory_entry('Select output directory', row=4)

        options = ['relion', 'scipy']

        self.method_var = self.add_method_combobox(row=5, options=options)

        # Creates a "Run" button that uses the segment average method
        self.add_run_button(command=self.run_function, row=6)

    def run_function(self):
        function = ReferenceScaler(self.input_file.get(), self.output_path, self.input_box_size, self.input_pixel_size)

        function.rescale_and_crop_image(method=self.method_var.get())
