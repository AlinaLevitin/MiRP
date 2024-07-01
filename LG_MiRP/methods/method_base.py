"""
Author: Alina Levitin
Date: 02/04/24
Updated: 27/05/24

This contains the base class for all the methods and wrappers for the methods

"""
import os
import shutil
import subprocess
import functools
import numpy as np
import matplotlib.pyplot as plt


# ======================================================================================================================
# Wrappers
def print_done_decorator(func):
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        print('Done!')
        return result

    return wrapper


def print_command_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract command from function's docstring or create it from arguments
        command = func.__doc__ or "Executing command"
        print(f"Command: {command}")

        # Perform the necessary checks
        instance = args[0]  # Assuming the first argument is the class instance
        if 'input_background_wedge_map' in kwargs:
            input_background_wedge_map = kwargs['input_background_wedge_map']
        elif len(args) > 1:
            input_background_wedge_map = args[1]
        else:
            print("Error: No `input_background_wedge_map` argument provided for checks.")
            return

        try:
            instance.perform_checks(input_background_wedge_map)
        except ValueError as e:
            print(f"Error: {e}")
            return

        result = func(*args, **kwargs)
        print("Command executed successfully.")
        return result

    return wrapper


# ======================================================================================================================
# Base class for all the method classes

class MethodBase:

    # Mathematical functions:

    @staticmethod
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

    def fit_clusters(self, values, top_cluster):

        slope, intercept = self.linear_fit(np.arange(1, len(top_cluster) + 1), [values[i] for i in top_cluster])

        # Fit linear model to the low weight cluster
        x = np.array([i for i in range(0, len(values))])
        linear_fit_values = intercept + slope * x

        return linear_fit_values

    @staticmethod
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

    def flatten_and_cluster_shifts(self, shifts):
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
        clusters = self.cluster_numpy_bins(flattened_shifts[min_flatness_idx], bins)

        # Find the cluster with the maximum length
        sorted_clusters = sorted(clusters.items(), key=lambda item: len(item[1]), reverse=True)
        top_cluster_key, top_cluster = sorted_clusters.pop(0)

        # Find the outliers
        low_weight_cluster = [value for sublist in sorted_clusters for value in sublist[1]]

        return top_cluster, low_weight_cluster

    @staticmethod
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

    def plot_confidence_distribution(self, data, cutoff=None):

        if cutoff:
            data = self.filter_microtubules_by_length(data, cutoff)

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
    # structural functions:

    @staticmethod
    def spherical_cosmask(n, mask_radius, edge_width, origin=None):
        """mask = spherical_cosmask(n, mask_radius, edge_width, origin)
        """

        if type(n) is int:
            n = np.array([n])

        sz = np.array([1, 1, 1])
        sz[0:np.size(n)] = n[:]

        szl = -np.floor(sz / 2)
        szh = szl + sz

        x, y, z = np.meshgrid(np.arange(szl[0], szh[0]),
                              np.arange(szl[1], szh[1]),
                              np.arange(szl[2], szh[2]), indexing='ij', sparse=True)

        r = np.sqrt(x * x + y * y + z * z)

        m = np.zeros(sz.tolist())

        #    edgezone = np.where( (x*x + y*y + z*z >= mask_radius) & (x*x + y*y + z*z <= np.square(mask_radius + edge_width)))

        edgezone = np.all(
            [(x * x + y * y + z * z >= mask_radius), (x * x + y * y + z * z <= np.square(mask_radius + edge_width))],
            axis=0)
        m[edgezone] = 0.5 + 0.5 * np.cos(2 * np.pi * (r[edgezone] - mask_radius) / (2 * edge_width))
        m[np.all([(x * x + y * y + z * z <= mask_radius * mask_radius)], axis=0)] = 1

        #    m[ np.where(x*x + y*y + z*z <= mask_radius*mask_radius)] = 1

        return m

    @staticmethod
    def calc_center_of_gravity(structure):
        x_sum, y_sum, z_sum = 0, 0, 0
        total_weight = 0

        for model in structure:
            for chain in model:
                for residue in chain:
                    for atom in residue:
                        # Get the atom coordinates
                        atom_coord = atom.get_coord()
                        # Get the atom weight (assuming it's stored in B-factor)
                        atom_weight = atom.get_bfactor()
                        # Accumulate the weighted sum of coordinates
                        x_sum += atom_coord[0] * atom_weight
                        y_sum += atom_coord[1] * atom_weight
                        z_sum += atom_coord[2] * atom_weight
                        # Accumulate the total weight
                        total_weight += atom_weight

        # Calculate the center of gravity
        center_of_gravity = np.array([x_sum / total_weight, y_sum / total_weight, z_sum / total_weight])

        return center_of_gravity

    # ======================================================================================================================
    # Lazy functions:
    @staticmethod
    def filter_microtubules_by_length(data, cutoff):
        # Group the DataFrame by micrograph name and helical tube ID
        grouped = data.groupby(['rlnMicrographName', 'rlnHelicalTubeID'])

        # Filter out microtubules with lengths below the cutoff
        filtered_data = data[grouped.size() >= cutoff]

        # Write the updated DataFrame to a new STAR file
        return filtered_data

    @staticmethod
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

    # ==================================================================================================================
    # Relion checks commands

    @staticmethod
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



