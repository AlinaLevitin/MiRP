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


class LgMasterGui(tk.Tk):
    """
    A class to create GUI's LG-style
    Inherits from tkinter (tk) Tk class
    """
    def __init__(self, title_name: str = "empty"):
        super().__init__()
        # Adding the title, job name and exit button as base GUI
        self.title_name = title_name
        self.add_job_name()
        self.title(title_name)
        self.add_exit_button()

    def add_job_name(self):
        """
        Adds the name of the job to the GUI window (always first)
        """
        label = tk.Label(self, text=self.title_name, font=('Ariel', 18))
        label.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

    def add_frame(self, frame, row=1):
        frame(self).grid(row=row)

    def add_exit_button(self, row: int = 11):
        button = tk.Button(self, text='Exit', command=self.destroy)
        button.grid(row=row, column=5, columnspan=1, padx=5, pady=5)
