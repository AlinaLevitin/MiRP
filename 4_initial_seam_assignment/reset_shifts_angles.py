"""
Author: Alina Levitin
Date: 11/04/24
Updated: 15/04/24

Command to bring up Reset Shifts and angles GUI
The method of shifts and angles reset is located in LG_MiRP/methods/reset_angles_shifts

shifts: _rlnAngleRot, _rlnOriginX, _rlnOriginY, _rlnOriginZ are set to 0
angles: _rlnAnglePsi, _rlnAngleTilt are set to priors: _rlnAnglePsiPrior, _rlnAngleTiltPrior


The GUI is located in LG_MiRP/gui/reset_angles_shifts_gui
"""

from LG_MiRP import ResetShiftsAnglesGui

# Generating the gui
ResetShiftsAnglesGui("Reset shifts and angles to 0/prior")
