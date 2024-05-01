"""
Author: Alina Levitin
Date: 01/05/24
Updated: 01/05/24

Methods for smoothing X/Y Shifts and angles

"""
import os

import numpy as np
import starfile

from .methods_utils import fit_clusters, filter_microtubules_by_length, cluster_shallow_slopes, flatten_and_cluster_shifts


def smooth_angles_or_shifts(star_file_input, output_path, function, cutoff=None):

    data = starfile.read(star_file_input.get())

    particles_dataframe = data['particles']
    data_optics_dataframe = data['optics']

    if cutoff:
        particles_dataframe = filter_microtubules_by_length(particles_dataframe, cutoff)

    if function == 'angles':
        particles_dataframe = process_data(particles_dataframe, id_label='rlnAngleRot')
    elif function == 'shifts':
        particles_dataframe = process_data(particles_dataframe, id_label='rlnOriginXAngst')
        particles_dataframe = process_data(particles_dataframe, id_label='rlnOriginYAngst')

    new_particles_star_file_data = {'optics': data_optics_dataframe, 'particles': particles_dataframe}

    os.chdir(output_path.get())
    original_name = star_file_input.get().replace('.star', '')
    output_file = f'{original_name}_smoothened_{function}.star'

    starfile.write(new_particles_star_file_data, output_file)

    print("=" * 50)
    print(f"Updated STAR file saved as: {output_file} at {output_path.get()}")

    return particles_dataframe


def process_data(particles_dataframe, id_label):
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
            top_clstr, outliers = cluster_shallow_slopes(values, angle_cutoff)
        elif id_label in ['rlnOriginXAngst', 'rlnOriginYAngst']:
            top_clstr, outliers = flatten_and_cluster_shifts(values)
        else:
            raise ValueError("Unsupported id_label")
        if top_clstr:
            print(f'Now fitting MT {MT} in micrograph {micrograph}')
            MT_dataframe.reset_index(inplace=True)

            values = MT_dataframe.loc[:, id_label].to_numpy()
            fitted_values = fit_clusters(values, top_clstr)

            particles_dataframe.loc[mask1 & mask2, id_label] = fitted_values
        else:
            print(f'MT {MT} in micrograph {micrograph}, {id_label} cannot be fit, and is discarded')
            matching_rows = particles_dataframe[mask1 & mask2]
            index_numbers = matching_rows.index
            bad_mts.append(index_numbers[0])

    if bad_mts:
        particles_dataframe.drop(bad_mts, inplace=True)

    return particles_dataframe


