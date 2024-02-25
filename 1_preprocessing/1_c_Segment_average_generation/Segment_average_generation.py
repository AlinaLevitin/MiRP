import LG_MiRP


segment_average_generation_gui = LG_MiRP.LgGui(title_name="Segment Average")

segment_average_generation_gui.add_image(image_name="segment_average.jpg")

segment_average_generation_gui.add_sub_job_name('Scale helical track length', row=2)

input_star_file = segment_average_generation_gui.add_star_file_entry(row=3)

segment_average_generation_gui.add_run_button(lambda: LG_MiRP.scale(input_star_file), row=4)


segment_average_generation_gui.mainloop()

