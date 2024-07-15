"""
Author: Alina Levitin
Date: 27/05/24
Updated: 27/05/24

This contains a class for handling mrc volume files using mcrfile library

"""
import mrcfile


class VolumeMrc:

    def __init__(self, mrc_file_path):
        self.mrc_file_path = mrc_file_path
        self.data = None
        self.shape = None
        self.voxel_size = None
        self.pixel = None
        # Getting all the parameters from the mrc file
        self.mrc_attributes()

    def mrc_attributes(self):
        """
        Gets the parameters of the mrc files, used when called
        """
        with mrcfile.open(self.mrc_file_path) as mrc:
            self.data = mrc.data
            self.shape = self.data.shape
            self.voxel_size = mrc.voxel_size
            self.pixel = self.voxel_size['x']

