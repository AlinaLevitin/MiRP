import starfile


def scale_helical_track_length(star_file, upscale_factor):
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
    df.loc[:, 'rlnHelicalTrackLengthAngst'] = df.loc[:, 'rlnHelicalTrackLengthAngst'] * upscale_factor

    print(data['particles'])

    # Write modified data to a new STAR file
    # output_file = star_file.replace('.star', '_scaled_helical_track_length.star')
    starfile.write(data, 'scaled_helical_track_length.star')


def scale(star_entry, factor_entry=0.25):
    # Get input values from GUI
    star_file = star_entry.get()
    upscale_factor = float(factor_entry)

    # Call function to scale helical track length
    scale_helical_track_length(star_file, upscale_factor)


