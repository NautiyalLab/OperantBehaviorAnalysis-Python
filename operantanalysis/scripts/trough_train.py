#!/usr/bin/env python3

from operantanalysis import loop_over_days, extract_info_from_file, reward_retrieval, cue_responding_duration,\
    total_head_pokes, display_line_graph
import pandas as pd
import matplotlib.pyplot as plt
from sys import argv
import os

column_list = ['Subject', 'Day', 'Dippers', 'Dippers Retrieved', 'Retrieval Latency', 'Avg Poke Dur', 'Tot Poke Dur',
               'Total Pokes Count']


def trough_train_function(loaded_file, i):
    """
    :param loaded_file: file output from operant box
    :param i: number of days analyzing
    :return: data frame of all analysis extracted from file (one animal)
    """
    (timecode, eventcode) = extract_info_from_file(loaded_file, 500)
    (dippers, dippers_retrieved, retrieval_latency) = reward_retrieval(timecode, eventcode)
    (ind_dur, tot_dur, ind_dur_iti, tot_dur_iti) = cue_responding_duration(timecode, eventcode, 'StartSession', 'EndSession', "PokeOn1", "PokeOff1")
    # ITI is meaningless here because we are using the whole session
    total_pokes = total_head_pokes(eventcode)

    file_keys = list(loaded_file.keys())
    for constant in ['File', 'Start Date', 'End Date', 'Subject', 'Experiment', 'Group', 'Box', 'Start Time', 'End Time', 'MSN', 'W']:
        file_keys.remove(constant)

    # All that's left in the list file_keys should be any group labels. 
    group_ids = []
    for group in file_keys:
        group_ids.append(loaded_file[group])

    df2 = pd.DataFrame([[loaded_file['Subject'], int(i + 1), float(dippers), float(dippers_retrieved),
                         float(retrieval_latency), float(ind_dur), float(tot_dur), float(total_pokes), *group_ids]],
                       columns=column_list+file_keys)

    return df2

# If user provided an argument at execution, use this to find data. 
try:
    data_directory = argv[1]
# Otherwise, store it as an empty string so loop_over_days knows to use GUI.
except IndexError:
    data_directory = ''

(days, df) = loop_over_days(column_list, trough_train_function, master_data_folder=data_directory)
print(df.to_string())


# If user provided multiple arguments at execution, use the second one as the save path for the output folder.
try:
    save_path = os.path.join(argv[2], 'output.xlsx')
    df.to_excel(save_path)
# Otherwise, save the DataFrame to the current working directory.
except IndexError:
    df.to_excel("output.xlsx")



graph_toggle = input('Would you like to see graphs of dipper retrieval and latency (Y/n)?    ')

if graph_toggle=='Y':
    latency_DF = display_line_graph(df, 'Retrieval Latency')
    dipper_DF = display_line_graph(df, 'Dippers Retrieved')
    # The below is important to prevent hanging terminal after closing graph windows. 
    plt.show(block=False)
    plt.pause(0.001) 
    input("hit[enter] to end.")
    plt.close('all') # all open plots are correctly closed after each run)
