"""
Author: Alina Levitin
Date: 02/07/24
Updated: 10/07/24

BROKEN!! NOT WORKING!!
"""
import os
import subprocess
from mpi4py import MPI
import numpy as np
import starfile
import mrcfile

from .method_base import MethodBase, print_done_decorator, print_command_decorator
from .volume_mrc import VolumeMrc


class MicrotubuleSubtract(MethodBase):

    def __init__(self, input_star_file, input_wedge_directory, pf_number, method):
        self.input_star_file = input_star_file.get()
        particles_star_file_data = starfile.read(self.input_star_file)
        self.particles_dataframe = particles_star_file_data['particles']
        self.data_optics_dataframe = particles_star_file_data['optics']
        self.particles_pixel_size = float(self.data_optics_dataframe['rlnImagePixelSize'].iloc[0])
        self.input_wedge_directory = input_wedge_directory.get()
        self.pf_number = int(pf_number.get())
        self.method = method.get()

    @print_command_decorator
    def relion_microtubule_subtract(self, pf, input_background_wedge_map):

        output_star_file = os.path.join(self.input_wedge_directory, f'{pf}/proto_particles')

        # command = [
        #     'relion_particle_subtract',
        #     '--i', self.input_star_file,
        #     '--o', output_star_file,
        #     '--bck', input_background_wedge_map,
        #     '--angpix', str(self.particles_pixel_size),
        #     '--ctf',
        #     '--skip_local_recenter'
        # ]
        command = [
            'relion_project',
            '--i', input_background_wedge_map,
            '--o', output_star_file,
            '--ctf',
            '--angpix', str(self.particles_pixel_size),
            '--ang', self.input_star_file,
            '--subtract_exp'
        ]
        result = subprocess.run(command, capture_output=True, text=True)

        print(f'Saved particles STAR file at {output_star_file}')

        if result.returncode != 0:
            raise RuntimeError(
                f'RELION did not run properly. Try running the following command to troubleshoot:\n\n{" ".join(command)}\n\n'
                f'STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}'
            )

    @print_command_decorator
    def numpy_microtubule_subtract(self, pf, input_background_wedge_map):
        output_star_file = os.path.join(self.input_wedge_directory, f'{pf}/proto_particles')

        # Load the mask
        with mrcfile.open(input_background_wedge_map) as mrc:
            mask = mrc.data

        # Get the particle image paths for the given PF
        particle_paths = self.particles_dataframe['rlnImageName'].values

        subtracted_images = []

        for particle_path in particle_paths:
            particle_image_path = os.path.join(self.input_wedge_directory, particle_path)

            # Load the particle image
            with mrcfile.open(particle_image_path) as mrc:
                particle_image = mrc.data

            # Subtract particles using the mask
            subtracted_image = particle_image - mask

            # Save the subtracted image
            subtracted_image_path = os.path.join(self.input_wedge_directory, f'{pf}/Particles/subtracted_opticsgroup1.mrcs')
            with mrcfile.new(subtracted_image_path, overwrite=True) as mrc:
                mrc.set_data(subtracted_image)

            subtracted_images.append(subtracted_image_path)

        # Add the subtracted image paths to the STAR file
        self.particles_dataframe['rlnImageName'] = subtracted_images

        # Write the STAR file with updated particle paths
        updated_star_data = {
            'data_optics': self.data_optics_dataframe,
            'data_particles': self.particles_dataframe
        }

        starfile.write(output_star_file, updated_star_data, write_loops=True)

        print(f'Saved subtracted images STAR file at {output_star_file}')

    @print_done_decorator
    def subtract_microtubule(self, method='relion'):

        if method == 'relion':
            extract_directory = self.find_extract_directory()
            os.chdir(extract_directory)

        for i in range(1, self.pf_number + 1):

            input_background_wedge_map = os.path.join(self.input_wedge_directory, f'{i}/pf{i}_wedge.mrc')
            if method == 'relion':
                self.relion_microtubule_subtract(i, input_background_wedge_map=input_background_wedge_map)
            if method == 'numpy':
                self.numpy_microtubule_subtract(i, input_background_wedge_map=input_background_wedge_map)

    # @print_done_decorator
    # def subtract_microtubule(self):
    #     pfs = np.arange(self.pf_number)
    #     comm = MPI.COMM_WORLD
    #     rank = comm.Get_rank()
    #     size = comm.Get_size()
    #     nums = pfs[pfs % size == rank]
    #
    #     extract_directory = self.find_extract_directory()
    #     os.chdir(extract_directory)
    #
    #     for i in range(1, self.pf_number + 1):
    #         input_background_wedge_map = os.path.join(self.input_wedge_directory, f'{i}/pf{i}_wedge.mrc')
    #         self.relion_microtubule_subtract(i, input_background_wedge_map=input_background_wedge_map)

    def find_extract_directory(self):
        current_dir = self.input_wedge_directory
        while True:
            if 'Extract' in os.listdir(current_dir):
                return current_dir
            parent_dir = os.path.dirname(current_dir)
            if parent_dir == current_dir:  # Root directory reached
                raise FileNotFoundError("No 'Extract' directory found in the path hierarchy.")
            current_dir = parent_dir

    def perform_checks(self, input_background_wedge_map):
        # Check if Relion is installed
        if self.method == 'relion':
            if not self.is_relion_installed():
                raise ValueError("Relion is not installed on this computer.")

        # Check if pixel size and shape are compatible
        particles_size = int(self.data_optics_dataframe['rlnImageSize'].iloc[0])
        volume = VolumeMrc(input_background_wedge_map)
        wedge_size = volume.shape[0]
        wedge_pixel_size = round(float(volume.pixel), 2)

        # Checks if the box sized matches
        if particles_size != wedge_size:
            raise ValueError(
                f"\nParticles box size {particles_size} is not compatible with wedge box size {wedge_size} "
            )

        # Checks if the pixel sized matches
        if self.particles_pixel_size != wedge_pixel_size:
            raise ValueError(
                f"\nParticles pixel size {self.particles_pixel_size} is not compatible with wedge pixel size {wedge_pixel_size} "
            )
