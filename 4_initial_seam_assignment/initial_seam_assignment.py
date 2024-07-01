#!/usr/bin/env python3
"""
Author: Alina Levitin
Date: 01/07/24
Updated: 01/07/24

Command to bring up Methods GUI
The GUI is located in LG_MiRP/gui/method_gui

"""

from LG_MiRP import MethodGui, RescaleReferenceFrame, SmoothingFrame, ResetShiftsAnglesFrame


def main():
    # Generating the gui
    gui = MethodGui('Initial Seam Assignment')
    gui.add_frame(RescaleReferenceFrame, 'Rescale References')
    gui.add_frame(ResetShiftsAnglesFrame, 'Angles and Shifts Reset')
    gui.add_frame(SmoothingFrame, 'Angels and Shifts Smoothing')
    gui.mainloop()


if __name__ == "__main__":
    main()
