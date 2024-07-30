"""
Author: Alina Levitin
Date: 14/03/24
Updated: 28/07/24

Two GUI classes (master and frame) for class unification and extraction
The method of class unification and extraction is located in LG_MiRP/methods/class_unifier_extractor.py
"""
import tkinter as tk

from ..gui_base import LgFrameBase, LgMasterGui, LGTopLevelBase, check_parameters
from ..methods import ClassUnifierExtractor
from ..methods_base import ParticlesStarfile


class ClassUnificationExtractionGui(LgMasterGui):
    """
    Inherits from LgMasterGui
    """
    def __init__(self, name):
        super().__init__(name)
        frame = ClassUnificationFrame(self)
        frame.grid(row=1, column=0, sticky="NSEW")
        self.mainloop()


class ClassUnificationFrame(LgFrameBase):
    """
    ...
    Inherits from LgFrameBase
    """
    def __init__(self, master):
        """
        :param master: the master gui in which the frame will be displayed
        """
        super().__init__(master)

        self.add_sub_job_name("Class Unification and extraction")

        options = ['pf_number_check', 'seam_check']

        self.step = self.add_method_combobox(row=1, options=options)
        # Creates an entry for run_it000_data.star file
        self.input_star_file0 = self.add_file_entry('star', 'Select a run_it000_data.star file', row=2)
        # Creates an entry for run_it001_data.star file
        self.input_star_file1 = self.add_file_entry('star', 'Select a run_it0xx_data.star file', row=3)

        # Creates an entry for output directory
        self.output_directory = self.add_directory_entry('Select output directory', row=4)

        # Adds a number entry for portion cutoff (if the most common class is less than that portion then th MT is
        # discarded
        self.cutoff = self.add_number_entry(entry_name='Portion cutoff:', row=5, default_value=0.7)

        # Creates a "Run" button that uses the class unification and extraction method
        self.add_run_button(row=6)
        # Creates a button to show the distribution of classes according to 3D classification
        result_button = tk.Button(self, text="Show Classes Distribution", command=self.show_class_distribution)
        result_button.grid(row=7, column=0)

        # Imports a themed image at the bottom
        self.add_image(new_size=600, row=8)

    @check_parameters(['input_star_file0', 'input_star_file1', 'output_directory', 'cutoff'])
    def run_function(self):
        """
        Setting up the class, checking if the parameters are all filled (prints in the terminal if something is missing)
        and running the function with the parameters
        """
        function = ClassUnifierExtractor(self.input_star_file0, self.input_star_file1, self.output_directory, self.cutoff, self.step.get())
        self.output = function.class_unifier_extractor()

    def show_class_distribution(self):
        """
        Opening an additional window with class distribution in %
        """
        # Generating a pie chart with percentages of MTs classified in each class
        if self.output.empty:
            input_file = ParticlesStarfile(self.input_star_file1)
            self.input = input_file.particles_dataframe
            fig = ClassUnifierExtractor.classes_distribution_fig(self.input)
        else:
            fig = ClassUnifierExtractor.classes_distribution_fig(self.output)
        # Generating a Tkinter Top level window
        pie_window = LGTopLevelBase(self)
        # Adding a title to the figure
        pie_window.title("Classes Distribution")
        # Adding the pie chart to the window
        pie_window.add_plot(fig)
