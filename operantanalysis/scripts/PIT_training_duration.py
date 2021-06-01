#!/usr/bin/env python3


from operantanalysis import loop_over_days, extract_info_from_file, cue_responding_duration, display_line_graph
import pandas as pd

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt  # noqa
from sys import argv
import os
import datetime



column_list = ['Subject', 'Condition', 'Day', 'CS+ Pokes Duration', 'CS+ ITI', 'CS- Pokes Duration',
               'CS- ITI', 'CS+ Elevation Score', 'CS- Elevation Score']


def PIT_training_function(loaded_file, i):
    """
    :param loaded_file: file output from operant box
    :param i: number of days analyzing
    :return: data frame of all analysis extracted from file (one animal)
    """

    (timecode, eventcode) = extract_info_from_file(loaded_file, 500)
    (A_dur_individual, A_dur_total, AITI_dur_individual, AITI_dur_total) = cue_responding_duration(timecode, eventcode, 'ExcitorATrialStart', 'ExcitorATrialEnd', 'PokeOn1', 'PokeOff1')
    (B_dur_individual, B_dur_total, BITI_dur_individual, BITI_dur_total) = cue_responding_duration(timecode, eventcode, 'ExcitorBTrialStart', 'ExcitorBTrialEnd', 'PokeOn1', 'PokeOff1')
   

    file_keys = list(loaded_file.keys())
    for constant in ['File', 'Start Date', 'End Date', 'Subject', 'Experiment', 'Group', 'Box', 'Start Time', 'End Time', 'MSN', 'W']:
        file_keys.remove(constant)

    # All that's left in the list file_keys should be any group labels. 
    group_ids = []
    for group in file_keys:
        group_ids.append(loaded_file[group])


    df2 = pd.DataFrame([[loaded_file['Subject'], loaded_file['MSN'], int(i + 1),
                         float(A_dur_total), float(AITI_dur_total), float(B_dur_total), float(BITI_dur_total),
                         float(A_dur_total-AITI_dur_total), float(B_dur_total-BITI_dur_total), *group_ids]], columns=column_list+file_keys)

    return df2



# If user provided an argument at execution, use this to find data. 
try:
    data_directory = argv[1]
# Otherwise, store it as an empty string so loop_over_days knows to use GUI.
except IndexError:
    data_directory = ''


(days, df) = loop_over_days(column_list, PIT_training_function, master_data_folder=data_directory)
print(df.to_string())


# If user provided multiple arguments at execution, use the second one as the save path for the output folder.
try:
    save_path = os.path.join(argv[2], 'output.xlsx')
    df.to_excel(save_path)
# Otherwise, save the DataFrame to the current working directory.
except IndexError:
    df.to_excel("output.xlsx")




graph_toggle = input('Would you like to see graphs of CS+ Responding (Y/n)?    ')

if graph_toggle=='Y':
    poke_rate = display_line_graph(df, 'CS+ Pokes Duration')
    elevation_score = display_line_graph(df, 'CS+ Elevation Score')

    # The below is important to prevent hanging terminal after closing graph windows. 
    plt.show(block=False)
    plt.pause(0.001) 
    input("hit[enter] to end.")
    plt.close('all') # all open plots are correctly closed after each run)
