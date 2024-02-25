"""
Author: Alina Levitin
Date: 22/02/24
Version: 1.0
"""

import tkinter as tk
from tkinter import filedialog
import pkg_resources
from PIL import ImageTk, Image

import starfile


class LgGui(tk.Tk):
    def __init__(self, title_name: str = "empty", **kwargs):
        super().__init__()

        self.geometry("630x800")
        self.title(title_name)
        self.add_job_name(title_name)

    def add_job_name(self, title):
        label = tk.Label(self, text=title, font=('Ariel', 18))
        label.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

    def add_image(self, image_name: str = "missing image"):
        image_stream = pkg_resources.resource_stream('LG_MiRP', f'assets/{image_name}')
        image = Image.open(image_stream)

        scale = float(600 / image.width)
        new_width = 600  # Set the desired width
        new_height = int(image.height*scale)  # Set the desired height
        resized_image = image.resize((new_width, new_height))

        self.img = ImageTk.PhotoImage(resized_image)
        self.imlabel = tk.Label(self, image=self.img)
        self.imlabel.grid(row=7, column=0, columnspan=4, padx=5, pady=5)

    def add_sub_job_name(self, name: str = 'test', row: int = 2):
        label = tk.Label(self, text=name, font=('Ariel', 16))
        label.grid(row=row, column=0, padx=5, pady=5)

    def add_run_button(self, command, row):
        button = tk.Button(self, text='Run', command=command)
        button.grid(row=row, column=0, columnspan=4, padx=5, pady=5)

    @staticmethod
    def browse_star_files(file_type, file_entry):
        # Open file dialog to select STAR file
        file_path = filedialog.askopenfilename(filetypes=[(f"{file_type.upper()} Files", f"*.{file_type}")])
        if file_path:
            file_entry.delete(0, tk.END)
            file_entry.insert(0, file_path)

    def add_star_file_entry(self, entry_name, row):
        label = tk.Label(self, text=entry_name, font=('Ariel', 12))
        label.grid(row=row, column=0, padx=5, pady=5)

        star_entry = tk.Entry(self, width=50)
        star_entry.grid(row=row, column=1, padx=5, pady=5)

        browse_button = tk.Button(self, text="Browse", command=lambda: self.browse_star_files("star", star_entry))
        browse_button.grid(row=row, column=2, padx=5, pady=5)

        return star_entry

    def add_number_entry(self, entry_name, row):
        label = tk.Label(self, text=entry_name, font=('Ariel', 12))
        label.grid(row=row, column=0, padx=5, pady=5)

        number_entry = tk.Entry(self, width=10)
        number_entry.grid(row=row, column=1, padx=5, pady=5)

        return number_entry
