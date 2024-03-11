"""
Author: Alina Levitin
Date: 26/02/24
Updated: 11/3/24

Class to generate ttk.Frames LG-style.
"""
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from LG_MiRP.gui_base import utils


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
        # Open and resize a tiny folder icon for browse button
        self.browse_image = utils.open_and_resize_browse_image()

    def add_image(self, image_name: str = "default_image.jpg", new_size: int = 600, row: int = 10):
        """
        Adds the resized image to the GUI window, row is set to 10

        :param image_name: selected image name
        :param new_size: in case image needs to be resized, default is 600 since it looks nice
        :param row: int in which row of Tk GUI (as grid) the image will appear
        """
        image_stream = utils.open_image(image_name)
        self.image = utils.resize_image(image_stream, new_size)
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
            label = tk.Label(self, text=text, font=('Ariel', 16))
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

        browse_button = tk.Button(self, text="Browse", command=lambda: utils.browse(entry_type, file_entry))
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

        browse_button = tk.Button(self, text="Browse", command=lambda: utils.browse('directory', directory))
        browse_button.grid(row=row, column=2, padx=5, pady=5)

        browse_label = tk.Label(self, image=self.browse_image)
        browse_label.grid(row=row, column=3, padx=5, pady=5)

        return directory

    def add_number_entry(self, entry_name, row):
        """
        Adds a numerical entry

        :param entry_name: text to appear next to the entry
        :param row: row in the frame
        :return: numerical tk.Entry for downstream operations
        """
        label = tk.Label(self, text=entry_name, font=('Ariel', 12))
        label.grid(row=row, column=0, padx=5, pady=5)

        number_entry = tk.Entry(self, width=10)
        number_entry.grid(row=row, column=1, padx=5, pady=5)

        return number_entry
