"""
Author: Alina Levitin
Date: 26/02/24
Updated: 09/06/24

Class to generate ttk.Frames LG-style.
"""
import os
import random

import tkinter as tk
from tkinter import ttk
import pandas as pd

from functools import wraps

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
        self.input = pd.DataFrame()
        self.output = pd.DataFrame()
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

    def add_file_entry(self, entry_type, entry_name, row, default_value=""):
        """
        Adds a file entry with a browse button.

        :param entry_type: can be star, mrc, mrcs - passed down to browse function in gui_base.utils
        :param entry_name: text to appear next to the Entry
        :param row: row in the frame
        :param default_value: the default value to be set in the Entry (optional)
        :return: tk.Entry for downstream operations
        """
        label = tk.Label(self, text=entry_name, font=('Ariel', 12))
        label.grid(row=row, column=0, padx=5, pady=5)

        file_entry = tk.Entry(self, width=50)
        file_entry.grid(row=row, column=1, padx=5, pady=5)

        # Set the default value if provided
        if default_value:
            file_entry.insert(0, default_value)

        browse_button = tk.Button(self, text="Browse", command=lambda: browse(entry_type, file_entry))
        browse_button.grid(row=row, column=2, padx=5, pady=5)

        browse_label = tk.Label(self, image=self.browse_image)
        browse_label.grid(row=row, column=3, padx=5, pady=5)

        return file_entry

    def add_directory_entry(self, entry_name, row, command=None):
        """
        Adds a directory entry with a browse button

        :param command:
        :param entry_name: text to appear next to the entry
        :param row: row in the frame
        :return: directory entry for downstream operations
        """

        label = tk.Label(self, text=entry_name, font=('Ariel', 12))
        label.grid(row=row, column=0, padx=5, pady=5)

        directory = tk.Entry(self, width=50)
        directory.grid(row=row, column=1, padx=5, pady=5)

        browse_button = tk.Button(self, text="Browse", command=lambda: browse('directory', directory, command=command))
        browse_button.grid(row=row, column=2, padx=5, pady=5)

        browse_label = tk.Label(self, image=self.browse_image)
        browse_label.grid(row=row, column=3, padx=5, pady=5)

        return directory

    def add_number_entry(self, entry_name, row, default_value=None):
        """
        Adds a numerical entry

        :param entry_name: text to appear next to the entry
        :param row: row in the frame
        :param default_value: the default value to be set in the Entry (optional)
        :return: numerical tk.Entry for downstream operations
        """
        label = tk.Label(self, text=entry_name, font=('Ariel', 12))
        label.grid(row=row, column=0, padx=5, pady=5)

        number_entry = tk.Entry(self, width=10)
        number_entry.grid(row=row, column=1, padx=5, pady=5)

        # Set the default value if provided
        if default_value is not None:
            number_entry.insert(0, str(default_value))

        return number_entry

    def add_show_results_button(self, command, row, text="Show Results", column=2):
        button = tk.Button(self, text=text, command=command)
        button.grid(row=row, column=column, columnspan=1, padx=5, pady=5)

    def show_angle_and_shifts_plot(self, n=10):
        # Assuming 'grouped_data' is the grouped data from a DataFrame
        grouped_data = self.output.groupby(['rlnMicrographName', 'rlnHelicalTubeID'])

        # Convert the grouped data into a list of tuples (key, grouped DataFrame)
        grouped_data_list = list(grouped_data)
        num_groups = len(grouped_data_list)

        selected_indices = random.sample(range(num_groups), n)

        # Iterate through the selected items in the grouped data list
        for index in selected_indices:
            # Unpack the key and the grouped DataFrame
            (micrograph, MT), MT_dataframe = grouped_data_list[index]

            # Plot the output data
            fig_output = plot_angles_and_shifts(MT_dataframe)

            if not self.input.empty:
                # Assuming 'grouped_data_input' is the grouped data from the input DataFrame
                grouped_data_input = self.input.groupby(['rlnMicrographName', 'rlnHelicalTubeID'])
                grouped_data_list_input = list(grouped_data_input)

                # Find the corresponding input DataFrame
                input_dataframe = pd.DataFrame()
                for (micrograph_input, MT_input), df in grouped_data_list_input:
                    if micrograph_input == micrograph and MT_input == MT:
                        input_dataframe = df
                        break

                if not input_dataframe.empty:
                    fig_input = plot_angles_and_shifts(input_dataframe)
                else:
                    fig_input = None
            else:
                fig_input = None

            # Create a new window for each plot
            plot_window = LGTopLevelBase(self)
            plot_window.title("Plot of angles")
            plot_window.add_title(text=f"MT {MT} in {micrograph}")

            if fig_input:
                plot_window.add_title(text='Before smoothing/correcting', row=1)
                plot_window.add_plot(fig_input, row=2)
                plot_window.add_title(text='After smoothing/correcting', row=3)
            plot_window.add_plot(fig_output, row=4)

    def display_multiple_mrc_files(self, path, row):
        """
        A method to show the mrc images of the references in a Tkinter top level window
        """
        # File paths
        # file_paths = [os.path.join(path, file) for file in os.listdir(path) if file.endswith(".mrc")]
        file_paths = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".mrc"):
                    file_paths.append(os.path.join(root, file))

        if not file_paths:
            raise ValueError("No .mrc files found in the specified path.")

        # labels to be displayed under the images
        base_names = [os.path.basename(file) for file in file_paths]
        label_text = [file.split("_")[0:2] for file in base_names]

        # Define the maximum number of columns
        max_columns = 6

        # Shows the mrc images
        for i, (file_path, label_text) in enumerate(zip(file_paths, label_text)):
            # Calculate the row and column index
            show_row = row + (i // max_columns) * 2
            column = i % max_columns

            # Display the mrc stack
            display_mrc_stack(self, file_path, label_text, row=show_row, column=column)

    def add_method_combobox(self, row, options, on_method_change=None, text='Method:'):
        label = tk.Label(self, text=text, font=('Ariel', 12))
        label.grid(row=row, column=0)
        method_var = tk.StringVar(value=options[0])
        method_combobox = ttk.Combobox(self, textvariable=method_var)
        method_combobox['values'] = options
        method_combobox.grid(row=row, column=1)

        if on_method_change:
            # Bind the combobox selection change to the add_image_by_name method
            method_combobox.bind("<<ComboboxSelected>>", self.on_method_change)

        return method_var

    def on_method_change(self, event):
        pass

    def display_image(self):
        image_stream = open_image("default_image.jpg")
        self.image = resize_image(image_stream, 600)
        image_label = tk.Label(self, image=self.image)
        image_label.grid(row=0, column=0, padx=10, pady=10)


# =======================================================================================================================
# Decorators:

def check_parameters(required_params):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            missing_params = []

            for param in required_params:
                value = getattr(self, param, None)
                if value is None or not value.get():
                    missing_params.append(param.replace('_', ' '))

            if missing_params:
                for param in missing_params:
                    print(f"Please provide {param}")
                print(50 * "=")
                return

            return func(self, *args, **kwargs)

        return wrapper

    return decorator
