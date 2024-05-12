#!/usr/bin/env python3
"""
TODO: check if the class column is the same for both 3D classification steps
Author: Alina Levitin
Date: 18/04/24
Updated: 18/04/24

Command to bring up Rescale References GUI - input pixel size and box size can be found in the particles.star file after
subset selection
The method of rescaling references is located in LG_MiRP/methods/reference_scaler
The GUI is located in LG_MiRP/gui/rescale_references_gui
"""

import LG_MiRP

# Generating the gui
LG_MiRP.RescaleReferencesGui("References/13pf", method='relion')
