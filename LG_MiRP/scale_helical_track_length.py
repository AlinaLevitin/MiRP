"""
Author: Alina Levitin
Date: 26/02/24
Version: 1.0
"""

import starfile
import os


def scale_helical_track_length(star_file, bin):

    scale_factor = float(1/bin)
    # Read STAR file using starfile package
    try:
        data = starfile.read(star_file)
        print(
            f'This star file contains {len(data.keys())} data blocks: {[data_block for data_block in data.keys()]}')
    except Exception as e:
        print("Error:", e)
        return

    # Check if data is empty
    if not data:
        print("Error: Empty DataFrame")
        return

    # Modify the column containing helical track length
    df = data['particles']
    df.loc[:, 'rlnHelicalTrackLengthAngst'] = df.loc[:, 'rlnHelicalTrackLengthAngst'] * scale_factor

    # Write modified data to a new STAR file
    output_file = f'scaled_helical_track_length_binning_{bin}.star'
    if output_file not in os.listdir(os.getcwd()):
        try:
            starfile.write(data, output_file)
            print(f'File was saved to {os.getcwd()}\\{output_file} ')
        except Exception as e:
            print("Error:", e)
    else:
        print(f'File named {os.getcwd()}\\{output_file} already exists')


def scale(star_entry, bin: int=4):
    # Get input values from GUI
    star_file = star_entry.get()

    # Call function to scale helical track length
    scale_helical_track_length(star_file, bin)


