"""
Author: Alina Levitin
Date: 26/02/24
Version: 1.0

Class to generate GUIs LG-style.
"""
import tkinter as tk


class LgMasterGui(tk.Tk):
    """
    A class to create a master GUI's LG-style that will contain a jof ttk.Frame
    Inherits from tkinter (tk) Tk class
    """
    def __init__(self):
        super().__init__()
        # Adding exit button as base GUI
        self.add_exit_button()

    def add_job_name(self, title_name):
        """
        Adds the name of the job to the GUI window (always first)
        """
        self.title(title_name)
        label = tk.Label(self, text=title_name, font=('Ariel', 18))
        label.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

    def add_frame(self, frame, row=1):
        """
        Adding the desired frame to the master gui
        :param frame: ttk.Frame of the required job
        :param row: the row in which the frame will be located
        """
        frame(self).grid(row=row)

    def add_exit_button(self, row: int = 11):
        """
        Adding an exit button to the master gui
        :param row: should always be on the bottom left, therefore the row and the column are set to a high number
        """
        button = tk.Button(self, text='Exit', command=self.destroy)
        button.grid(row=row, column=5, columnspan=1, padx=5, pady=5)
