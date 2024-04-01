"""
Author: Alina Levitin
Date: 14/03/24
Updated: 31/3/24

Two GUI classes (master and frame) for class unification and extraction
The method of ... is located in LG_MiRP/methods/...
"""
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from ..gui_base import LgFrameBase, LgMasterGui, LGTopLevelBase
from ..methods import class_unifier, classes_distribution


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
        # Adds the job name at the top row
        self.add_sub_job_name("Class Unification", row=0)
        # Creates an entry for run_it001_data.star file
        input_star_file = self.add_file_entry('star', 'Select a run_it001_data.star file', row=1)
        # Creates an entry for input directory with mrcs stack files in Extract folder (after particle picking)
        output_directory = self.add_directory_entry('Select output directory', row=2)
        # Creates a "Run" button that uses the segment average method
        self.add_run_button(lambda: class_unifier(input_star_file, output_directory),
                            row=3)
        result_button = tk.Button(self, text="Show Classes Distribution", command=lambda: self.show_class_distribution(input_star_file))
        result_button.grid(row=4, column=0)
        # Imports a themed image at the bottom
        self.add_image(new_size=600, row=5)

    def show_class_distribution(self, input_star_file):
        fig = classes_distribution(input_star_file)
        pie_window = LGTopLevelBase(self)
        pie_window.title("Classes Distribution")
        pie_window.add_plot(fig)
