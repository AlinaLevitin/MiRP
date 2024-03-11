"""
Author: Alina Levitin
Date: 26/02/24
Updated: 10/3/24

Class to generate ttk.Frames LG-style.
"""

import tkinter as tk
from tkinter import filedialog
import pkg_resources
from PIL import ImageTk, Image  # pillow


def open_image(image_name: str = "missing image"):
    image_stream = pkg_resources.resource_stream('LG_MiRP', f'assets/{image_name}')
    if image_stream:
        image = Image.open(image_stream)
        return image


def resize_image(image, new_width: int = 100):
    scale = new_width / image.width
    new_height = int(image.height * scale)
    resized_image = image.resize((new_width, new_height))
    new_image = ImageTk.PhotoImage(resized_image)
    return new_image


def open_and_resize_browse_image():
    browse_image = open_image('directory_icon.png')
    new_browse_image = resize_image(browse_image, 20)
    return new_browse_image


def browse(file_type, file_entry=None):
    # Open a dialog to select a directory
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