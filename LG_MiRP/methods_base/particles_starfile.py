"""
Author: Alina Levitin
Date: 27/05/24
Updated: 28/07/24

This contains a collection of plotting functions

"""
import random

import matplotlib.pyplot as plt
import starfile


class ParticlesStarfile:

    def __init__(self, particles_starfile_path):
        self.particles_dataframe = None
        self.optics_dataframe = None
        try:
            self.read_particles_starfile(particles_starfile_path)
        except FileNotFoundError:
            # Handle the case where the specified STAR file does not exist
            print("Error: The specified STAR file does not exist.")
            # Optionally, you can raise the error again if needed
            raise

    def read_particles_starfile(self, path):
        particles_star_file_data = starfile.read(path)
        self.particles_dataframe = particles_star_file_data['particles']
        self.optics_dataframe = particles_star_file_data['optics']


def groupby_micrograph_and_helical_id(particles_dataframe):
    return particles_dataframe.groupby(['rlnMicrographName', 'rlnHelicalTubeID'])


def filter_microtubules_by_length(particles_dataframe, cutoff):
    """
    Removes MTs in which the number of segments is lower than the cutoff

    :param particles_dataframe: data block from data star file
    :param cutoff: minimal number of segments to include
    :return: data where MTs with number of segments lower than in the cutoff are excluded
    """
    # Group the DataFrame by micrograph name and helical tube ID
    grouped = particles_dataframe.groupby_micrograph_and_helical_id()

    # Filter out microtubules with lengths below the cutoff
    filtered_data = particles_dataframe.particles_dataframe[grouped.size() >= cutoff]

    # Write the updated DataFrame to a new STAR file
    return filtered_data


# ======================================================================================================================
# Plotting functions:
def mt_segment_histogram(particles_dataframe):
    """
    A method to generate a histogram from number of segment
    s per MT

    :return: matplotlib histogram fig
    """
    micrographs = particles_dataframe.particles_dataframe['rlnMicrographName'].unique()

    mt_segments = []
    for micrograph in micrographs:
        mask = particles_dataframe.particles_dataframe['rlnMicrographName'] == micrograph
        micrograph_star = particles_dataframe.particles_dataframe.loc[mask]
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


def plot_angles_and_shifts(particles_dataframe):
    """
    Plots angles and shifts as a function of segments along a MT

    :param particles_dataframe: pandas.Dataframe containing the particles data block from a star file

    :return: The matplotlib figure object containing the subplots
    """
    # Reset the index of the DataFrame to ensure it's sequential and starts from 0
    particles_dataframe.reset_index(inplace=True)

    # Create a figure with 4 subplots arranged in 1 row and 4 columns
    fig, axes = plt.subplots(1, 4, figsize=(10, 3))

    # Plot rlnAngleRot (Phi Angle) in the first subplot
    axes[0].plot(particles_dataframe['rlnAngleRot'], 'o')
    axes[0].set_ylim([-181, 181])  # Set the y-axis limits
    axes[0].set_yticks([i for i in range(-180, 180 + 1, 40)])  # Set y-axis ticks
    axes[0].set_ylabel('Phi Angle')  # Label the y-axis
    axes[0].set_title('Phi')  # Set the title of the subplot

    # Plot rlnAngleTilt (Theta Angle) in the second subplot
    axes[1].plot(particles_dataframe['rlnAngleTilt'], 'o')
    axes[1].set_ylim([-181, 181])  # Set the y-axis limits
    axes[1].set_yticks([i for i in range(-180, 180 + 1, 40)])  # Set y-axis ticks
    axes[1].set_ylabel('Theta Angle')  # Label the y-axis
    axes[1].set_title('Theta')  # Set the title of the subplot

    # Plot rlnAnglePsi (Psi Angle) in the third subplot
    axes[2].plot(particles_dataframe['rlnAnglePsi'], 'o')
    axes[2].set_ylim([-181, 181])  # Set the y-axis limits
    axes[2].set_yticks([i for i in range(-180, 180 + 1, 40)])  # Set y-axis ticks
    axes[2].set_ylabel('Psi Angle')  # Label the y-axis
    axes[2].set_title('Psi')  # Set the title of the subplot

    # Plot rlnOriginXAngst and rlnOriginYAngst (X and Y Shifts) in the fourth subplot
    axes[3].plot(particles_dataframe['rlnOriginXAngst'], 'o', label='Xshift')
    axes[3].plot(particles_dataframe['rlnOriginYAngst'], 'o', label='Yshift')
    axes[3].set_title('X/Y Shifts')  # Set the title of the subplot
    axes[3].set_ylabel('Shift (pixels)')  # Label the y-axis
    axes[3].legend(loc='upper right')  # Add a legend in the upper right corner

    # Set the x-ticks for all subplots to be the segment numbers, spaced by 2
    plt.setp(axes, xticks=[i for i in range(1, len(particles_dataframe) + 1, 2)], xlabel='Segment')

    # Adjust the layout to add padding between subplots
    plt.tight_layout()

    # Return the figure object containing the plots
    return fig
