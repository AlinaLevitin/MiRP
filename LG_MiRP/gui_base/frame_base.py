"""
Author: Alina Levitin
Date: 26/02/24
Updated: 10/3/24

Class to generate ttk.Frames LG-style.
"""
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

from LG_MiRP.gui_base import utils


class LgFrameBase(ttk.Frame):
    """
    A class to create GUI's LG-style
    Inherits from tkinter (ttk) Frame class
    """

    def __init__(self, master):
        super().__init__(master)

        self.image = None
        self.browse_image = utils.open_and_resize_browse_image()

    def add_image(self, image_name: str = "missing image", new_size: int = 20, row: int = 10):
        """
        Adds the resized image to the GUI window, row is set to 10
        :param image_name: selected image name
        :param new_size: in case image needs to be resized
        :param row: int in which row of Tk GUI (as grid) the image will appear
        """
        image_stream = utils.open_image(image_name)
        self.image = utils.resize_image(image_stream, new_size)
        image_label = tk.Label(self, image=self.image)
        image_label.grid(row=row, column=0, columnspan=5, padx=5, pady=5)

    def add_sub_job_name(self, sub_job_name, row: int = 0):
        label = tk.Label(self, text=sub_job_name, font=('Ariel', 16))
        label.grid(row=row, column=0, padx=5, pady=5)

    def add_run_button(self, command, row, text=None, ):
        if text:
            label = tk.Label(self, text=text, font=('Ariel', 16))
            label.grid(row=row, column=0, columnspan=1, padx=5, pady=5)

        button = tk.Button(self, text='Run', command=command)
        button.grid(row=row, column=1, columnspan=1, padx=5, pady=5)

    # @staticmethod
    # def browse(file_type, file_entry=None):
    #     # Open a dialog to select a directory
    #     if file_type == 'directory':
    #         directory = filedialog.askdirectory(title="Select directory")
    #         if directory:
    #             file_entry.delete(0, tk.END)
    #             file_entry.insert(0, directory)
    #         return directory
    #     # Open file dialog to select STAR file
    #     file_path = filedialog.askopenfilename(filetypes=[(f"{file_type.upper()} Files", f"*.{file_type}")])
    #     if file_path:
    #         file_entry.delete(0, tk.END)
    #         file_entry.insert(0, file_path)

    def add_file_entry(self, entry_type, entry_name, row):
        label = tk.Label(self, text=entry_name, font=('Ariel', 12))
        label.grid(row=row, column=0, padx=5, pady=5)

        star_entry = tk.Entry(self, width=50)
        star_entry.grid(row=row, column=1, padx=5, pady=5)

        browse_label = tk.Label(self, image=self.browse_image)
        browse_label.grid(row=row, column=3, columnspan=4, padx=5, pady=5)

        browse_button = tk.Button(self, text="Browse", command=lambda: utils.browse(entry_type, star_entry))
        browse_button.grid(row=row, column=2, padx=5, pady=5)

        return star_entry

    def add_directory_entry(self, entry_name, row):

        label = tk.Label(self, text=entry_name, font=('Ariel', 12))
        label.grid(row=row, column=0, padx=5, pady=5)

        browse_label = tk.Label(self, image=self.browse_image)
        browse_label.grid(row=row, column=3, columnspan=4, padx=5, pady=5)

        directory = tk.Entry(self, width=50)
        directory.grid(row=row, column=1, padx=5, pady=5)
        browse_button = tk.Button(self, text="Browse", command=lambda: utils.browse('directory', directory))
        browse_button.grid(row=row, column=2, padx=5, pady=5)

        return directory

    def add_number_entry(self, entry_name, row):
        label = tk.Label(self, text=entry_name, font=('Ariel', 12))
        label.grid(row=row, column=0, padx=5, pady=5)

        number_entry = tk.Entry(self, width=10)
        number_entry.grid(row=row, column=1, padx=5, pady=5)

        return number_entry
