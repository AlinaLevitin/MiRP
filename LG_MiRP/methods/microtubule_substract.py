import os
import subprocess
from mpi4py import MPI
import numpy as np
import mrcfile
import starfile
from Bio.PDB import PDBParser
from Bio.PDB.Structure import Structure

from .method_base import MethodBase, print_done_decorator


class MicrotubuleSubtract(MethodBase):

    def __init__(self, input_star_file, pf_number):
        self.input_star_file = input_star_file.get()
        particles_star_file_data = starfile.read(self.input_star_file)
        self.particles_dataframe = particles_star_file_data['particles']
        self.data_optics_dataframe = particles_star_file_data['optics']
        self.pixel_size = self.data_optics_dataframe['rlnImagePixelSize'].iloc[0]
        self.pf_number = int(pf_number.get())

    @print_done_decorator
    def subtract(self, pf):
        command = [
            'relion_project',
            '--i', f'pf{pf}/pf_masked.mrc',
            '--o', f'pf{pf}/proto_particles',
            '--ctf',
            '--angpix', self.pixel_size,
            '--ang', self.input_star_file,
            '--subtract_exp'
        ]
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(
                f'RELION did not run properly. Try running the following command to troubleshoot:\n\n{" ".join(command)}\n\n'
                f'STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}'
            )

    def parallel(self):
        pfs = np.arange(self.pf_number)
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        size = comm.Get_size()
        nums = pfs[pfs % size == rank]

        for i in nums:
            if self.is_relion_installed():
                self.subtract(i)
            else:
                print("Relion is not installed on this computer.")
