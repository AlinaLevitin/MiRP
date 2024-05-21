"""
Author: Alina Levitin
Date: 17/04/24
Updated: 17/04/24

Command to bring up unifi PHI/Rot (angle smoothing) GUI
The method of angle smoothing is located in LG_MiRP/methods/angle_smoothing

shifts: _rlnOriginX, _rlnOriginY, _rlnOriginZ are set to 0
(_rlnAngleRot is kept same)
angles: _rlnAnglePsi, _rlnAngleTilt are set to priors: _rlnAnglePsiPrior, _rlnAngleTiltPrior


The GUI is located in LG_MiRP/gui/angles_smoothing_gui
"""

from LG_MiRP import SmoothingGui

# Generating the gui
SmoothingGui(method="angles")
