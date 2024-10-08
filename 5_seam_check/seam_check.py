#!/usr/bin/env python3
"""
Author: Alina Levitin
Date: 01/07/24
Updated: 01/07/24

Command to bring up Methods GUI
The GUI is located in LG_MiRP/gui/method_gui

"""

from LG_MiRP import MethodMenuGui, RescaleReferenceFrame, ClassUnificationFrame, AngleShiftsCorrectionFrame


def main():
    # Generating the gui
    gui = MethodMenuGui('Seam Check')
    gui.add_frame(RescaleReferenceFrame, 'Rescale references', step=gui.get_file_name(__file__))
    gui.add_frame(ClassUnificationFrame, 'Class unification and extraction')
    gui.add_frame(AngleShiftsCorrectionFrame, 'Angle and Shifts Correction')
    gui.mainloop()


if __name__ == "__main__":
    main()
