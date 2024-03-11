"""
Author: Alina Levitin
Date: 10/03/24
Updated: 10/3/24

Two GUI classes (master and frame) for segment average generation
The method of segment averaging is located in LG_MiRP/methods/segment_average_generator
"""

from LG_MiRP import LgFrameBase, LgMasterGui, segment_average_generator


class SegmentAverageGui(LgMasterGui):
    def __init__(self):
        super().__init__()
        self.add_job_name("Segment Average Generation")
        frame = SegmentAverageFrame(self)
        frame.grid(row=1, column=0)


class SegmentAverageFrame(LgFrameBase):
    def __init__(self, master):
        super().__init__(master)

        self.add_sub_job_name("Segment Average Generator", row=0)

        # Creates an entry for particles.star file
        input_star_file = self.add_file_entry('star', 'Select a particles.star file', row=1)
        # Creates an entry binning
        bins_entry = self.add_number_entry("Binning (example: 4)", row=2)
        # Creates an entry for input directory with mrcs stack files
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

        # Imports a themed image
        self.add_image("segment_average.jpg", new_size=600, row=6)
