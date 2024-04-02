"""
Author: Alina Levitin
Date: 28/03/24
Updated: 02/04/24

Two GUI classes (master and frame) for class reference rescaling
The method of reference rescaling is located in LG_MiRP/methods/reference_scaler
"""
import os
import tkinter as tk

from ..gui_base import LgFrameBase, LgMasterGui, LGTopLevelBase
from ..methods import rescale_and_crop_image


class RescaleReferencesGui(LgMasterGui):
    """
    ...
    Inherits from LgMasterGui
    """

    def __init__(self, path):
        super().__init__()
        self.add_job_name("Rescale References")
        frame = RescaleReferenceFrame(self, path)
        frame.grid(row=1, column=0, sticky="NSEW")
        self.mainloop()


class RescaleReferenceFrame(LgFrameBase):
    """
    ...
    Inherits from LgFrameBase
    """

    def __init__(self, master, path):
        """
        :param master: the master gui in which the frame will be displayed
        """
        self.path = path
        super().__init__(master)
        # Adds the job name at the top row
        # self.add_sub_job_name("Rescale References", row=0)

        input_pixel_size = self.add_number_entry("Pixel size", row=1)

        input_box_size = self.add_number_entry("Box size", row=2)

        output_directory = self.add_directory_entry('Select output directory', row=3)
        # Creates a "Run" button that uses the segment average method
        self.add_run_button(lambda: rescale_and_crop_image(self.path,
                                                           input_pixel_size,
                                                           input_box_size,
                                                           output_directory
                                                           ),
                            row=4)

        # Generating a button to show the references images in a separated window
        mrc_image_button = tk.Button(self, text="Show mrc references",
                                     command=lambda: self.display_multiple_mrc_files())
        mrc_image_button.grid(row=5, column=0)

        # Imports a themed image at the bottom
        self.add_image("default_image.jpg", new_size=600, row=6)

    def display_multiple_mrc_files(self):
        """
        A method to show the mrc images of the references in a Tkinter top level window
        """
        # Creating a new Tkinter top level window
        reference_window = LGTopLevelBase(self)
        # Adding a title
        reference_window.title("References")

        # File paths
        file_paths = [os.path.join(self.path, file) for file in os.listdir(self.path) if file.endswith(".mrc")]

        # The slices that will be displayed since the references mrs files are stacks
        slice_indices = [1 for file in os.listdir(self.path) if file.endswith(".mrc")]

        # labels to be displayed under the images
        label_text = [file.split("_")[0:2] for file in os.listdir(self.path) if file.endswith(".mrc")]

        # Shows the mrc images
        for i, (file_path, slice_index, label_text) in enumerate(zip(file_paths, slice_indices, label_text)):
            reference_window.display_mrc_slice(file_path, slice_index, label_text, row=0, column=i)
