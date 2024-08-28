#!/usr/bin/env python3
"""
Author: Alina Levitin
Date: 02/07/24
Updated: 02/07/24

Command to bring up Methods GUI
The GUI is located in LG_MiRP/gui/method_menu_gui

"""

from LG_MiRP import MethodMenuGui, RescaleMaskFrame, MaskGeneratorFrame, KinesinMaskFrame


def main():
    # Generating the gui
    gui = MethodMenuGui('Initial Seam Assignment')
    gui.add_frame(RescaleMaskFrame, 'Rescale Mask')
    gui.add_frame(MaskGeneratorFrame, 'Mask generator')
    gui.add_frame(KinesinMaskFrame, 'Kinesin Mask Generator')
    gui.mainloop()


if __name__ == "__main__":
    main()
