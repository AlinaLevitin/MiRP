"""
Author: Alina Levitin
Date: 11/03/24
Updated: 1/4/24

Utilization functions for gui_base
"""

import tkinter as tk
from tkinter import filedialog
from pkg_resources import resource_stream
from PIL import ImageTk, Image  # pillow
import mrcfile
import numpy as np


def open_image(image_name: str = "missing image"):
    """
    Open image using resource_stream

    :param image_name: string name of image in LG_MiRP/assets
    :return: Image
    """
    image_stream = resource_stream('LG_MiRP', f'assets/{image_name}')
    if image_stream:
        image = Image.open(image_stream)

        return image


def resize_image(image, new_width: int = 100):
    """
    Resizing the image according to desired width

    :param image: Image input after opening with open_image function
    :param new_width: desired new width
    :return: PhotoImage Image
    """
    scale = new_width / image.width
    new_height = int(image.height * scale)
    resized_image = image.resize((new_width, new_height))
    new_image = ImageTk.PhotoImage(resized_image)

    return new_image


def open_and_resize_browse_image():
    """
    Opening and resizing a small browse image (tiny folder icon)

    :return: tiny folder image
    """
    browse_image = open_image('directory_icon.png')
    new_browse_image = resize_image(browse_image, 20)

    return new_browse_image


def browse(file_type, file_entry=None, command=None):
    """
    Browsing function using filedialog from tk

    :param command:
    :param file_type: file type can be star, mrc, mrcs, directory,
                        when browsing it will show only the selected file type
    :param file_entry: tk.Entry in order to insert the selected file/directory in the entry
    :return: if file_type is a directory then returns the directory entry for downstream operations
    """
    # Open a dialog to select a directory
    if file_type == 'directory':
        directory = filedialog.askdirectory(title="Select directory")
        if directory:
            file_entry.delete(0, tk.END)
            file_entry.insert(0, directory)
            if command:
                command()

        return directory

    # Open file dialog to select a file according to the file_type
    file_path = filedialog.askopenfilename(filetypes=[(f"{file_type.upper()} Files", f"*.{file_type}")])
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)
        if command:
            command()


def display_mrc_slice(master, file_path, slice_index, label_text, row, column):
    # Open the MRC file
    with mrcfile.open(file_path, permissive=True) as mrc:
        # Extract the image data for the specified slice
        image_data = mrc.data[slice_index, :, :]

        # Normalize the image data to [0, 255]
        min_value = np.min(image_data)
        max_value = np.max(image_data)
        normalized_data = (image_data - min_value) / (max_value - min_value) * 255
        image_data_uint8 = normalized_data.astype(np.uint8)

    # Convert the image data to PIL Image
    pil_image = Image.fromarray(image_data_uint8)

    # Convert the PIL Image to Tkinter PhotoImage
    photo = ImageTk.PhotoImage(pil_image)

    # Create a Tkinter label to display the image and place it in the frame
    image_label = tk.Label(master, image=photo)
    image_label.grid(row=row, column=column)

    # Create a text label and place it below the image in the frame
    text_label = tk.Label(master, text=label_text)
    text_label.grid(row=row + 1, column=column)

    # Keep a reference to the PhotoImage object to prevent garbage collection
    image_label.photo = photo


def display_mrc_stack(master, file_path, label_text, row, column):
    # Open the MRC file
    with mrcfile.open(file_path, permissive=True) as mrc:
        # Extract the image data for the specified slice
        image_data = mrc.data[:, :, :]

        z_projected_image = np.max(image_data, axis=0)

        # Normalize the image data to [0, 255]
        min_value = np.min(z_projected_image)
        max_value = np.max(z_projected_image)
        normalized_data = (z_projected_image- min_value) / (max_value - min_value) * 255
        image_data_uint8 = normalized_data.astype(np.uint8)

    # Convert the image data to PIL Image
    pil_image = Image.fromarray(image_data_uint8)

    # Convert the PIL Image to Tkinter PhotoImage
    photo = ImageTk.PhotoImage(pil_image)

    # Create a Tkinter label to display the image and place it in the frame
    image_label = tk.Label(master, image=photo)
    image_label.grid(row=row, column=column)

    # Create a text label and place it below the image in the frame
    text_label = tk.Label(master, text=label_text)
    text_label.grid(row=row + 1, column=column)

    # Keep a reference to the PhotoImage object to prevent garbage collection
    image_label.photo = photo
