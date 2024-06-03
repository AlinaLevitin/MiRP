"""
Author: Alina Levitin
Date: 10/03/24
Updated: 11/3/24

Two GUI classes (master and frame) for segment average generation
The method of segment averaging is located in LG_MiRP/methods/segment_average_generator
"""
import tkinter as tk
from ..gui_base import LgFrameBase, LgMasterGui, LGTopLevelBase
from ..methods import SegmentAverageGenerator, mt_segment_histogram


class UtilsGui(LgMasterGui):
    """
    A class for the segment average master gui
    Inherits from LgMasterGui
    """
    def __init__(self):
        super().__init__()
        self.add_job_name("Utils")

        self.frames = {}

        # Add menu frame on the left
        self.menu_frame = tk.Frame(self, width=200, bg='lightgrey')
        self.menu_frame.grid(row=0, column=0, rowspan=12, sticky="NS")

        # Main content frame
        self.main_frame = tk.Frame(self)
        self.main_frame.grid(row=0, column=1, rowspan=12, sticky="NSEW")

        self.default_frame = LgFrameBase(self.main_frame)
        self.default_frame.display_image()
        self.default_frame.grid(row=0, column=0, sticky="NSEW")
        self.current_frame = self.default_frame

    def add_frame(self, frame_class, frame_name, row=1):
        """
        Adding the desired frame to the master gui and menu
        :param frame_class: class of the ttk.Frame of the required job
        :param frame_name: name of the frame to display in the menu
        :param row: the row in which the frame will be located
        """
        frame = frame_class(self.main_frame)
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
