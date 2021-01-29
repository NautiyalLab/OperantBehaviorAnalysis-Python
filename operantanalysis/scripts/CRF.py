#!/usr/bin/env python3

from operantanalysis import loop_over_days, extract_info_from_file, reward_retrieval, lever_pressing, display_line_graph
#    lever_press_latency, cue_iti_responding
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt  # noqa
from sys import argv
import os

column_list = ['Subject', 'Day', 'Dippers', 'Dippers Retrieved', 'Retrieval Latency',
               'Left Lever Presses', 'Right Lever Presses', 'Total Presses']


def crf_function(loaded_file, i):
    """
    :param loaded_file: file output from operant box
    :param i: number of days analyzing
    :return: data frame of all analysis extracted from file (one animal)
    """
    (timecode, eventcode) = extract_info_from_file(loaded_file, 500)
    (dippers, dippers_retrieved, retrieval_latency) = reward_retrieval(timecode, eventcode)
    (left_presses, right_presses, total_presses) = lever_pressing(eventcode, 'LPressOn', 'RPressOn')

#    Use this code for latencies and rates
#
#    if 'LLeverOn' in eventcode:
#        press_latency = lever_press_latency(timecode, eventcode, 'LLeverOn', 'LPressOn')
#        (lever_press_rate, iti_rate) = cue_iti_responding(timecode, eventcode, 'StartSession', 'EndSession', 'LPressOn')
#    elif 'RLeverOn' in eventcode:
#        press_latency = lever_press_latency(timecode, eventcode, 'RLeverOn', 'RPressOn')
#        (lever_press_rate, iti_rate) = cue_iti_responding(timecode, eventcode, 'StartSession', 'EndSession', 'RPressOn')
        
    df2 = pd.DataFrame([[loaded_file['Subject'], int(i + 1), float(dippers),
                         float(dippers_retrieved), float(retrieval_latency), float(left_presses),
                         float(right_presses), float(total_presses)]], columns=column_list)
    
    return df2

# If user provided an argument at execution, use this to find data. 
try:
    data_directory = argv[1]
# Otherwise, store it as an empty string so loop_over_days knows to use GUI.
except IndexError:
    data_directory = ''


(days, df) = loop_over_days(column_list, crf_function, master_data_folder=data_directory)
print(df.to_string())

# If user provided multiple arguments at execution, use the second one as the save path for the output folder.
try:
    save_path = os.path.join(argv[2], 'output.xlsx')
    df.to_excel(save_path)
# Otherwise, save the DataFrame to the current working directory.
except IndexError:
    df.to_excel("output.xlsx")


graph_toggle = input('Would you like to see graphs of dipper retrieval, latency, and lever presses (Y/n)?    ')

if graph_toggle=='Y':
    latency_DF = display_line_graph(df, 'Retrieval Latency')
    dipper_DF = display_line_graph(df, 'Dippers Retrieved')
    lever_DF = display_line_graph(df, 'Total Presses')

    # The below is important to prevent hanging terminal after closing graph windows. 
    plt.show(block=False)
    plt.pause(0.001) 
    input("hit[enter] to end.")
    plt.close('all') # all open plots are correctly closed after each run)
