"""
Author: Alina Levitin
Date: 26/02/24
Updated: 11/3/24

Class to generate ttk.Frames LG-style.
"""
import os

import tkinter as tk
from tkinter import ttk

from .utils import *
from .top_level_base import LGTopLevelBase
from LG_MiRP.methods import plot_angles_and_shifts


class LgFrameBase(ttk.Frame):
    """
    A class to create GUI's LG-style
    Inherits from tkinter ttk.Frame class
    """

    def __init__(self, master):
        """
        :param master: master tk.Tk gui (gui_base.master_gui class)
        """
        super().__init__(master)

        self.image = None
        self.output = None
        # Open and resize a tiny folder icon for browse button
        self.browse_image = open_and_resize_browse_image()

    def add_image(self, image_name: str = "default_image.jpg", new_size: int = 600, row: int = 10):
        """
        Adds the resized image to the GUI window, row is set to 10

        :param image_name: selected image name
        :param new_size: in case image needs to be resized, default is 600 since it looks nice
        :param row: int in which row of Tk GUI (as grid) the image will appear
        """
        image_stream = open_image(image_name)
        self.image = resize_image(image_stream, new_size)
        image_label = tk.Label(self, image=self.image)
        image_label.grid(row=row, column=0, columnspan=5, padx=5, pady=5)

    def add_sub_job_name(self, sub_job_name, row: int = 0):
        """
        Adds a title label for the job

        :param sub_job_name: desired title
        :param row: row in the frame
        """
        label = tk.Label(self, text=sub_job_name, font=('Ariel', 16))
        label.grid(row=row, column=0, columnspan=5, padx=5, pady=5)

    def add_run_button(self, command, row, text=None):
        """
        Adds a "Run" button in order to run a function (functions are located in LG_MiRP/methods)

        :param command: desired function
        :param row: row in the frame
        :param text: text located next to the button (optional)
        """
        if text:
            label = tk.Label(self, text=text, font=('Ariel', 12))
            label.grid(row=row, column=0, columnspan=1, padx=5, pady=5)

        button = tk.Button(self, text='Run', command=command)
        button.grid(row=row, column=1, columnspan=1, padx=5, pady=5)

    def add_file_entry(self, entry_type, entry_name, row):
        """
        Adds a file entry with w browse button

        :param entry_type: can be star, mrc, mrcs - passed down to brose function in gui_base.utils
        :param entry_name: text to appear next to the Entry
        :param row: row in the frame
        :return: tk.Entry for downstream operations
        """
        label = tk.Label(self, text=entry_name, font=('Ariel', 12))
        label.grid(row=row, column=0, padx=5, pady=5)

        file_entry = tk.Entry(self, width=50)
        file_entry.grid(row=row, column=1, padx=5, pady=5)

        browse_button = tk.Button(self, text="Browse", command=lambda: browse(entry_type, file_entry))
        browse_button.grid(row=row, column=2, padx=5, pady=5)

        browse_label = tk.Label(self, image=self.browse_image)
        browse_label.grid(row=row, column=3, padx=5, pady=5)

        return file_entry

    def add_directory_entry(self, entry_name, row):
        """
        Adds a directory entry with a browse button

        :param entry_name: text to appear next to the entry
        :param row: row in the frame
        :return: directory entry for downstream operations
        """

        label = tk.Label(self, text=entry_name, font=('Ariel', 12))
        label.grid(row=row, column=0, padx=5, pady=5)

        directory = tk.Entry(self, width=50)
        directory.grid(row=row, column=1, padx=5, pady=5)

        browse_button = tk.Button(self, text="Browse", command=lambda: browse('directory', directory))
        browse_button.grid(row=row, column=2, padx=5, pady=5)

        browse_label = tk.Label(self, image=self.browse_image)
        browse_label.grid(row=row, column=3, padx=5, pady=5)

        return directory

    def add_number_entry(self, entry_name, row):
        """
        Adds a numerical entry

        :param column:
        :param entry_name: text to appear next to the entry
        :param row: row in the frame
        :return: numerical tk.Entry for downstream operations
        """
        label = tk.Label(self, text=entry_name, font=('Ariel', 12))
        label.grid(row=row, column=0, padx=5, pady=5)

        number_entry = tk.Entry(self, width=10)
        number_entry.grid(row=row, column=1, padx=5, pady=5)

        return number_entry

    def add_show_results_button(self, command, row, text="Show Results"):
        button = tk.Button(self, text=text, command=command)
        button.grid(row=row, column=2, columnspan=1, padx=5, pady=5)

    def show_result(self, n=5):

        # Assuming 'grouped_data' is the grouped data from a DataFrame
        grouped_data = self.output.groupby(['rlnMicrographName', 'rlnHelicalTubeID'])

        # Convert the grouped data into a list of tuples (key, grouped DataFrame)
        grouped_data_list = list(grouped_data)

        # Iterate through the first three items in the grouped data list
        for index in range(n):
            # Unpack the key and the grouped DataFrame
            (micrograph, MT), MT_dataframe = grouped_data_list[index]

            # Plot the data at the first item in each group
            fig = plot_angles_and_shifts(MT_dataframe)

            # Create a new window for each plot
            plot_window = LGTopLevelBase(self)
            plot_window.title("Plot of angles")
            plot_window.add_title(text=f"MT {MT} in {micrograph}")
            plot_window.add_plot(fig)

    def display_multiple_mrc_files(self, path, row):
        """
        A method to show the mrc images of the references in a Tkinter top level window
        """
        # File paths
        file_paths = [os.path.join(path, file) for file in os.listdir(path) if file.endswith(".mrc")]

        # The slices that will be displayed since the references mrs files are stacks
        slice_indices = [1 for file in os.listdir(path) if file.endswith(".mrc")]

        # labels to be displayed under the images
        label_text = [file.split("_")[0:2] for file in os.listdir(path) if file.endswith(".mrc")]

        # Shows the mrc images
        for i, (file_path, slice_index, label_text) in enumerate(zip(file_paths, slice_indices, label_text)):
            display_mrc_slice(self, file_path, slice_index, label_text, row=row, column=i)
