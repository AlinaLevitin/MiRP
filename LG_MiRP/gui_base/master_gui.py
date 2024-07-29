"""
Author: Alina Levitin
Date: 26/02/24
Updated: 11/3/24

Class to generate GUIs LG-style.
"""
import tkinter as tk
from tkinter import ttk
from .top_level_base import LGTopLevelBase


class LgMasterGui(tk.Tk):
    """
    A class to create a master GUI's LG-style that will contain a jof ttk.Frame
    Inherits from tkinter (tk) Tk class
    """

    def __init__(self, name):
        """
        :param name: Selected name that will appear at the top of the window
        """
        super().__init__()
        # Sets the name of the gui
        self.title(name)

        # Make the window resizable
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Sets an empty dictionary for frames in menu-style gui
        self.frames = {}

        # Add menu frame on the left
        self.menu_frame = ttk.Frame(self)
        self.menu_frame.grid(row=1, column=0, sticky="NS")
        self.menu_frame.grid_columnconfigure(0, weight=1)

        # Main content frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=1, column=1, sticky="NSEW")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Frame to be displayed in the main frame
        self.current_frame = None

        # Adding exit button as base GUI
        self.add_exit_button()
        # Adding a button to display an illustration of the pipeline
        self.add_complete_pipeline_button()

    def add_job_name(self, name):
        """
        Adds a label as a title at the top of the window

        :param name: desired name
        """
        label = tk.Label(self, text=name, font=('Ariel', 18))
        label.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="EW")

    def add_exit_button(self, row: int = 15):
        """
        Adding an exit button to the master gui
        :param row: should always be on the bottom left, therefore the row and the column are set to a high number
        """
        button = tk.Button(self, text='Exit', command=self.destroy)
        button.grid(row=row, column=5, columnspan=1, padx=5, pady=5, sticky="SE")

    def add_complete_pipeline_button(self, row: int = 15):
        """
        Adding an exit button to the master gui
        :param row: should always be on the bottom left, therefore the row and the column are set to a high number
        """
        button = tk.Button(self, text="Complete Pipeline illustration", command=self.open_complete_pipeline)
        button.grid(row=row, column=0, columnspan=2, padx=5, pady=5, sticky="SE")

    def open_complete_pipeline(self):
        """
        Opens a secondary window with image of the complete pipeline
        """
        complete_pipeline_top_level = LGTopLevelBase(self)
        complete_pipeline_top_level.title("Complete Pipeline")
        complete_pipeline_top_level.add_image("complete_pipeline.jpg", 400)

    # ==================================================================================================================
    # Methods for menu-style gui
    def add_frame(self, frame_class, frame_name, row=1, **kwargs):
        """
        Adding the desired frame to the master gui and menu
        :param frame_class: class of the ttk.Frame of the required job
        :param frame_name: name of the frame to display in the menu
        :param row: the row in which the frame will be located
        """
        frame = frame_class(self.main_frame, **kwargs)
        self.frames[frame_name] = frame
        frame.grid(row=row, column=1, sticky="NSEW")
        frame.grid_remove()

        # Add button to menu to raise the frame
        button = tk.Button(self.menu_frame, text=frame_name, command=lambda: self.raise_frame(frame_name))
        button.pack(fill="x", padx=5, pady=5)

    def raise_frame(self, frame_name):
        """
        Raise the specified frame when user is pressing the corresponding button in the menu

        :param frame_name: name of the frame to raise
        """
        if self.current_frame:
            self.current_frame.grid_remove()
        self.current_frame = self.frames[frame_name]
        self.current_frame.grid(sticky="NSEW")
        self.update_idletasks()
        self.geometry(f"{self.winfo_width()}x{self.winfo_height()}")
