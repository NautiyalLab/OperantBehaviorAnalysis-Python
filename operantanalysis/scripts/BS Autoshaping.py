from operantanalysis import cue_responding_duration, get_events_indices, cue_iti_responding
import pandas as pd
import csv
import os
import glob
from tkinter import *  # noqa

column_list = ['Subject', 'Day', 'CS+ Dur', 'CS- Dur', 'CS+ Approach Count', 'CS- Approach Count',
               'CS+ Goal Dur', 'CS- Goal Dur', 'CS+ Goal Approach Count', 'CS- Goal Approach Count']
def loop_over_days_BS(column_list, behavioral_test_function):
    """
    :param column_list: list of strings/column titles for analysis that will be output in a table
    :param behavioral_test_function: function that contains all the analysis functions to run on each file
    :return: one concatenated data table of analysis for each animal for each day specified
    """
    days = int(input("How many days would you like to analyze?"))
    df = pd.DataFrame(columns=column_list)

    for i in range(days):
        root = Tk()  # noqa
        root.withdraw()
        folder_selected = filedialog.askdirectory()
        file_pattern = os.path.join(folder_selected, '*')
        for loaded_file in sorted(glob.glob(file_pattern)):
            df2 = behavioral_test_function(loaded_file, i)
            df = df.append(df2, ignore_index=True)

    return days, df

def BS_Auto_function(loaded_file, i):
    """
    :param loaded_file: file output from operant box
    :param i: number of days analyzing
    :return: data frame of all analysis extracted from file (one animal)
    """

    with open(loaded_file) as csv_file:
        csv_reader = csv.reader(csv_file)
        rows = list(csv_reader)
        ID = rows[10]

    RawData = pd.read_csv(loaded_file, skiprows=19,
                          usecols=['Evnt_Time', 'Evnt_Name',
                                   'Item_Name', 'Alias_Name',
                                   'Arg1_Name', 'Arg1_Value'])
    RawData["eventcode"] = RawData['Evnt_Name'].astype(str) + "-" + RawData['Item_Name'].astype(str) + "-" + \
                           RawData['Alias_Name'].astype(str) + "-" + RawData['Arg1_Name'].astype(str) + "-" + \
                           RawData['Arg1_Value'].astype(str)
    RawData["timecode"] = RawData['Evnt_Time']
    RawData = RawData[['timecode', "eventcode"]]
    timecode = RawData["timecode"].tolist()
    eventcode = RawData["eventcode"].tolist()

    first_filter = get_events_indices(eventcode, ['Whisker - Display Image-Bussey Mouse Autoshaping Mode-Background-Position-1.0',
                                              'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Background-Position-2.0'])
    eventcode.pop(first_filter[1])
    eventcode.pop(first_filter[0])

# need to filter to contain only pertinent events for tray entries during lit cs
    filtered2 = get_events_indices(eventcode, ['Variable Event-CS_Plus-nan-Value-2.0','Variable Event-CS_Plus-nan-Value-1.0',
                                              'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Images-Position-2.0',
                                              'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Background-Position-2.0',
                                              'Input Transition On Event-Tray #1-nan-nan-nan',
                                              'Input Transition Off Event-Tray #1-nan-nan-nan',
                                              'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Images-Position-1.0',
                                              'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Background-Position-1.0',
                                              'Schedule Startup Event-(SYSTEM)-nan-nan-nan',
                                              'Schedule Shutdown Event-(SYSTEM)-nan-nan-nan'])
    filtered_ec2 = list(map(lambda z: eventcode[z], filtered2))
    filtered_tc2 = list(map(lambda z: timecode[z], filtered2))
    # need to exclude first background instance

    if 'Variable Event-CS_Plus-nan-Value-2.0' in filtered_ec2:
        (A_dur_individual2, A_dur_total2, AITI_dur_individual2, AITI_dur_total2) = cue_responding_duration(filtered_tc2,
                                                                                                       filtered_ec2,
                                                                                                       'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Images-Position-2.0',
                                                                                                       'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Background-Position-2.0',
                                                                                                       'Input Transition On Event-Tray #1-nan-nan-nan',
                                                                                                       'Input Transition Off Event-Tray #1-nan-nan-nan')
        (B_dur_individual2, B_dur_total2, BITI_dur_individual2, BITI_dur_total2) = cue_responding_duration(filtered_tc2,
                                                                                                       filtered_ec2,
                                                                                                       'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Images-Position-1.0',
                                                                                                       'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Background-Position-1.0',
                                                                                                       'Input Transition On Event-Tray #1-nan-nan-nan',
                                                                                                       'Input Transition Off Event-Tray #1-nan-nan-nan')
        (A_total2, AITI_total2) = cue_iti_responding(filtered_tc2, filtered_ec2, 'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Images-Position-2.0',
                                                        'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Background-Position-2.0',
                                                        'Input Transition On Event-Tray #1-nan-nan-nan')

        (B_total2, BITI_total2) = cue_iti_responding(filtered_tc2, filtered_ec2,
                                                        'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Images-Position-1.0',
                                                        'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Background-Position-1.0',
                                                        'Input Transition On Event-Tray #1-nan-nan-nan')
    else:
        (A_dur_individual2, A_dur_total2, AITI_dur_individual2, AITI_dur_total2) = cue_responding_duration(filtered_tc2,
                                                                                                       filtered_ec2,
                                                                                                       'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Images-Position-1.0',
                                                                                                       'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Background-Position-1.0',
                                                                                                       'Input Transition On Event-Tray #1-nan-nan-nan',
                                                                                                       'Input Transition Off Event-Tray #1-nan-nan-nan')
        (B_dur_individual2, B_dur_total2, BITI_dur_individual2, BITI_dur_total2) = cue_responding_duration(filtered_tc2,
                                                                                                       filtered_ec2,
                                                                                                       'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Images-Position-2.0',
                                                                                                       'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Background-Position-2.0',
                                                                                                       'Input Transition On Event-Tray #1-nan-nan-nan',
                                                                                                       'Input Transition Off Event-Tray #1-nan-nan-nan')
        (A_total2, AITI_total2) = cue_iti_responding(filtered_tc2, filtered_ec2,
                                                   'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Images-Position-1.0',
                                                   'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Background-Position-1.0',
                                                   'Input Transition On Event-Tray #1-nan-nan-nan')

        (B_total2, BITI_total2) = cue_iti_responding(filtered_tc2, filtered_ec2,
                                                   'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Images-Position-2.0',
                                                   'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Background-Position-2.0',
                                                   'Input Transition On Event-Tray #1-nan-nan-nan')

