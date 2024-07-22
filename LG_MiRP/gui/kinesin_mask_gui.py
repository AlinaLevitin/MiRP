"""
Author: Alina Levitin
Date: 18/07/24
Updated: 22/07/24

Two GUI classes (master and frame) for class generating kinesin only mask on protofilaments
The method KinesinMaskGenerator, is located in LG_MiRP/methods/kinesin_mask_generator.py
"""
from ..gui_base import LgFrameBase, LgMasterGui, check_parameters
from ..methods import KinesinMaskGenerator


class KiensinMaskGui(LgMasterGui):
    """
    Inherits from LgMasterGui
    """
    def __init__(self, name):
        super().__init__(name)
        frame = KinesinMaskFrame(self)
        frame.grid(row=1, column=0, sticky="NSEW")
        self.mainloop()


class KinesinMaskFrame(LgFrameBase):
    """
    Inherits from LgFrameBase
    """
    def __init__(self, master, **kwargs):
        """
        :param master: the master gui in which the frame will be displayed
        """
        super().__init__(master)

        # Adds the job name at the top row
        self.add_sub_job_name("Kinesin Mask Generator", row=0)

        # Adding entry for mask mrc file
        self.pdb_file = self.add_file_entry(entry_type='pdb', entry_name='Choose a kinein .pdb file', row=1)

        # Adding a numerical entry for pixel size in angstrom, default is 3.56A
        self.input_pixel_size = self.add_number_entry("Pixel size (Angstrom)", default_value=3.56, row=2)

        self.microtubule_volume = self.add_file_entry('mrc', 'Select microtubule volume .mrc file', row=3)

        self.microtubule_mask = self.add_file_entry('mrc', 'Select microtubule mask .mrc file', row=4)

        # Adding an output directory entry
        self.output_directory = self.add_directory_entry('Select output directory', row=5)

        self.sphere_radius = self.add_number_entry("Sphere radius is pixels", default_value=20, row=6)

        # Creates a "Run" button that uses the segment average method
        self.add_run_button(row=7)

    # @check_parameters(['pdb_file', 'output_directory', 'input_pixel_size', 'input_box_size'])
    def run_function(self):
        """
        Setting up the class, checking if the parameters are all filled (prints in the terminal if something is missing)
        and running the function with the parameters
        """
        function = KinesinMaskGenerator(fit_tubulin_pdb=self.pdb_file,
                                        microtubule_volume=self.microtubule_volume,
                                        microtubule_mask=self.microtubule_mask,
                                        output_path=self.output_directory,
                                        pixel_size=self.input_pixel_size,
                                        sphere_radius=self.sphere_radius)

        function.generate_spherical_mask()

