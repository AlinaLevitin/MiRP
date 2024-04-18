"""
Author: Alina Levitin
Date: 16/04/24
Updated: 18/04/24

Methods for smoothing ROT and PSI

"""
import os

import numpy as np
import starfile

from .methods_utils import linear_fit, filter_microtubules_by_length


def smooth_angles(star_file_input, id_label, output_path, cutoff=None):
    """

    :param star_file_input: input star file after 2nd 3D refinement
    :param id_label: rlnAngleRot or rlnAnglePsi
    :param output_path: path to write the output star file
    :param cutoff: microtubule length cutoff
    :return: Writes a new star file with corrected angles
    """

    data = starfile.read(star_file_input.get())

    particles_dataframe = data['particles']
    data_optics_dataframe = data['optics']

    if cutoff:
        particles_dataframe = filter_microtubules_by_length(particles_dataframe, cutoff)

    angle_cutoff = 8
    bad_mts = []

    for mtIDX, MT_dataframe in particles_dataframe.groupby(['rlnMicrographName', 'rlnHelicalTubeID']):
        angles = MT_dataframe[id_label].to_numpy()

        top_clstr, outliers = cluster_shallow_slopes(angles, angle_cutoff)

        if not top_clstr:
            print(f'MT {mtIDX[1]} in micrograph {mtIDX[0]}, {id_label} cannot be fit, and is discarded')
            # Find the rows in `particles_dataframe` where the values of 'rlnMicrographName' and 'rlnHelicalTubeID' match `mtIDX`
            matching_rows = particles_dataframe[
                (particles_dataframe['rlnMicrographName'] == mtIDX[0]) &
                (particles_dataframe['rlnHelicalTubeID'] == mtIDX[1])
                ]

            # Get the index numbers of the matching rows
            index_numbers = matching_rows.index
            bad_mts.append(index_numbers[0])
        else:
            top_clstr_vals = MT_dataframe.iloc[top_clstr][id_label].to_numpy()
            fitted = linear_fit(np.arange(1, len(top_clstr) + 1), top_clstr_vals)
            particles_dataframe.loc[MT_dataframe.index, id_label] = fitted

    particles_dataframe.drop(bad_mts, inplace=True)

    new_particles_star_file_data = {'optics': data_optics_dataframe, 'particles': particles_dataframe}

    os.chdir(output_path.get())
    output_file = f'smoothened_{id_label}_data.star'

    starfile.write(new_particles_star_file_data, output_file)

    print(f"Updated STAR file saved as: {output_file} at {output_path.get()}")

    return particles_dataframe


def cluster_shallow_slopes(angles, cutoff):
    # Create an array of all pairwise differences
    diff_matrix = angles[:, None] - angles[None, :]

    # Find the absolute differences within the cutoff range
    within_cutoff = np.abs(diff_matrix) <= cutoff

    # Create an upper triangular mask to exclude self-comparisons and symmetric pairs
    mask = np.triu(np.ones_like(within_cutoff), k=1)

    # Apply the mask to keep only the upper triangular part within the cutoff range
    within_cutoff = within_cutoff & mask

    # Find the indices of the pairs within the cutoff range
    pairs = np.transpose(np.nonzero(within_cutoff))

    # Initialize a list to store clusters
    clusters = []

    while pairs.size > 0:
        # Get the last pair
        node = pairs[-1]

        # Find all pairs that share a common index with the last pair
        related_pairs = pairs[(pairs[:, 0] == node[0]) | (pairs[:, 1] == node[0]) |
                              (pairs[:, 0] == node[1]) | (pairs[:, 1] == node[1])]

        # Merge the related pairs into a single cluster
        cluster = set(node)
        for pair in related_pairs:
            cluster |= set(pair)

        # Add the cluster to the list of clusters
        clusters.append(sorted(cluster))

        # Remove the pairs belonging to the cluster from the list
        pairs = pairs[~np.isin(pairs, related_pairs).all(axis=1)]

    # Find the cluster with the maximum length
    if clusters:
        top_cluster = max(clusters, key=len)
        low_weight_cluster = [j for i in clusters if i != top_cluster for j in i]
    else:
        top_cluster, low_weight_cluster = None, None

    return top_cluster, low_weight_cluster
