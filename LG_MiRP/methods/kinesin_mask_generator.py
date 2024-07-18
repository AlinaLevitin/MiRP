"""
Author: Alina Levitin
Date: 18/07/24
Updated: 18/07/24

Method to generate masks volume .mrc file from a pdb
"""
import os
from pymol import cmd
import MDAnalysis as mda
# from MDAnalysis.analysis.density import density_from_universe
import numpy as np
import mrcfile
import starfile
from Bio.PDB import PDBParser
from Bio.PDB.Structure import Structure

from .method_base import MethodBase, print_done_decorator


class KinesinMaskGenerator(MethodBase):
    """
    Inherits from MethodBase class located in method_base.py
    """

    class KinesinMaskGenerator:
        """
        Class to generate masks volume .mrc file from a PDB using PyMOL.
        """

        def __init__(self, input_pdb, output_directory, input_pixel_size, input_box_size):
            self.input_pdb = input_pdb
            self.output_mrc = os.path.join(output_directory, 'test.mrc')
            self.grid_spacing = float(input_pixel_size)
            self.box_size = int(input_box_size)

        def pdb_to_mrc(self):
            # Initialize PyMOL and load the PDB file
            cmd.reinitialize()
            cmd.load(self.input_pdb, 'my_structure')

            # Set up the grid size
            center = cmd.centerofmass('my_structure')
            grid_min = [center[0] - self.box_size / 2, center[1] - self.box_size / 2, center[2] - self.box_size / 2]
            grid_max = [center[0] + self.box_size / 2, center[1] + self.box_size / 2, center[2] + self.box_size / 2]
            cmd.set('grid_max', grid_max)
            cmd.set('grid_min', grid_min)

            # Generate the density map using PyMOL's map calculation
            cmd.map_new('density_map', 'gaussian', self.grid_spacing, 'my_structure', 0.8)

            # Save the density map as an MRC file
            cmd.save(self.output_mrc, 'density_map')

            print(f"Density map saved as {self.output_mrc}")
