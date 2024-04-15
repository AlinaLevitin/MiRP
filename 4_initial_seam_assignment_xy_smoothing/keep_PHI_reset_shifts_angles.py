"""
Author: Alina Levitin
Date: 15/04/24
Updated: 15/04/24

Command to bring up Reset Shifts and angles GUI
The method of shifts and angles reset is located in LG_MiRP/methods/keep_PHI_reset_angles_shifts

shifts: _rlnOriginX, _rlnOriginY, _rlnOriginZ are set to 0
(_rlnAngleRot is kept same)
angles: _rlnAnglePsi, _rlnAngleTilt are set to priors: _rlnAnglePsiPrior, _rlnAngleTiltPrior


The GUI is located in LG_MiRP/gui/keep_PHI_reset_angles_shifts_gui
"""

import LG_MiRP

# Generating the gui
LG_MiRP.KeepPHIResetShiftsAnglesGui()
