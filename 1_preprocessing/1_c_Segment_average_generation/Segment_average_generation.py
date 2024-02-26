import LG_MiRP


segment_average_generation_gui = LG_MiRP.LgGui(title_name="Segment Average", image_name="segment_average.jpg")

segment_average_generation_gui.add_sub_job_name('Scale helical track length', row=2)

input_star_file = segment_average_generation_gui.add_file_entry('star', 'Select a particles.star file', row=3)

scale_entry = segment_average_generation_gui.add_number_entry("Scale factor (example: 0.25)", row=4)

segment_average_generation_gui.add_run_button(lambda: LG_MiRP.scale(input_star_file, float(scale_entry.get())), row=5)

segment_average_generation_gui.add_sub_job_name('Segment average generation', row=6)

directory = segment_average_generation_gui.add_directory_entry('Select directory containing extracted particles (Extract)',row=7)


segment_average_generation_gui.mainloop()

