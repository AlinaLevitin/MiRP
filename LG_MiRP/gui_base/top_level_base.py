"""
Author: Alina Levitin
Date: 11/03/24
Updated: 11/3/24

Class to generate tk.TopLevel LG-style.
"""
import tkinter as tk

from LG_MiRP.gui_base import utils
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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

    def add_title(self, text, row=0):
        """
        Adds a title label at the top of the window

        :param text: desired text
        :param row: selected row to display the title (default is 0 - first row)
        """
        label = tk.Label(self, text=text, font=('Ariel', 12))
        label.grid(row=row, column=0, padx=5, pady=5)

    def add_plot(self, fig, row: int = 1):
        """
        Adding a plot to the secondary window
        :param fig: plt fig
        :param row: the row in which to display the plot
        """
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=row, column=0)

    def add_image(self, image_name: str = "default_image.jpg", new_size: int = 600, row: int = 2):
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

    def add_exit_button(self, row: int = 11):
        """
        Adding an exit button to the master gui
        :param row: should always be on the bottom left, therefore the row and the column are set to a high number
        """
        button = tk.Button(self, text='Exit', command=self.destroy)
        button.grid(row=row, column=1, columnspan=1, padx=5, pady=5)
