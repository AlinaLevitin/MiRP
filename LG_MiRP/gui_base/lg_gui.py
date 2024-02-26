"""
Author: Alina Levitin
Date: 26/02/24
Version: 1.0

Class to generate GUIs LG-style.
Need to provide a title and an image(optional)
"""
import tkinter as tk
from tkinter import filedialog
import pkg_resources
from PIL import ImageTk, Image  # pillow


class LgGui(tk.Tk):
    """
    A class to create GUI's LG-style
    Inherits from tkinter (tk) Tk class
    """
    def __init__(self, title_name: str = "empty", image_name: str = "missing image"):
        super().__init__()
        # Adding the title, job name and exit button as base GUI
        self.title(title_name)
        self.add_job_name(title_name)
        self.add_exit_button()

        # sets the default image for directory browse as base for GUI (while also resizing it)
        self.browse_image = self.resize_image('directory_icon.png', 20)

        # Adds the images (while also resizing them) - needs to use them as class attributes because of PhotoImage
        # (otherwise it will be garbage collected)
        self.image = self.resize_image(image_name, 600)
        self.add_image()

    def add_job_name(self, title: str):
        """
        Adds the name of the job to the GUI window (always first)

        :param title: string of the job name
        """
        label = tk.Label(self, text=title, font=('Ariel', 18))
        label.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

    def add_image(self, row: int = 10):
        """
        Adds the resized image to the GUI window, row is set to 10
        :param row: int in which row of Tk GUI (as grid) the image will appear
        """

        image_label = tk.Label(self, image=self.image)
        image_label.grid(row=row, column=0, columnspan=5, padx=5, pady=5)

    def add_exit_button(self, row: int = 11):
        button = tk.Button(self, text='Exit', command=self.destroy)
        button.grid(row=row, column=5, columnspan=1, padx=5, pady=5)

    def add_sub_job_name(self, name: str = 'test', row: int = 2):
        label = tk.Label(self, text=name, font=('Ariel', 16))
        label.grid(row=row, column=0, padx=5, pady=5)

    def add_run_button(self, command, row):
        button = tk.Button(self, text='Run', command=command)
        button.grid(row=row, column=1, columnspan=1, padx=5, pady=5)

    @staticmethod
    def browse(file_type, file_entry=None):
        if file_type == 'directory':
            directory = filedialog.askdirectory(title="Select directory")
            if directory:
                file_entry.delete(0, tk.END)
                file_entry.insert(0, directory)
            return directory
        # Open file dialog to select STAR file
        file_path = filedialog.askopenfilename(filetypes=[(f"{file_type.upper()} Files", f"*.{file_type}")])
        if file_path:
            file_entry.delete(0, tk.END)
            file_entry.insert(0, file_path)

    def add_file_entry(self, entry_type, entry_name, row):
        label = tk.Label(self, text=entry_name, font=('Ariel', 12))
        label.grid(row=row, column=0, padx=5, pady=5)

        star_entry = tk.Entry(self, width=50)
        star_entry.grid(row=row, column=1, padx=5, pady=5)

        browse_button = tk.Button(self, text="Browse", command=lambda: self.browse(entry_type, star_entry))
        browse_button.grid(row=row, column=2, padx=5, pady=5)

        return star_entry

    def add_directory_entry(self, entry_name, row):

        label = tk.Label(self, text=entry_name, font=('Ariel', 12))
        label.grid(row=row, column=0, padx=5, pady=5)

        browse_label = tk.Label(self, image=self.browse_image)
        browse_label.grid(row=row, column=3, columnspan=4, padx=5, pady=5)

        directory = tk.Entry(self, width=50)
        directory.grid(row=row, column=1, padx=5, pady=5)
        browse_button = tk.Button(self, text="Browse", command=lambda: self.browse('directory', directory))
        browse_button.grid(row=row, column=2, padx=5, pady=5)

        return directory

    def add_number_entry(self, entry_name, row):
        label = tk.Label(self, text=entry_name, font=('Ariel', 12))
        label.grid(row=row, column=0, padx=5, pady=5)

        number_entry = tk.Entry(self, width=10)
        number_entry.grid(row=row, column=1, padx=5, pady=5)

        return number_entry

    @staticmethod
    def resize_image(image_name: str = "missing image", new_width: int = 100):
        image_stream = pkg_resources.resource_stream('LG_MiRP', f'assets/{image_name}')
        if image_stream:
            image = Image.open(image_stream)

            scale = new_width / image.width
            new_height = int(image.height * scale)
            resized_image = image.resize((new_width, new_height))

            new_image = ImageTk.PhotoImage(resized_image)

            return new_image
