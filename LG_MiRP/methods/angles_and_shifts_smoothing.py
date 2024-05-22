"""
Author: Alina Levitin
Date: 01/05/24
Updated: 01/05/24

Methods for smoothing X/Y Shifts and angles

"""
import os

import starfile

from .method_base import MethodBase, print_done_decorator


class SmoothAnglesOrShifts(MethodBase):

    def __init__(self, star_file_input, output_path, method, cutoff=None):
        self.star_file_input = star_file_input.get()
        self.star_file_name = os.path.basename(self.star_file_input)
        self.output_path = output_path.get()
        self.method = method.get()
        self.cutoff = cutoff

    @print_done_decorator
    def smooth_angles_or_shifts(self):

        data = starfile.read(self.star_file_input)

        particles_dataframe = data['particles']
        data_optics_dataframe = data['optics']

        if self.cutoff:
            particles_dataframe = self.filter_microtubules_by_length(particles_dataframe, self.cutoff)

        if self.method == 'angles':
            particles_dataframe = self.process_data(particles_dataframe, id_label='rlnAngleRot')
        elif self.method == 'shifts':
            particles_dataframe = self.process_data(particles_dataframe, id_label='rlnOriginXAngst')
            particles_dataframe = self.process_data(particles_dataframe, id_label='rlnOriginYAngst')

        new_particles_star_file_data = {'optics': data_optics_dataframe, 'particles': particles_dataframe}

        os.chdir(self.output_path)
        original_name = self.star_file_name.replace('.star', '')
        output_file = f'{original_name}_smoothened_{self.method}.star'

        starfile.write(new_particles_star_file_data, output_file)

        print("=" * 50)
        print(f"Updated STAR file saved as: {output_file} at {self.output_path}")

        return particles_dataframe

    def process_data(self, particles_dataframe, id_label):
        print('=' * 50)
        print(f'Smoothing {id_label}')
        print('=' * 50)

        bad_mts = []
        grouped_data = particles_dataframe.groupby(['rlnMicrographName', 'rlnHelicalTubeID'])

        for (micrograph, MT), MT_dataframe in grouped_data:
            mask1 = particles_dataframe['rlnMicrographName'] == micrograph
            mask2 = particles_dataframe['rlnHelicalTubeID'] == MT

            values = MT_dataframe[id_label].to_numpy()

            if id_label == 'rlnAngleRot':
                angle_cutoff = 8
                top_clstr, outliers = self.cluster_shallow_slopes(values, angle_cutoff)
            elif id_label in ['rlnOriginXAngst', 'rlnOriginYAngst']:
                top_clstr, outliers = self.flatten_and_cluster_shifts(values)
            else:
                raise ValueError("Unsupported id_label")
            if top_clstr:
                print(f'Now fitting MT {MT} in micrograph {micrograph}')
                MT_dataframe.reset_index(inplace=True)

                values = MT_dataframe.loc[:, id_label].to_numpy()
                fitted_values = self.fit_clusters(values, top_clstr)

                particles_dataframe.loc[mask1 & mask2, id_label] = fitted_values
            else:
                print(f'MT {MT} in micrograph {micrograph}, {id_label} cannot be fit, and is discarded')
                matching_rows = particles_dataframe[mask1 & mask2]
                index_numbers = matching_rows.index
                bad_mts.append(index_numbers[0])

        if bad_mts:
            particles_dataframe.drop(bad_mts, inplace=True)

        return particles_dataframe
