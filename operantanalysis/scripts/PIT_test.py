#!/usr/bin/env python3

from operantanalysis import loop_over_days, extract_info_from_file, lever_pressing, display_line_graph
import pandas as pd


import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt  # noqa
from sys import argv
import os
import datetime


column_list = ['Subject', 'Day', 'CS+ Lever Presses', 'CS- Lever Presses']


def PIT_test_function(loaded_file, i):
    """
    :param loaded_file: file output from operant box
    :param i: number of days analyzing
    :return: data frame of all analysis extracted from file (one animal)
    """
    (timecode, eventcode) = extract_info_from_file(loaded_file, 500)
    (csplus_presses, csmin_presses, total_presses) = lever_pressing(eventcode, 'ActivePress', 'InactivePress')


    file_keys = list(loaded_file.keys())
    for constant in ['File', 'Start Date', 'End Date', 'Subject', 'Experiment', 'Group', 'Box', 'Start Time', 'End Time', 'MSN', 'W']:
        file_keys.remove(constant)

    # All that's left in the list file_keys should be any group labels. 
    group_ids = []
    for group in file_keys:
        group_ids.append(loaded_file[group])


    df2 = pd.DataFrame([[loaded_file['Subject'], int(i + 1), float(csplus_presses), float(csmin_presses), *group_ids]], columns=column_list+file_keys)
    return df2


# If user provided an argument at execution, use this to find data. 
try:
    data_directory = argv[1]
# Otherwise, store it as an empty string so loop_over_days knows to use GUI.
except IndexError:
    data_directory = ''

(days, df) = loop_over_days(column_list, PIT_test_function, master_data_folder = data_directory)



# If user provided multiple arguments at execution, use the second one as the save path for the output folder.
try:
    save_path = os.path.join(argv[2], 'output.xlsx')
    df.to_excel(save_path)
# Otherwise, save the DataFrame to the current working directory.
except IndexError:
    df.to_excel("output.xlsx")

print(df.to_string())





graph_toggle = input('Would you like to see graphs (Y/n)?    ')

if graph_toggle=='Y':
    cs_plus_pressing = display_line_graph(df, 'CS+ Lever Presses')
    cs_minus_pressing = display_line_graph(df, 'CS- Lever Presses')

    # The below is important to prevent hanging terminal after closing graph windows. 
    plt.show(block=False)
    plt.pause(0.001) 
    input("hit[enter] to end.")
    plt.close('all') # all open plots are correctly closed after each run)
