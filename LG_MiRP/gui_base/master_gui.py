"""
Author: Alina Levitin
Date: 26/02/24
Updated: 11/3/24

Class to generate GUIs LG-style.
"""
import tkinter as tk

from .top_level_base import LGTopLevelBase


class LgMasterGui(tk.Tk):
    """
    A class to create a master GUI's LG-style that will contain a jof ttk.Frame
    Inherits from tkinter (tk) Tk class
    """
    def __init__(self, name):
        super().__init__()
        self.add_gui_name(name)

        self.frames = {}

        # Add menu frame on the left
        self.menu_frame = None

        # Main content frame
        self.main_frame = None

        self.current_frame = None

        # Adding exit button as base GUI
        self.add_exit_button()
        self.add_complete_pipeline_button()

    def add_job_name(self, name):
        label = tk.Label(self, text=name, font=('Ariel', 18))
        label.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

    def add_gui_name(self, title_name):
        """
        Adds the name of the job to the GUI window (always first)
        """
        self.title(title_name)

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
        Raise the specified frame
        :param frame_name: name of the frame to raise
        """
        if self.current_frame:
            self.current_frame.grid_remove()
        self.current_frame = self.frames[frame_name]
        self.current_frame.grid()

    def add_exit_button(self, row: int = 15):
        """
        Adding an exit button to the master gui
        :param row: should always be on the bottom left, therefore the row and the column are set to a high number
        """
        button = tk.Button(self, text='Exit', command=self.destroy)
        button.grid(row=row, column=5, columnspan=1, padx=5, pady=5)

    def add_complete_pipeline_button(self, row: int = 15):
        """
        Adding an exit button to the master gui
        :param row: should always be on the bottom left, therefore the row and the column are set to a high number
        """
        button = tk.Button(self, text="Complete Pipeline illustration", command=self.open_complete_pipeline)
        button.grid(row=row, column=0, columnspan=2, padx=5, pady=5, sticky="SE")

    def open_complete_pipeline(self):
        complete_pipeline_top_level = LGTopLevelBase(self)
        complete_pipeline_top_level.title("Complete Pipeline")
        complete_pipeline_top_level.add_image("complete_pipeline.jpg", 400)
