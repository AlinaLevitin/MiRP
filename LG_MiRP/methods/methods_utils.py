"""
Author: Alina Levitin
Date: 02/04/24
Updated: 02/04/24

Random utils and methods

"""
import os
import shutil
import subprocess

import numpy as np
import matplotlib.pyplot as plt
import starfile

# ======================================================================================================================
# Mathematical functions:


def linear_fit(xax, vals):
    x = np.array(xax)
    y = np.array(vals)

    # Create the design matrix
    matrix = np.column_stack([np.ones_like(x), x])

    # Calculate the least squares solution
    beta = np.linalg.lstsq(matrix, y, rcond=None)[0]

    slope = beta[1]
    intercept = beta[0]

    return slope, intercept


def fit_clusters(values, top_cluster):

    slope, intercept = linear_fit(np.arange(1, len(top_cluster) + 1), [values[i] for i in top_cluster])

    # Fit linear model to the low weight cluster
    x = np.array([i for i in range(0, len(values))])
    linear_fit_values = intercept + slope * x

    return linear_fit_values


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
    sorted_clusters = sorted(clusters.items(), key=lambda item: len(item[1]), reverse=True)
    top_cluster_key, top_cluster = sorted_clusters.pop(0)

    # Find the outliers
    low_weight_cluster = [value for sublist in sorted_clusters for value in sublist[1]]

    return top_cluster, low_weight_cluster


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

# ======================================================================================================================
# Plotting functions:


def mt_segment_histogram(particles_star_file):
    """
    A method to generate a histogram from number of segments per MT

    :param particles_star_file: particles star file from entry
    :return: matplotlib histogram fig
    """

    try:
        # Try to read the STAR file
        particles_star_file_data = starfile.read(particles_star_file.get())
        particles_dataframe = particles_star_file_data['particles']

        # Access the 'rlnMicrographName' column and get unique values
        micrographs = particles_dataframe['rlnMicrographName'].unique()

        # Continue with further processing
        # ...

    except FileNotFoundError:
        # Handle the case where the specified STAR file does not exist
        print("Error: The specified STAR file does not exist.")
        # Optionally, you can raise the error again if needed
        raise

    mt_segments = []
    for micrograph in micrographs:
        mask = particles_dataframe['rlnMicrographName'] == micrograph
        micrograph_star = particles_dataframe.loc[mask]
        number_of_MTs = micrograph_star['rlnHelicalTubeID'].max()
        for mt in range(1, number_of_MTs + 1):
            mask_mt_number = micrograph_star['rlnHelicalTubeID'] == mt
            mt_star = micrograph_star.loc[mask_mt_number]
            number_of_segments_per_mt = mt_star.shape[0]
            mt_segments.append(number_of_segments_per_mt)

    # Create a Matplotlib figure and axes
    fig, ax = plt.subplots()

    # Plot histogram
    ax.hist(mt_segments, color='skyblue', edgecolor='black', bins=5)

    # Add labels and title
    ax.set_xlabel('Number of segments')
    ax.set_ylabel('Frequency')
    ax.set_title('Histogram of Segments of Microtubules')

    return fig


def plot_angles_and_shifts(data):

    data.reset_index(inplace=True)

    fig, axes = plt.subplots(1, 4, figsize=(12, 6))

    axes[0].plot(data['rlnAngleRot'], 'o')
    axes[0].set_ylim([-181, 181])
    axes[0].set_yticks([i for i in range(-180, 180 + 1, 40)])
    axes[0].set_ylabel('Phi Angle')
    axes[0].set_title('Phi')

    axes[1].plot(data['rlnAngleTilt'], 'o')
    axes[1].set_yticks([i for i in range(-180, 180 + 1, 40)])
    axes[1].set_ylim([-181, 181])
    axes[1].set_ylabel('Theta Angle')
    axes[1].set_title('Theta')

    axes[2].plot(data['rlnAnglePsi'], 'o')
    axes[2].set_yticks([i for i in range(-180, 180 + 1, 40)])
    axes[2].set_ylim([-181, 181])
    axes[2].set_ylabel('Psi Angle')
    axes[2].set_title('Psi')

    axes[3].plot(data['rlnOriginXAngst'], 'o', label='Xshift')
    axes[3].plot(data['rlnOriginYAngst'], 'o', label='Yshift')
    axes[3].set_title('X/Y Shifts')
    axes[3].set_ylabel('Shift (pixels)')
    axes[3].legend(loc='upper right')

    plt.setp(axes, xticks=[i for i in range(1, len(data) + 1, 2)], xlabel='Segment')

    plt.tight_layout()  # Add padding between subplots

    return fig


def plot_confidence_distribution(data, cutoff=None):

    if cutoff:
        data = filter_microtubules_by_length(data, cutoff)

    # Group particle data by micrograph name and helical tube ID
    grouped_data = data.groupby(['rlnMicrographName', 'rlnHelicalTubeID'])

    # Calculate confidence distribution for each microtubule
    cer = []
    for _, group in grouped_data:
        cls_distribution = group['rlnClassNumber'].value_counts()
        max_count = cls_distribution.max()
        total_particles = len(group)
        confidence = (max_count / total_particles) * 100
        cer.append(confidence)

    # Create a histogram of the confidence distribution
    fig, ax = plt.subplots()
    ax.hist(cer, bins=10)
    ax.set_xlabel('Percent Confidence')
    ax.set_ylabel('Frequency')
    ax.set_title('Confidence Distribution')
    return fig

# ======================================================================================================================
# Lazy functions:


def filter_microtubules_by_length(data, cutoff):
    # Group the DataFrame by micrograph name and helical tube ID
    grouped = data.groupby(['rlnMicrographName', 'rlnHelicalTubeID'])

    # Filter out microtubules with lengths below the cutoff
    filtered_data = data[grouped.size() >= cutoff]

    # Write the updated DataFrame to a new STAR file
    return filtered_data


def is_relion_installed():
    """
    A lazy method to check if relion is installed on the computer
    :return: True or False if relion is installed or not
    """
    try:
        # Run a command to check if relion is installed
        result = subprocess.run(['relion_refine', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            # If the return code is 0, it means the command executed successfully, hence Relion is installed
            return True
        else:
            # If the return code is not 0, Relion is likely not installed or the command failed
            return False
    except FileNotFoundError:
        # If FileNotFoundError is raised, it means the command (relion_refine) wasn't found,
        # hence Relion is not installed
        return False


def delete_folder_contents(folder_path):
    # List all contents in the folder
    contents = os.listdir(folder_path)

    # Iterate through each item in the folder
    for item in contents:
        # Create the full path to the item
        item_path = os.path.join(folder_path, item)

        # Check if the item is a file
        if os.path.isfile(item_path) or os.path.islink(item_path):
            # Delete the file or symbolic link
            os.remove(item_path)

        # Check if the item is a directory
        elif os.path.isdir(item_path):
            # Recursively delete the directory and its contents using shutil.rmtree
            shutil.rmtree(item_path)

    print(f"All contents in {folder_path} have been deleted.")