"""
Author: Alina Levitin
Date: 28/03/24
Updated: 17/07/24

Two GUI classes (master and frame) for class reference rescaling
The method of reference rescaling is located in LG_MiRP/methods/reference_scaler
"""

from ..gui_base import LgFrameBase, LgMasterGui, check_parameters
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

        self.reference_file = self.add_file_entry(entry_type='mrc', entry_name='Choose mask .mrc file', row=1, command=self.update_references)

        self.input_pixel_size = self.add_number_entry("Pixel size", row=2)

        self.input_box_size = self.add_number_entry("Box size", row=3)

        self.output_directory = self.add_directory_entry('Select output directory', row=4)

        options = ['relion', 'scipy']

        self.method_var = self.add_method_combobox(row=5, options=options)

        # Creates a "Run" button that uses the segment average method
        self.add_run_button(row=6)

        self.frame2 = None

    @check_parameters(['reference_file', 'input_pixel_size', 'input_box_size', 'output_directory', 'method_var'])
    def run_function(self):
        function = ReferenceScaler(self.reference_file, self.output_directory, self.input_box_size,
                                   self.input_pixel_size, self.method_var)

        function.rescale_and_crop_image(directory='new_mask')

    def update_references(self):

        # Display the MRC files from the selected path
        self.frame2 = LgFrameBase(self)
        self.frame2.grid(row=7, column=0, columnspan=6, sticky="NSEW")
        self.frame2.add_sub_job_name("Selected mrc file:")
        self.frame2.display_single_mrc_files(self.reference_file, row=1)
