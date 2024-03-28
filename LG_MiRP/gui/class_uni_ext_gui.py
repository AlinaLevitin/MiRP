"""
Author: Alina Levitin
Date: 14/03/24
Updated: 14/3/24

Two GUI classes (master and frame) for class unification and extraction
The method of ... is located in LG_MiRP/methods/...
"""
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from ..gui_base import LgFrameBase, LgMasterGui, LGTopLevelBase
from ..methods import segment_average_generator


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
        # Creates an entry for binning
        bins_entry = self.add_number_entry("Binning (example: 4)", row=2)
        # Creates an entry for input directory with mrcs stack files in Extract folder (after particle picking)
        input_directory = self.add_directory_entry('Select directory containing extracted particles in Extract', row=3)
        # Creates an entry for output directory (usually the project folder) there it will save the new mrcs files and
        # the new star file
        output_directory = self.add_directory_entry('Select output directory', row=4)
        # Creates a "Run" button that uses the segment average method
        self.add_run_button(lambda: segment_average_generator(input_directory,
                                                              output_directory,
                                                              input_star_file,
                                                              binning=bins_entry),
                            row=5)
        result_button = tk.Button(self, text="Show segments histogram", command=lambda: self.show_mt_segment_histogram(input_star_file))
        result_button.grid(row=6, column=0)
        # Imports a themed image at the bottom
        self.add_image("segment_average.jpg", new_size=600, row=7)

    def show_mt_segment_histogram(self, input_star_file):
        fig = mt_segment_histogram(input_star_file)
        histogram_window = LGTopLevelBase(self)
        histogram_window.title("Histogram of number of segments per MT")
        histogram_window.add_plot(fig)