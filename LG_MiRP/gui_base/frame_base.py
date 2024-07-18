"""
Author: Alina Levitin
Date: 26/02/24
Updated: 17/07/24

Class to generate ttk.Frames LG-style.
"""
import os
import random

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
        :param master: master tk.Tk gui (gui_base.LgMasterGui class in master_gui.py) that will contain the frame
        """
        super().__init__(master)

        self.image = None
        self.input = pd.DataFrame()
        self.output = pd.DataFrame()
        # Open and resize a tiny 'folder' icon for browse button
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

    def add_run_button(self, row, command=None, text=None):
        """
        Adds a "Run" button in order to run a function (functions are located in LG_MiRP/methods)

        :param command: desired function
        :param row: row in the frame
        :param text: text located next to the button (optional)
        """
        if text:
            label = tk.Label(self, text=text, font=('Ariel', 12))
            label.grid(row=row, column=0, columnspan=1, padx=5, pady=5)

        if command:
            button = tk.Button(self, text='Run', command=command)
        else:
            button = tk.Button(self, text='Run', command=self.run_function)
        button.grid(row=row, column=1, columnspan=1, padx=5, pady=5)

    def run_function(self):
        """
        Place-holder for function to be run when user clicks the run button
        """
        pass

    def add_file_entry(self, entry_type, entry_name, row, default_value="", command=None):
        """
        Adds a file entry with a browse button.

        :param command:
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

        browse_button = tk.Button(self, text="Browse", command=lambda: browse(entry_type, file_entry, command=command))
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
        """
        Adds a button to show plots (very similar to run button, I don't remember why I felt the need to have both)

        :param command: the function to run when pressing the button
        :param row: selected row in the frame to display the button
        :param text: selected test to display on the left of the button (default is "Show Results"
        :param column: column to show the button on, default is 2
        """
        button = tk.Button(self, text=text, command=command)
        button.grid(row=row, column=column, columnspan=1, padx=5, pady=5)

    def show_angle_and_shifts_plot(self, n=10):
        """
        Generates a matplot lib fig with 4 subplots for rot, tilt, psi and X/Y shifts as a function of segment number
        for n random microtubules in the data set in new sub-windows (tk.TopLevel)
        Uses plot_angles_and_shifts method from plost_functions.py in methods folder

        :param n: number of MTs to display plots for
        """
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

    def display_multiple_mrc_files(self, path, row, max_columns=6):
        """
        A method to show the mrc images of the references in a Tkinter top level window
        Uses display_mrc_stack method from

        :param path: mrc files path
        :param row: the row in which to display the mrc images
        :param max_columns: the maximum number of columns to display (default is six)
        """

        # Getting all files in the path (even in nested directories - just in case)
        file_paths = []
        for root, dirs, files in os.walk(path.get()):
            for file in files:
                if file.endswith(".mrc"):
                    file_paths.append(os.path.join(root, file))

        if not file_paths:
            raise ValueError("No .mrc files found in the specified path.")

        # labels to be displayed under the images
        base_names = [os.path.basename(file) for file in file_paths]
        label_text = [file.split("_")[0:2] for file in base_names]

        # Shows the mrc images
        for i, (file_path, label_text) in enumerate(zip(file_paths, label_text)):
            # Calculate the row and column index
            show_row = row + (i // max_columns) * 2
            column = i % max_columns

            # Display the mrc stack
            display_mrc_stack(self, file_path, label_text, row=show_row, column=column)

    def display_single_mrc_files(self, path, row=1):
        """
        A method to show the mrc images of the references in a Tkinter top level window

        :param path: path of the mrc file
        :param row: selected row, default is 1
        """

        file_path = path.get()

        if not file_path:
            raise ValueError("No .mrc files found in the specified path.")

        # labels to be displayed under the images
        base_name = os.path.basename(file_path)
        label_text = base_name.split("_")[0:2]

        # Shows the mrc images
        display_mrc_stack(self, file_path, label_text, row=row, column=0)

    def add_method_combobox(self, row, options, on_method_change=None, text='Method:'):
        """
        Creates a dropdown menu (ttk.Combobox) at a selected row with the options list as the menu next to the selected
        text
        Optionally will change something in the gui (method or image or both) when a specific option is selected
        (on_method_change)

        :param row: row number in the frame
        :param options: list of options, the first item in the list will appear as the default option
        :param on_method_change: True or None/False
        :param text: text to be displayed on the left of the combobox

        :return: selected option from the dropdown menu
        """
        # Creating a label with the desired text at the desired row
        label = tk.Label(self, text=text, font=('Ariel', 12))
        label.grid(row=row, column=0)

        # Sets the default option as the first item in the options list
        selected_option = tk.StringVar(value=options[0])
        method_combobox = ttk.Combobox(self, textvariable=selected_option)

        # Sets the options in the dropdown menu
        method_combobox['values'] = options
        method_combobox.grid(row=row, column=1)

        if on_method_change:
            # Bind the combobox selection change to the add_image_by_name method
            method_combobox.bind("<<ComboboxSelected>>", self.on_combobox_select)

        return selected_option

    def on_combobox_select(self, event):
        """
        This is used to change the displayed image or method (or both)as a result of changing options in the dropdown
        menu.
        Since this may change for different steps, the method here is kept empty and is added on gui classes that
        inherit from this class
        """
        pass

    def display_image(self):
        """
        Used for MethodMenuGui (in gui.method_menu_gui.py) to display a default image when used is opening the gui
        """
        image_stream = open_image("default_image.jpg")
        self.image = resize_image(image_stream, 600)
        image_label = tk.Label(self, image=self.image)
        image_label.grid(row=0, column=0, padx=10, pady=10)


# =======================================================================================================================
# Decorators:

def check_parameters(required_params):
    """
    Decorator to check if all the parameters are filled before trying to run a function.
    Used in all guis to check if the used filled the required boxes before executing self.run_function()
    """
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
                    print(f"WARNING! Missing parameter: please provide {param}")
                print(50 * "=")
                return

            return func(self, *args, **kwargs)

        return wrapper

    return decorator
