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
        self.fit_tubulin_pdb = self.add_file_entry(entry_type='pdb', entry_name='Choose a kinein .pdb file', row=1)

        self.microtubule_volume = self.add_file_entry('mrc', 'Select microtubule volume .mrc file', row=2)

        # Adding an output directory entry
        self.output_directory = self.add_directory_entry('Select output directory', row=3)

        self.sphere_radius = self.add_number_entry("Sphere radius is pixels", default_value=20, row=4)

        # Adding a numerical entry for interval of the spheres in angstrom, default is 82A
        self.x_interval = self.add_number_entry("Interval (Angstrom)", default_value=82, row=5)

        # Creates a "Run" button that uses the segment average method
        self.add_run_button(row=6)

    # @check_parameters(['pdb_file', 'output_directory', 'input_pixel_size', 'input_box_size'])
    def run_function(self):
        """
        Setting up the class, checking if the parameters are all filled (prints in the terminal if something is missing)
        and running the function with the parameters
        """
        function = KinesinMaskGenerator(fit_tubulin_pdb=self.fit_tubulin_pdb,
                                        microtubule_volume=self.microtubule_volume,
                                        output_path=self.output_directory,
                                        sphere_radius=self.sphere_radius,
                                        x_interval=self.x_interval)

        function.generate_multiple_spheres()

