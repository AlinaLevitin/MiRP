"""
Author: Alina Levitin
Date: 10/03/24
Updated: 11/3/24

Two GUI classes (master and frame) for segment average generation
The method of segment averaging is located in LG_MiRP/methods/segment_average_generator
"""
import tkinter as tk

# from LG_MiRP import LgFrameBase, LgMasterGui, LGTopLevelBase, segment_average_generator, mt_segment_histogram
from ..gui_base import LgFrameBase, LgMasterGui, LGTopLevelBase
from ..methods import segment_average_generator, mt_segment_histogram


class SegmentAverageGui(LgMasterGui):
    """
    A class for the segment average master gui
    Inherits from LgMasterGui
    """
    def __init__(self):
        super().__init__()
        self.add_job_name("Segment Average Generation")
        frame = SegmentAverageFrame(self)
        frame.grid(row=1, column=0, sticky="NSEW")
        self.mainloop()


class SegmentAverageFrame(LgFrameBase):
    """
    A class for the segment average frame
    Inherits from LgFrameBase
    """
    def __init__(self, master):
        """
        :param master: the master gui in which the frame will be displayed
        """
        super().__init__(master)
        # Adds the job name at the top row
        self.add_sub_job_name("Segment Average Generator", row=0)
        # Creates an entry for particles.star file
        input_star_file = self.add_file_entry('star', 'Select a particles.star file', row=1)
        # Creates a Show segments histogram to show the distribution of number of segments
        result_button = tk.Button(self, text="Show segments histogram",
                                  command=lambda: self.show_mt_segment_histogram(input_star_file))
        result_button.grid(row=2, column=0)
        # Creates an entry for binning
        # bins_entry = self.add_number_entry("Binning (example: 4)", row=3)
        # Creates an entry for input directory with mrcs stack files in Extract folder (after particle picking)
        input_directory = self.add_directory_entry('Select directory containing extracted particles in Extract', row=4)
        # Creates an entry for output directory (usually the project folder) there it will save the new mrcs files and
        # the new star file
        output_directory = self.add_directory_entry('Select output directory', row=5)
        # Creates a "Run" button that uses the segment average method
        self.add_run_button(lambda: segment_average_generator(input_directory,
                                                              output_directory,
                                                              input_star_file,
                                                              ),
                            row=6)

        # Imports a themed image at the bottom
        self.add_image("segment_average.jpg", new_size=600, row=7)

    def show_mt_segment_histogram(self, input_star_file):
        fig = mt_segment_histogram(input_star_file)
        histogram_window = LGTopLevelBase(self)
        histogram_window.title("Histogram of number of segments per MT")
        histogram_window.add_plot(fig)
