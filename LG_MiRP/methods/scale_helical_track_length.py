"""
Author: Alina Levitin
Date: 26/02/24
Updated: 1/3/24

Method to scale helical track length
Updating the _rlnHelicalTrackLengthAngst column in the particles star file
According to moors-lab readme file, relion at that time wasn't able to update the star file automatically after binning
I don't implement this method, but it's here just in case we will need it
"""

import starfile
import os


def scale_helical_track_length(star_entry, binning):
    """
    Method to scale helical track according to the binning

    :param star_entry: particles star file from entry
    :param binning: binning used
    :return: updates the _rlnHelicalTrackLengthAngst column and generates a new star file with the binning in the name
    """

    scale_factor = float(1 / binning)
    # Read STAR file using starfile package
    star_file = star_entry.get()
    data = starfile.read(star_file)

    # Modify the column containing helical track length
    df = data['particles']
    df.loc[:, 'rlnHelicalTrackLengthAngst'] = df.loc[:, 'rlnHelicalTrackLengthAngst'] * scale_factor

    # Write modified data to a new STAR file
    output_file = f'scaled_helical_track_length_binning_{binning}.star'
    if output_file not in os.listdir(os.getcwd()):
        try:
            starfile.write(data, output_file)
            print(f'File was saved to {os.getcwd()}\\{output_file} ')
        except Exception as e:
            print("Error:", e)
    else:
        print(f'File named {os.getcwd()}\\{output_file} already exists')
