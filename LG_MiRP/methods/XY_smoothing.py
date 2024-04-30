"""
Author: Alina Levitin
Date: 02/04/24
Updated: 02/04/24

Methods for smoothing X/Y Shifts

"""
import os

import numpy as np
import starfile

from .methods_utils import linear_fit, filter_microtubules_by_length


def smooth_xy_shifts(star_file_input, output_path, cutoff=None):

    data = starfile.read(star_file_input.get())

    particles_dataframe = data['particles']
    data_optics_dataframe = data['optics']

    if cutoff:
        particles_dataframe = filter_microtubules_by_length(particles_dataframe, cutoff)

    # Group data by micrograph and tube ID
    grouped_data = particles_dataframe.groupby(['rlnMicrographName', 'rlnHelicalTubeID'])

    # Initialize lists to store smoothed X and Y shifts
    smoothed_x_shifts = []
    smoothed_y_shifts = []

    for (micrograph, MT), MT_dataframe in grouped_data:
        print(f'Now fitting MT {MT} in micrograph {micrograph}')
        # Extract X and Y shifts for the current microtubule
        x_shifts = MT_dataframe['rlnOriginXAngst'].tolist()
        y_shifts = MT_dataframe['rlnOriginYAngst'].tolist()

        # Smooth X and Y shifts
        smoothed_x = flatten_and_cluster_shifts(x_shifts)
        smoothed_y = flatten_and_cluster_shifts(y_shifts)

        # # Append smoothed shifts to the lists
        # smoothed_x_shifts.extend(smoothed_x)
        # smoothed_y_shifts.extend(smoothed_y)

    # Assign smoothed shifts to the DataFrame
    particles_dataframe['rlnOriginXAngst'] = smoothed_x
    particles_dataframe['rlnOriginYAngst'] = smoothed_y

    new_particles_star_file_data = {'optics': data_optics_dataframe, 'particles': particles_dataframe}

    os.chdir(output_path.get())
    original_name = star_file_input.get().replace('.star', '')
    output_file = f'{original_name}_smoothened_XY.star'

    starfile.write(new_particles_star_file_data, output_file)

    print("=" * 50)
    print(f"Updated STAR file saved as: {output_file} at {output_path.get()}")

    return particles_dataframe


def flatten_and_cluster_shifts(shifts):
    # Generate flattening factors
    flattening_factors = np.arange(-8, 8, 0.25)
    flatness_score = []
    b = []

    # Initialize arrays to store flattened shifts and flatness scores
    flattened_shifts = np.zeros((len(flattening_factors), len(shifts)))
    flatness_scores = np.zeros(len(flattening_factors))

    for i, factor in enumerate(flattening_factors):
        # Flatten shifts using broadcasting
        flattened_shifts[i] = shifts - np.arange(1, len(shifts) + 1) * factor

        # Calculate flatness score
        flatness_scores[i] = np.sum(np.abs(np.diff(flattened_shifts[i])))

    # Find index of minimum flatness score
    min_flatness_idx = np.argmin(flatness_scores)

    # Find histogram bins using numpy
    try:
        hist, bins = np.histogram(flattened_shifts[min_flatness_idx], bins='auto')
    except MemoryError:
        hist, bins = np.histogram(flattened_shifts[min_flatness_idx], bins=5)

    # Cluster shift values
    clusters = cluster_numpy_bins(flattened_shifts[min_flatness_idx], bins)

    # Find the cluster with the maximum length
    top_cluster = max(clusters.values(), key=len)

    # Fit linear model to the top cluster
    fit = linear_fit(top_cluster, [shifts[i] for i in top_cluster])

    return fit


def cluster_numpy_bins(data, bins):
    bin_ids = np.digitize(data, bins)

    cluster = {}

    for idx, a in enumerate(bin_ids):
        if a in cluster.keys():
            for b in cluster.keys():
                if a == b:
                    cluster[b].append(idx)
                else:
                    pass
        else:
            cluster[a] = [idx]

    return cluster