# need to filter to contain only pertinent events for beam breaks during lit cs
    filtered = get_events_indices(eventcode, ['Variable Event-CS_Plus-nan-Value-2.0',
                                              'Variable Event-CS_Plus-nan-Value-1.0',
                                              'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Images-Position-2.0',
                                              'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Background-Position-2.0',
                                              'Input Transition On Event-RightFIRBeam #1-nan-nan-nan',
                                              'Input Transition Off Event-RightFIRBeam #1-nan-nan-nan',
                                              'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Images-Position-1.0',
                                              'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Background-Position-1.0',
                                              'Input Transition On Event-FIRBeam #1-nan-nan-nan',
                                              'Input Transition Off Event-FIRBeam #1-nan-nan-nan',
                                              'Schedule Shutdown Event-(SYSTEM)-nan-nan-nan',
                                              'Schedule Startup Event-(SYSTEM)-nan-nan-nan'])
    filtered_ec = list(map(lambda z: eventcode[z], filtered))
    filtered_tc = list(map(lambda z: timecode[z], filtered))
# need to exclude first background instance

    if 'Variable Event-CS_Plus-nan-Value-2.0' in filtered_ec:
        (A_dur_individual, A_dur_total, AITI_dur_individual, AITI_dur_total) = cue_responding_duration(filtered_tc,
                                                                                                       filtered_ec,
                                                                                                       'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Images-Position-2.0',
                                                                                                       'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Background-Position-2.0',
                                                                                                       'Input Transition On Event-RightFIRBeam #1-nan-nan-nan',
                                                                                                       'Input Transition Off Event-RightFIRBeam #1-nan-nan-nan')
        (B_dur_individual, B_dur_total, BITI_dur_individual, BITI_dur_total) = cue_responding_duration(filtered_tc,
                                                                                                       filtered_ec,
                                                                                                       'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Images-Position-1.0',
                                                                                                       'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Background-Position-1.0',
                                                                                                       'Input Transition On Event-FIRBeam #1-nan-nan-nan',
                                                                                                       'Input Transition Off Event-FIRBeam #1-nan-nan-nan')
        (A_total, AITI_total) = cue_iti_responding(filtered_tc, filtered_ec,
                                                   'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Images-Position-2.0',
                                                   'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Background-Position-2.0',
                                                   'Input Transition On Event-RightFIRBeam #1-nan-nan-nan')

        (B_total, BITI_total) = cue_iti_responding(filtered_tc, filtered_ec,
                                                   'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Images-Position-1.0',
                                                   'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Background-Position-1.0',
                                                   'Input Transition On Event-FIRBeam #1-nan-nan-nan')
    else:
        (A_dur_individual, A_dur_total, AITI_dur_individual, AITI_dur_total) = cue_responding_duration(filtered_tc,
                                                                                                       filtered_ec,
                                                                                                       'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Images-Position-1.0',
                                                                                                       'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Background-Position-1.0',
                                                                                                       'Input Transition On Event-FIRBeam #1-nan-nan-nan',
                                                                                                       'Input Transition Off Event-FIRBeam #1-nan-nan-nan')
        (B_dur_individual, B_dur_total, BITI_dur_individual, BITI_dur_total) = cue_responding_duration(filtered_tc,
                                                                                                       filtered_ec,
                                                                                                       'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Images-Position-2.0',
                                                                                                       'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Background-Position-2.0',
                                                                                                       'Input Transition On Event-RightFIRBeam #1-nan-nan-nan',
                                                                                                       'Input Transition Off Event-RightFIRBeam #1-nan-nan-nan')
        (A_total, AITI_total) = cue_iti_responding(filtered_tc, filtered_ec,
                                                   'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Images-Position-1.0',
                                                   'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Background-Position-1.0',
                                                   'Input Transition On Event-FIRBeam #1-nan-nan-nan')

        (B_total, BITI_total) = cue_iti_responding(filtered_tc, filtered_ec,
                                                   'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Images-Position-2.0',
                                                   'Whisker - Display Image-Bussey Mouse Autoshaping Mode-Background-Position-2.0',
                                                   'Input Transition On Event-RightFIRBeam #1-nan-nan-nan')

    df2 = pd.DataFrame([[ID, int(i + 1), float(A_dur_total), float(B_dur_total), float(A_total), float(B_total), float(A_dur_total2), float(B_dur_total2), float(A_total2), float(B_total2)]],
                       columns=column_list)

    return df2

(days, df) = loop_over_days_BS(column_list, BS_Auto_function)
print(df.to_string())
df.to_excel("output.xlsx")
