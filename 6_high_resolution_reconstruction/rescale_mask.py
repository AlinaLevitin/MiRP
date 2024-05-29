#!/usr/bin/env python3
"""
Author: Alina Levitin
Date: 22/05/24
Updated: 22/05/24

Command to bring up Rescale References GUI - input pixel size and box size can be found in the particles.star file after
subset selection
The method of rescaling references is located in LG_MiRP/methods/reference_scaler
The GUI is located in LG_MiRP/gui/rescale_references_gui
"""

from LG_MiRP import RescaleMaskGui

# Generating the gui
RescaleMaskGui()