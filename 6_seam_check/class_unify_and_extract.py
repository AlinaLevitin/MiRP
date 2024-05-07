"""
Author: Alina Levitin
Date: 31/03/24
Updated: 7/5/24

Method to unify classes  and extract the particles to separate STAR files according to their
class after 3D Classification (assuming 6 classes)
Command to bring up Class Unification and extraction GUI
The method of class unification is located in LG_MiRP/methods/class_unifier
The GUI is located in LG_MiRP/gui/class_uni_ext_gui

"""
import LG_MiRP


LG_MiRP.ClassUnificationExtractionGui(step='seam_check')
