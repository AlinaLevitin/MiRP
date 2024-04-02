"""
Author: Alina Levitin
Date: 14/03/24
Updated: 02/04/24

Two GUI classes (master and frame) for class unification and extraction
The method of class unification and extraction is located in LG_MiRP/methods/class_unifier_extractor
"""
import tkinter as tk

from ..gui_base import LgFrameBase, LgMasterGui, LGTopLevelBase
from ..methods import class_unifier_extractor, classes_distribution


class ClassUnificationExtractionGui(LgMasterGui):
    """
    ...
    Inherits from LgMasterGui
    """
    def __init__(self):
        super().__init__()
        self.add_job_name("Class Unification and extraction")
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
        # Creates an entry for run_it000_data.star file
        input_star_file0 = self.add_file_entry('star', 'Select a run_it000_data.star file', row=1)
        # Creates an entry for run_it001_data.star file
        input_star_file1 = self.add_file_entry('star', 'Select a run_it001_data.star file', row=2)

        # Creates an entry for output directory
        output_directory = self.add_directory_entry('Select output directory', row=3)

        # Creates a "Run" button that uses the class unification and extraction method
        self.add_run_button(lambda: class_unifier_extractor(input_star_file0, input_star_file1, output_directory),
                            row=4)
        # Creates a button to show the distribution of classes according to 3D classification
        result_button = tk.Button(self, text="Show Classes Distribution", command=lambda: self.show_class_distribution(input_star_file1))
        result_button.grid(row=5, column=0)

        # Imports a themed image at the bottom
        self.add_image(new_size=600, row=6)

    def show_class_distribution(self, input_star_file):
        """
        Opening an additional window with class distribution in %
        :param input_star_file: star file after 3D classification run_it001_data.star
        """
        # Generating a pie chart with percentages of MTs classified in each class
        fig = classes_distribution(input_star_file)
        # Generating a Tkinter Top level window
        pie_window = LGTopLevelBase(self)
        # Adding a title to the figure
        pie_window.title("Classes Distribution")
        # Adding the pie chart to the window
        pie_window.add_plot(fig)
