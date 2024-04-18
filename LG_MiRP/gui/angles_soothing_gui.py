"""
Author: Alina Levitin
Date: 17/04/24
Updated: 18/04/24

Two GUI classes (master and frame) to unifi PHI/Rot (angle smoothing)
The method of angle smoothing is in and extraction is located in LG_MiRP/methods/angle_smoothing

"""
from ..gui_base import LgFrameBase, LgMasterGui, LGTopLevelBase
from ..methods import smooth_angles, plot_angles_and_shifts


class AngleSmoothingGui(LgMasterGui):
    """
    ...
    Inherits from LgMasterGui
    """

    def __init__(self):
        super().__init__()
        self.add_job_name("Angle (PHI/Rot) smoothing")
        frame = AngleSmoothingFrame(self)
        frame.grid(row=1, column=0, sticky="NSEW")
        self.mainloop()


class AngleSmoothingFrame(LgFrameBase):
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
        star_file_input = self.add_file_entry('star', 'Select a run_it001_data.star file', row=1)

        # Creates an entry for output directory
        output_path = self.add_directory_entry('Select output directory', row=2)

        # Creates a "Run" button that uses the class unification and extraction method
        self.add_run_button(lambda: self.run_smooth_angles(star_file_input=star_file_input,
                                                           id_label='rlnAngleRot',
                                                           output_path=output_path),
                            row=3)

        self.add_show_results_button(command=self.show_result, row=4, text="Show PHI for segments")
        # Imports a themed image at the bottom
        self.add_image(image_name="Rot_unification.jpg", new_size=600, row=5)

    def run_smooth_angles(self, star_file_input, id_label, output_path, cutoff=None):
        self.output = smooth_angles(star_file_input=star_file_input, id_label=id_label, output_path=output_path,
                                    cutoff=cutoff)

    def show_result(self, n=5):

        data = []
        for mtIDX, MT_dataframe in self.output.groupby(['rlnMicrographName', 'rlnHelicalTubeID']):
            data.append(MT_dataframe)

        for i in range(n):
            fig = plot_angles_and_shifts(data[i])

            plot_window = LGTopLevelBase(self)
            plot_window.title("Plot of angles")
            plot_window.add_plot(fig)

