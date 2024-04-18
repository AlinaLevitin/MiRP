"""
Author: Alina Levitin
Date: 18/04/24
Updated: 18/04/24

Command to bring up unifi PHI/Rot (XY shifts smoothing) GUI
The method of angle smoothing is located in LG_MiRP/methods/XY_smoothing

shifts: _rlnOriginX, _rlnOriginY, _rlnOriginZ are set to 0
(_rlnAngleRot is kept same)
angles: _rlnAnglePsi, _rlnAngleTilt are set to priors: _rlnAnglePsiPrior, _rlnAngleTiltPrior


The GUI is located in LG_MiRP/gui/angles_smoothing_gui
"""

import LG_MiRP

# Generating the gui
LG_MiRP.SmoothingGui(label='shifts')
