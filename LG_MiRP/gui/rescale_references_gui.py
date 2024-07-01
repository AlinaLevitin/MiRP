"""
Author: Alina Levitin
Date: 28/03/24
Updated: 01/07/24

Two GUI classes (master and frame) for class reference rescaling
The method of reference rescaling is located in LG_MiRP/methods/reference_scaler
"""
from ..gui_base import LgFrameBase, LgMasterGui, check_parameters
from ..methods import ReferenceScaler


class RescaleReferencesGui(LgMasterGui):
    """
    ...
    Inherits from LgMasterGui
    """

    def __init__(self, name):
        super().__init__(name)
        frame1 = RescaleReferenceFrame(self)
        frame1.grid(row=1, column=0, sticky="NSEW")
        self.mainloop()


class RescaleReferenceFrame(LgFrameBase):
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
        self.add_sub_job_name("Rescale References", row=0)

        self.reference_directory = self.add_directory_entry('Select references directory', row=1, command=self.update_references)

        self.input_pixel_size = self.add_number_entry("Pixel size", row=2)

        self.input_box_size = self.add_number_entry("Box size", row=3)

        self.output_directory = self.add_directory_entry('Select output directory', row=4)

        options = ['relion', 'scipy']

        self.method_var = self.add_method_combobox(row=5, options=options)

        # Creates a "Run" button that uses the segment average method
        self.add_run_button(command=self.run_function, row=6)

        self.frame2 = None

    @check_parameters(['reference_directory', 'input_pixel_size', 'input_box_size', 'output_directory', 'method_var'])
    def run_function(self):
        function = ReferenceScaler(self.reference_directory, self.output_directory, self.input_box_size, self.input_pixel_size, self.method_var)

        function.rescale_and_crop_image(directory="new_references")

    def update_references(self):

        # Display the MRC files from the selected path
        self.frame2 = LgFrameBase(self)
        self.frame2.grid(row=7, column=0, columnspan=6, sticky="NSEW")
        self.frame2.add_sub_job_name("References")
        self.frame2.display_multiple_mrc_files(self.reference_directory.get(), row=1)
