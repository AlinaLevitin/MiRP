"""
Author: Alina Levitin
Date: 28/03/24
Updated: 17/07/24

Two GUI classes (master and frame) for class refernce rescaling
The method ReferenceScaler, is located in LG_MiRP/methods/reference_scaler.py
"""
from ..gui_base import LgFrameBase, LgMasterGui, check_parameters
from ..methods import ReferenceScaler


class RescaleReferencesGui(LgMasterGui):
    """
    Inherits from LgMasterGui
    """
    def __init__(self, name):
        super().__init__(name)
        frame = RescaleReferenceFrame(self)
        frame.grid(row=1, column=0, sticky="NSEW")
        self.mainloop()


class RescaleReferenceFrame(LgFrameBase):
    """
    Inherits from LgFrameBase
    """
    def __init__(self, master, **kwargs):
        """
        :param master: the master gui in which the frame will be displayed
        """
        super().__init__(master)

        self.step = kwargs.get('step', None)

        # Adds the job name at the top row
        self.add_sub_job_name("Rescale References", row=0)

        # Adding a reference directory entry
        self.reference_directory = self.add_directory_entry('Select references directory', row=1, command=self.update_references)

        # Adding a numerical entry for pixel size in angstrom, default is 3.56A
        self.input_pixel_size = self.add_number_entry("Pixel size (Angstrom)", default_value=3.56, row=2)

        # Adding a numerical entry for box size in pexels, default is 250 pix
        self.input_box_size = self.add_number_entry("Box size (Pixels)", default_value=250, row=3)

        # Adding an output directory entry
        self.output_directory = self.add_directory_entry('Select output directory', row=4)

        # Creating a dropdown menu (combobox) for rescaling mask/references method (relion or scipy)
        options = ['relion', 'scipy']
        self.method_var = self.add_method_combobox(row=5, options=options)

        # Creates a "Run" button that uses the segment average method
        self.add_run_button(row=6)

        self.frame2 = None

    @check_parameters(['reference_directory', 'output_directory', 'input_pixel_size', 'input_box_size', 'method_var'])
    def run_function(self):
        """
        Setting up the class, checking if the parameters are all filled (prints in the terminal if something is missing)
        and running the function with the parameters
        """
        function = ReferenceScaler(self.reference_directory, self.output_directory, self.input_box_size, self.input_pixel_size, self.method_var)

        function.rescale_and_crop_image(directory="new_references", step=self.step)

    def update_references(self):
        """
        After the user selects the reference file/s, they will be displayed at the bottom of the window
        """
        # Display the MRC files from the selected path
        self.frame2 = LgFrameBase(self)
        self.frame2.grid(row=7, column=0, columnspan=6, sticky="NSEW")
        self.frame2.add_sub_job_name("References")
        self.frame2.display_multiple_mrc_files(self.reference_directory, row=1)
