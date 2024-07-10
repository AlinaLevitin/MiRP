"""
Author: Alina Levitin
Date: 27/05/24
Updated: 27/05/24

This contains a collection of plotting functions

"""
import matplotlib.pyplot as plt
import starfile


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
    """
    Plots angles and shifts as a function of segments along a MT

    :param data: pandas.Dataframe containing the particles data block from a star file

    :return: The matplotlib figure object containing the subplots
    """
    # Reset the index of the DataFrame to ensure it's sequential and starts from 0
    data.reset_index(inplace=True)

    # Create a figure with 4 subplots arranged in 1 row and 4 columns
    fig, axes = plt.subplots(1, 4, figsize=(12, 6))

    # Plot rlnAngleRot (Phi Angle) in the first subplot
    axes[0].plot(data['rlnAngleRot'], 'o')
    axes[0].set_ylim([-181, 181])  # Set the y-axis limits
    axes[0].set_yticks([i for i in range(-180, 180 + 1, 40)])  # Set y-axis ticks
    axes[0].set_ylabel('Phi Angle')  # Label the y-axis
    axes[0].set_title('Phi')  # Set the title of the subplot

    # Plot rlnAngleTilt (Theta Angle) in the second subplot
    axes[1].plot(data['rlnAngleTilt'], 'o')
    axes[1].set_ylim([-181, 181])  # Set the y-axis limits
    axes[1].set_yticks([i for i in range(-180, 180 + 1, 40)])  # Set y-axis ticks
    axes[1].set_ylabel('Theta Angle')  # Label the y-axis
    axes[1].set_title('Theta')  # Set the title of the subplot

    # Plot rlnAnglePsi (Psi Angle) in the third subplot
    axes[2].plot(data['rlnAnglePsi'], 'o')
    axes[2].set_ylim([-181, 181])  # Set the y-axis limits
    axes[2].set_yticks([i for i in range(-180, 180 + 1, 40)])  # Set y-axis ticks
    axes[2].set_ylabel('Psi Angle')  # Label the y-axis
    axes[2].set_title('Psi')  # Set the title of the subplot

    # Plot rlnOriginXAngst and rlnOriginYAngst (X and Y Shifts) in the fourth subplot
    axes[3].plot(data['rlnOriginXAngst'], 'o', label='Xshift')
    axes[3].plot(data['rlnOriginYAngst'], 'o', label='Yshift')
    axes[3].set_title('X/Y Shifts')  # Set the title of the subplot
    axes[3].set_ylabel('Shift (pixels)')  # Label the y-axis
    axes[3].legend(loc='upper right')  # Add a legend in the upper right corner

    # Set the x-ticks for all subplots to be the segment numbers, spaced by 2
    plt.setp(axes, xticks=[i for i in range(1, len(data) + 1, 2)], xlabel='Segment')

    # Adjust the layout to add padding between subplots
    plt.tight_layout()

    # Return the figure object containing the plots
    return fig
