#!/usr/bin/env python3
"""
Author: Alina Levitin
Date: 26/02/24
Version: 1.0
"""

import LG_MiRP


segment_average_generation_gui = LG_MiRP.LgMasterGui(title_name="Segment Average", image_name="segment_average.jpg")

segment_average_generation_gui.add_sub_job_name('Segment average generation', row=2)

# segment_average_generation_gui.add_sub_job_name('Scale helical track length', row=2)

input_star_file = segment_average_generation_gui.add_file_entry('star', 'Select a particles.star file', row=3)

bins_entry = segment_average_generation_gui.add_number_entry("Binning (example: 4)", row=4)

input_directory = segment_average_generation_gui.add_directory_entry('Select directory containing extracted particles in Extract', row=5)

# segment_average_generation_gui.add_run_button(lambda: LG_MiRP.scale(input_star_file, int(bins_entry.get())), row=5, text="*Optional")

output_directory = segment_average_generation_gui.add_directory_entry('Select output directory', row=6)

segment_average_generation_gui.add_run_button(lambda: LG_MiRP.preprocess_segment_averages(input_directory,
                                                                                          output_directory,
                                                                                          input_star_file,
                                                                                          binning=bins_entry),
                                              row=7)

segment_average_generation_gui.mainloop()

