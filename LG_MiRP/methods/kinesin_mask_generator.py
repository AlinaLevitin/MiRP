"""
Author: Alina Levitin
Date: 18/07/24
Updated: 18/07/24

Method to generate masks volume .mrc file from a pdb
"""
import os
# from pymol import cmd
# import MDAnalysis as mda
# from MDAnalysis.analysis.density import density_from_universe
import numpy as np
from Bio.PDB import PDBParser
import mrcfile
import starfile
from Bio.PDB import PDBParser
from scipy.ndimage import gaussian_filter
from Bio.PDB.Structure import Structure

from .method_base import MethodBase, print_done_decorator


class KinesinMaskGenerator(MethodBase):
    """
    Inherits from MethodBase class located in method_base.py
    """

    def __init__(self, input_pdb, output_directory, input_pixel_size, input_box_size):
        self.input_pdb = input_pdb.get()
        self.output_directory = output_directory.get()
        self.pixel_size = float(input_pixel_size.get())
        self.box_size = int(input_box_size.get())

    def generate_spherical_volume(self):
        # Parse PDB file and calculate the center of mass (COM)
        structure = self.parse_pdb()
        com = self.calc_center_of_gravity(structure)

        # Create spherical mask centered at COM
        spherical_mask = self.spherical_cosmask(self.box_size, self.mask_radius, self.edge_width, com)

        # Save the spherical mask as an MRC file
        self.save_spherical_mask(spherical_mask)

    def parse_pdb(self):
        parser = PDBParser(QUIET=True)
        structure = parser.get_structure('protein', self.input_pdb)
        return structure

    def save_spherical_mask(self, spherical_mask):
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

        output_mrc = os.path.join(self.output_directory, 'protein_spherical_volume.mrc')
        with mrcfile.new(output_mrc, overwrite=True) as mrc:
            mrc.set_data(spherical_mask.astype(np.float32))
            mrc.voxel_size = (self.pixel_size, self.pixel_size, self.pixel_size)

        print(f'Saved spherical volume at {output_mrc}')