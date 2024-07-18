"""
Author: Alina Levitin
Date: 28/05/24
Updated: 17/07/24

GUI classes (master gui and frame) for creating mrc files with masks in the shape of a wedge or a cylindrical cutout
Uses MaskGenerator method class in mask_generator.py

"""
from ..gui_base import LgFrameBase, LgMasterGui, check_parameters
from ..methods import MaskGenerator


class MaskGeneratorGui(LgMasterGui):
    """
    A class for the segment average master gui
    Inherits from LgMasterGui
    """

    def __init__(self, name):
        super().__init__(name)
        frame1 = MaskGeneratorFrame(self)
        frame1.grid(row=1, column=0, sticky="NSEW")
        self.mainloop()


class MaskGeneratorFrame(LgFrameBase):
    """
    Inherits from LgFrameBase
    """

    def __init__(self, master):
        """
        :param master: the master gui in which the frame will be displayed
        """
        super().__init__(master)
        # Adding a title label
        self.add_sub_job_name("Mask Generator", row=0)

        # Adding a star file entry
        self.input_star_file = self.add_file_entry('star', 'Select a particles.star file', row=1)

        # Adding entry for the microtubule mrc file
        self.microtubule_volume = self.add_file_entry('mrc', 'Select microtubule volume .mrc file', row=2)

        # Adding entry for a mask mrc file
        self.microtubule_mask = self.add_file_entry('mrc', 'Select microtubule mask .mrc file', row=3)

        # Adding entry for pdb file in which the tubulin is fit to a protofilament next to the seam
        self.fit_tubulin_pdb = self.add_file_entry('pdb', 'Select fit tubulin .pdb file', row=4)

        # Adding numerical entry for protofilament number, default is 13
        self.pf_number = self.add_number_entry("Proto-filament number", default_value='13', row=5)

        # Adding a numerical entry for helical twist, default is 0
        self.helical_twist = self.add_number_entry("Helical twist", default_value='0', row=6)

        # Adding a numerical entry for helical rise in angstrom, default is 82
        self.helical_rise = self.add_number_entry("Helical rise (in Angstrom)", default_value='82', row=7)

        # Adding entry for output directory
        self.output_directory = self.add_directory_entry('Select output directory', row=8)

        # Setting a dropdown menu (combobox) for type of mask
        options = ['wedge', 'cylindrical_cutout']
        self.method = self.add_method_combobox(row=9, options=options, on_method_change=True)
        # Executes self.on_method_change

        # Adding a "Run" button that will run self.run_function
        self.add_run_button(row=10)

        # Adding a themed image
        self.add_image_by_name()

    @check_parameters(['input_star_file', 'microtubule_volume', 'microtubule_mask', 'fit_tubulin_pdb', 'pf_number', 'helical_twist', 'helical_rise',  'output_directory'])
    def run_function(self):
        """
        Setting up the class, checking if the parameters are all filled (prints in the terminal if something is missing)
        and running the function with the parameters
        """
        function = MaskGenerator(self.input_star_file,
                                 self.microtubule_volume,
                                 self.microtubule_mask,
                                 self.fit_tubulin_pdb,
                                 self.pf_number,
                                 self.helical_twist,
                                 self.helical_rise,
                                 self.output_directory
                                 )

        if self.method.get() == 'cylindrical_cutout':
            function.generate_cylindrical_cutout_mask()
        elif self.method.get() == 'wedge':
            function.generate_wedge_mask()

    def on_combobox_select(self, event):
        """
        Changing the image according to the type of the mask (wedge or cylindrical cutout)
        Using ttk.Combobox.bind("<<ComboboxSelected>>", self.on_method_change)

        :param event: the event on which to perform the change
        """
        self.add_image_by_name()

    def add_image_by_name(self):
        """
        The function that changes the theme image according to the selected method
        """
        image_name = ""
        if self.method.get() == 'wedge':
            image_name = 'wedge_mask_generator.png'
        elif self.method.get() == 'cylindrical_cutout':
            image_name = "cylindrical_cutout_mask_generator.png"

        if image_name:
            self.add_image(image_name=image_name, new_size=600, row=11)
