#!/usr/bin/env python3
"""
Author: Alina Levitin
Date: 02/07/24
Updated: 02/07/24

Command to bring up Methods GUI
The GUI is located in LG_MiRP/gui/method_menu_gui

"""

from LG_MiRP import MethodMenuGui, RescaleReferenceFrame, MaskGeneratorFrame


def main():
    # Generating the gui
    gui = MethodMenuGui('Initial Seam Assignment')
    gui.add_frame(RescaleReferenceFrame, 'Rescale References', step=gui.get_file_name(__file__))
    gui.add_frame(MaskGeneratorFrame, 'Mask generator')
    gui.mainloop()


if __name__ == "__main__":
    main()
