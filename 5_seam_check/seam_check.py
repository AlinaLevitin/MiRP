#!/usr/bin/env python3
"""
Author: Alina Levitin
Date: 01/07/24
Updated: 01/07/24

Command to bring up Methods GUI
The GUI is located in LG_MiRP/gui/method_gui

"""

from LG_MiRP import MethodGui, RescaleReferenceFrame, ClassUnificationFrame, AngleShiftsCorrectionFrame


def main():
    # Generating the gui
    gui = MethodGui('Seam Check')
    gui.add_frame(RescaleReferenceFrame, 'Rescale references')
    gui.add_frame(ClassUnificationFrame, 'Class unification and extraction')
    gui.add_frame(AngleShiftsCorrectionFrame, 'Angle and Shifts Correction')
    gui.mainloop()


if __name__ == "__main__":
    main()
