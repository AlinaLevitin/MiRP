"""
Author: Alina Levitin
Date: 02/04/24
Updated: 02/04/24

Random utils and methods

"""

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
    X = np.column_stack([np.ones_like(x), x])

    # Calculate the least squares solution
    beta = np.linalg.lstsq(X, y, rcond=None)[0]

    # Calculate the fitted values
    fitted = beta[0] + beta[1] * x

    return fitted.tolist()

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


def plot_angles_and_shifts(star_file_input):

    star_data = starfile.read(star_file_input.get())
    data = star_data['particles']

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

    axes[3].plot(data['rlnOriginX'], 'o', label='Xshift')
    axes[3].plot(data['rlnOriginY'], 'o', label='Yshift')
    axes[3].set_title('X/Y Shifts')
    axes[3].set_ylabel('Shift (pixels)')
    axes[3].legend(loc='upper right')

    plt.setp(axes, xticks=[i for i in range(1, len(data) + 1, 2)], xlabel='Particle Number')

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

