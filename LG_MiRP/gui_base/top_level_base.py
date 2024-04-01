"""
Author: Alina Levitin
Date: 11/03/24
Updated: 11/3/24

Class to generate tk.TopLevel LG-style.
"""
import tkinter as tk

from LG_MiRP.gui_base import utils
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import ImageTk, Image  # pillow
import mrcfile
import numpy as np


class LGTopLevelBase(tk.Toplevel):
    """
    Class to generate tk.TopLevel LG style
    To create secondary windows
    """
    def __init__(self, master):
        """
        :param master: the master from which the secondary is generated from
        """
        super().__init__(master)
        self.image = None

        # Creating an exit button
        self.add_exit_button()

    def add_plot(self, fig, row: int = 0):
        """
        Adding a plot to the secondary window
        :param fig: plt fig
        :param row: the row in which to display the plot
        """
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=row, column=0)

    def add_image(self, image_name: str = "default_image.jpg", new_size: int = 600, row: int = 1):
        """
        Adds the resized image to the GUI window, row is set to 1

        :param image_name: selected image name
        :param new_size: in case image needs to be resized, default is 600 since it looks nice
        :param row: int in which row of Tk GUI (as grid) the image will appear
        """
        image_stream = utils.open_image(image_name)
        self.image = utils.resize_image(image_stream, new_size)
        image_label = tk.Label(self, image=self.image)
        image_label.grid(row=row, column=0, padx=5, pady=5)

    def display_mrc_slice(self, file_path, slice_index, label_text, row, column):
        # Open the MRC file
        with mrcfile.open(file_path, permissive=True) as mrc:
            # Extract the image data for the specified slice
            image_data = mrc.data[slice_index, :, :]

        # Normalize the image data to [0, 255]
        image_data = (image_data - np.min(image_data)) / (np.max(image_data) - np.min(image_data)) * 255
        image_data = image_data.astype(np.uint8)

        # Convert the image data to PIL Image
        pil_image = Image.fromarray(image_data)

        # Convert the PIL Image to Tkinter PhotoImage
        photo = ImageTk.PhotoImage(pil_image)

        # Create a Tkinter label to display the image
        label = tk.Label(self, image=photo)
        label.grid(row=row, column=column)

        text_label = tk.Label(self, text=label_text)
        text_label.grid(row=row + 1, column=column)  # Adjust the row for the text label

        # Keep a reference to the PhotoImage object to prevent garbage collection
        label.image = photo

    def add_exit_button(self, row: int = 11):
        """
        Adding an exit button to the master gui
        :param row: should always be on the bottom left, therefore the row and the column are set to a high number
        """
        button = tk.Button(self, text='Exit', command=self.destroy)
        button.grid(row=row, column=1, columnspan=1, padx=5, pady=5)
