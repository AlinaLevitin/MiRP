"""
Author: Alina Levitin
Date: 10/03/24
Updated: 17/07/24

Two GUI classes (master and frame) for segment average generation
The method of segment averaging is located in LG_MiRP/methods/segment_average_generator
"""

from ..gui_base import LgFrameBase, LgMasterGui, LGTopLevelBase, check_parameters
from ..methods import SegmentAverageGenerator
from LG_MiRP.methods_base import ParticlesStarfile, mt_segment_histogram


class SegmentAverageGui(LgMasterGui):
    """
    A class for the segment average master gui
    Inherits from LgMasterGui
    """
    def __init__(self, name):
        super().__init__(name)
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
        self.input_star_file = self.add_file_entry('star', 'Select a particles.star file', row=1)
        # Creates a Show segments histogram to show the distribution of number of segments
        self.add_show_results_button(command=self.show_mt_segment_histogram,
                                     row=2, text="Show segments histogram")
        # Creates an entry for input directory with mrcs stack files in Extract folder (after particle picking)
        self.input_directory = self.add_directory_entry('Select directory containing extracted particles in Extract', row=4)
        # Creates an entry for output directory (usually the project folder) there it will save the new mrcs files and
        # the new star file
        self.output_directory = self.add_directory_entry('Select output directory', row=5)
        # Creates a "Run" button that uses the segment average method
        self.add_run_button(row=6)

        # Imports a themed image at the bottom
        self.add_image("segment_average.jpg", new_size=600, row=7)

    @check_parameters(['input_directory', 'output_directory', 'input_star_file'])
    def run_function(self):
        """
        Setting up the class, checking if the parameters are all filled (prints in the terminal if something is missing)
        and running the function with the parameters
        """
        function = SegmentAverageGenerator(self.input_directory, self.output_directory, self.input_star_file)
        function.generate_segment_averages()

    def show_mt_segment_histogram(self):
        """
        Displays a histogram of the distribution of the segment number of the MTs
        """
        input_starfile = ParticlesStarfile(self.input_star_file.get())
        fig = mt_segment_histogram(input_starfile.particles_dataframe)
        histogram_window = LGTopLevelBase(self)
        histogram_window.title("Histogram of number of segments per MT")
        histogram_window.add_plot(fig)
