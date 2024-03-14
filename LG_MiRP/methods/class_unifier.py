"""
Author: Alina Levitin
Date: 14/03/24
Updated: 14/3/24

Method to unify classes by protofilament numbers after 3D-classification
The method counts how many times each class was assigned to segments of the same MT and assign the most common class
to all the MT segments
"""
import starfile
import pandas as pd


def class_unifier(star_file_input):

    # Read data from "run_it001_data.star" using starfile

    data = starfile.read(star_file_input.get())



# # Define getmode function
# def most_common_class(v):
#     uniqv, counts = np.unique(v, return_counts=True)
#     return uniqv[np.argmax(counts)]
#
# # Calculate mode of ClassNumber for each combination of GroupNumber and HelicalTubeID
# modeDataset = data.groupby(['GroupNumber', 'HelicalTubeID']).agg(ClassNumber2=('ClassNumber', getmode)).reset_index()
#
# # Merge original data with modeDataset
# y_df = pd.merge(x_df, modeDataset, on=['GroupNumber', 'HelicalTubeID'], how='left')
#
# # Write the merged data to a new STAR file "run_it001_data_corrected01.star"
# y = starfile.DataLoop()
# y['GroupNumber'] = y_df['GroupNumber']
# y['HelicalTubeID'] = y_df['HelicalTubeID']
# y['ClassNumber'] = y_df['ClassNumber']
# y['ClassNumber2'] = y_df['ClassNumber2']
# y.save("run_it001_data_corrected01.star")
#
# print("Data processing and saving to STAR file completed.")
