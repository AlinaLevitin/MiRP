#!/usr/bin/env python3
"""
Author: Alina Levitin
Date: 03/06/24
Updated: 09/06/24

Command to bring up Utils GUI
The GUI is located in LG_MiRP/gui/utils_gui

The Frame is located in LG_MiRP/gui/segment_average_gui
The method of segment averaging is located in LG_MiRP/methods/segment_average_generator

"""

from LG_MiRP import UtilsGui, SegmentAverageFrame, MaskGeneratorFrame


def main():
    # Generating the gui
    gui = UtilsGui('Utils')
    gui.add_frame(SegmentAverageFrame, 'Segment average generator')
    gui.add_frame(MaskGeneratorFrame, 'Mask generator')
    gui.mainloop()


if __name__ == "__main__":
    main()
