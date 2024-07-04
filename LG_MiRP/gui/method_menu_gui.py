"""
Author: Alina Levitin
Date: 30/05/24
Updated: 02/07/24

GUI class
"""
import os

import tkinter as tk
from ..gui_base import LgFrameBase, LgMasterGui


class MethodMenuGui(LgMasterGui):
    """
    A class for gui in the form of a menu
    Inherits from LgMasterGui
    """
    def __init__(self, name):
        super().__init__(name)

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

    @staticmethod
    def get_file_name(file):
        return os.path.splitext(os.path.basename(file))[0]