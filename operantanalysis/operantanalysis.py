import statistics
import os
import glob
from tkinter import filedialog
from tkinter import *  # noqa
import pandas as pd
from .eventcodes import eventcodes_dictionary
from natsort import natsorted, ns

__all__ = ["loop_over_days", "load_file", "concat_lickometer_files",
           "extract_info_from_file", "DNAMIC_extract_info_from_file",
           "DNAMIC_loop_over_days", "get_events_indices", "reward_retrieval", "cue_iti_responding",
           "cue_iti_responding_PavCA", "binned_responding",
           "cue_responding_duration", "lever_pressing", "lever_press_latency", "lever_press_latency_PavCA",
           "total_head_pokes", "binned_responding_duration",
           "num_successful_go_nogo_trials", "count_go_nogo_trials", "num_switch_trials", "bin_by_time",
           "lever_press_lat_gng", "RVI_gng_weird", "RVI_nogo_latency", "lever_press_latency_Switch",
           "response_rate_across_cue_iti", "duration_across_cue_iti", "duration_across_trace_iti", "closest",
           "cue_iti_responding_subset"]


def loop_over_days(column_list, behavioral_test_function):
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
        for file in sorted(glob.glob(file_pattern)):
            loaded_file = load_file(file)
            df2 = behavioral_test_function(loaded_file, i)
            df = df.append(df2, ignore_index=True)

    return days, df


def loop_over_days_lickometer(column_list, behavioral_test_function):
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
        for file in sorted(glob.glob(file_pattern)):
            loaded_file = load_file(file)
            df2 = behavioral_test_function(loaded_file, i)
            df = df.append(df2, ignore_index=True)

    return days, df


def load_file(filename):
    """
    :param filename: string that refers to single operant file location, file is txt
    :return: dictionary of all the fields and their values contained in the file (like subject, group, or w array)
    """
    with open(filename, "r") as fileref:
        filelines = fileref.readlines()

    fields_dictionary = {}

    for line in filelines:
        if line[0] != ' ' and line[0] != '\n':
            name = line.split(':')[0]
            fields_dictionary[name] = line.replace(name + ':', '')
            fields_dictionary[name] = fields_dictionary[name].replace('\n', '')
            fields_dictionary[name] = fields_dictionary[name].replace(' ', '')
        elif line[0] == ' ':
            fields_dictionary[name] += line
            fields_dictionary[name] = fields_dictionary[name].replace('\n', '')

    group_identities = fields_dictionary['Group'].split('/')
    fields_dictionary['Group'] = group_identities.pop(0)

    for remaining in group_identities:
        if ':' in remaining:
            next_group = remaining.split(':')
            fields_dictionary[next_group[0]] = next_group[1]

    return fields_dictionary


def concat_lickometer_files():
    """
    :return: data frame for lickometer analysis
    """

    files_list = []
    root = Tk();
    root.withdraw()

    home = os.path.expanduser('~')  # returns the home directory on any OS --> ex) /Users/jhl
    selected_folder = filedialog.askdirectory(initialdir=home)
    file_pattern = os.path.join(selected_folder, '*.txt')
    data_dict = {}
    for fname in natsorted(glob.glob(file_pattern), alg=ns.IGNORECASE):  # loop through all the txt files
        with open(fname, "r") as file:
            filelines = file.readlines()  # read the lines in each file
            subject_line = filelines[5]  # Animal ID will always be at the 6th index (5+1)
            subject = subject_line.split(",")[-1].strip()  # subject will be the last element, strip any whitespaces!
            values = filelines[-1].strip().split(",")  # Need to split by delimiter in order to make the list!
            data_dict[subject] = values
    lick_df = pd.DataFrame.from_dict(data_dict, orient='index')
    lick_final = lick_df.T

    # Delete row at index position 0 & 1
    lick_final = lick_final.drop([lick_final.index[0]])  # to get rid of row of ones at top
    lick_final.reset_index(inplace=True)

    for c in lick_final.columns:
        lick_final[c] = pd.to_numeric(lick_final[c], errors='coerce')

    lick_final = lick_final.drop(lick_final.columns[[0]], axis=1)
    lick_final.fillna(value=pd.np.nan, inplace=True)

    lick_final.rename(columns=lick_final.iloc[0]).drop(lick_final.index[0])
    lick_final.to_excel("output.xlsx")

    return lick_final


def extract_info_from_file(dictionary_from_file, time_conversion):
    """
    :param dictionary_from_file: dictionary of all the fields and their values contained in the file (like subject, group, or w array)
    :param time_conversion: conversion number the timecode needs to be divided by to get seconds
    :return: timecode and eventcode lists derived from the w array
    """
    time_event_codes = dictionary_from_file["W"].split()

    for num in time_event_codes:
        if ':' in num:
            time_event_codes.remove(num)
    for num in time_event_codes:
        time_event_codes[time_event_codes.index(num)] = str(int(float(num)))

    timecode = []
    eventcode = []
    first_timecode = (float(time_event_codes[0][:-4]) / time_conversion)

    for num in time_event_codes:
        if num == time_event_codes[0]:
            timecode += [0.0]
        else:
            timecode += [round((float(num[:-4]) / time_conversion) - first_timecode, 2)]
        eventcode += [eventcodes_dictionary[int(num[-4:])]]

    return timecode, eventcode


def DNAMIC_loop_over_days(column_list, behavioral_test_function):
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
        for file in sorted(glob.glob(file_pattern)):
            (eventcode, timecode, fields_dictionary) = DNAMIC_extract_info_from_file(file)
            df2 = behavioral_test_function(eventcode, timecode, fields_dictionary, i)
            df = df.append(df2, ignore_index=True)

    return days, df


def DNAMIC_extract_info_from_file(filename):
    df = pd.read_csv(filename, sep=':', names=['event', 'timestamp'])
    df['timestamp'] = df['timestamp'].str.strip()

    # 0, 0, 0 appears after successful initialization --> serves as a cutoff mark

    end_of_init_idx = df.loc[df['timestamp'] == '0'].index[-1]
    body_start_idx = end_of_init_idx + 1

    keys = df[:body_start_idx]['event'].tolist()
    values = df[:body_start_idx]['timestamp'].tolist()
    fields_dictionary = dict(zip(keys, values))

    df_body = df[body_start_idx:-2]

    eventcode = df_body['event'].tolist()
    eventcode = [eventcodes_dictionary[int(i)] for i in eventcode]
    timecode = df_body['timestamp'].tolist()
    timecode = [int(i) / 1000 for i in timecode]

    return eventcode, timecode, fields_dictionary


def get_events_indices(eventcode, eventtypes):
    """
    :param eventcode: list of event codes from operant conditioning file
    :param eventtypes: list of event types to index
    :return: list of indices of target events
    """
    return [i for i, event in enumerate(eventcode) if event in eventtypes]


def reward_retrieval(timecode, eventcode):
    """
    :param timecode: list of time codes from operant conditioning file
    :param eventcode: list of event codes from operant conditioning file
    :return: number of reinforcers (dippers) presented, number retrieved, and latency to retrieve as floats
    """
    dip_on = get_events_indices(eventcode, ['DipOn'])
    dip_off = get_events_indices(eventcode, ['DipOff', 'EndSession'])
    poke_on = get_events_indices(eventcode, ['PokeOn1'])
    poke_off = get_events_indices(eventcode, ['PokeOff1'])
    dips_retrieved = 0
    latency_dip_retrieval = []

    for i in range(len(dip_on)):
        for x in range(len(poke_off)):
            dip_on_idx = dip_on[i]
            dip_off_idx = dip_off[i]
            if poke_on[x] < dip_on_idx < poke_off[x]:
                dips_retrieved += 1
                latency_dip_retrieval += [0]
                break
            elif 'PokeOn1' in eventcode[dip_on_idx:dip_off_idx]:
                dips_retrieved += 1
                poke_during_dip_idx = eventcode[dip_on_idx:dip_off_idx].index('PokeOn1')
                latency_dip_retrieval += [round(timecode[poke_during_dip_idx + dip_on_idx] - timecode[dip_on_idx], 2)]
                break

    if dips_retrieved == 0:
        return len(dip_on), dips_retrieved, 0
    else:
        return len(dip_on), dips_retrieved, round(statistics.mean(latency_dip_retrieval), 3)


def cue_iti_responding(timecode, eventcode, code_on, code_off, counted_behavior):
    """
    :param timecode: list of time codes from operant conditioning file
    :param eventcode: list of event codes from operant conditioning file
    :param code_on: event code for the beginning of a cue
    :param code_off: event code for the end of a cue
    :param counted_behavior: event code for counted behavior
    :return: mean rpm of head pokes during cue and mean rpm of head pokes during equivalent ITI preceding cue
    """
    cue_on = get_events_indices(eventcode, [code_on])
    cue_off = get_events_indices(eventcode, [code_off])
    if len(cue_on) != len(cue_off):
        cue_off += get_events_indices(eventcode, ['EndSession', 'Schedule Shutdown Event-(SYSTEM)-nan-nan-nan'])
    iti_on = get_events_indices(eventcode, [code_off, 'StartSession', 'Schedule Startup Event-(SYSTEM)-nan-nan-nan'])
    all_poke_rpm = []
    all_poke_iti_rpm = []

    for i in range(len(cue_on)):
        cue_on_idx = cue_on[i]
        cue_off_idx = cue_off[i]
        iti_on_idx = iti_on[i]
        cue_length_sec = (timecode[cue_off_idx] - timecode[cue_on_idx])
        if cue_length_sec > 0:
            poke_rpm = ((eventcode[cue_on_idx:cue_off_idx].count(counted_behavior)) / (cue_length_sec / 60))
        else:
            poke_rpm = 0
        all_poke_rpm += [poke_rpm]
        iti_poke = 0
        for x in range(iti_on_idx, cue_on_idx):
            if eventcode[x] == counted_behavior and timecode[x] >= (timecode[cue_on_idx] - cue_length_sec):
                iti_poke += 1
        if cue_length_sec > 0:
            iti_poke_rpm = iti_poke / (cue_length_sec / 60)
        else:
            iti_poke_rpm = 0
        all_poke_iti_rpm += [iti_poke_rpm]

    return round(statistics.mean(all_poke_rpm), 3), round(statistics.mean(all_poke_iti_rpm), 3)


def cue_iti_responding_subset(timecode, eventcode, code_on, code_off, counted_behavior, time):
    """
    :param timecode: list of time codes from operant conditioning file
    :param eventcode: list of event codes from operant conditioning file
    :param code_on: event code for the beginning of a cue
    :param code_off: event code for the end of a cue
    :param counted_behavior: event code for counted behavior
    :return: mean rpm of head pokes during cue and mean rpm of head pokes during equivalent ITI preceding cue
    """
    cue_on = get_events_indices(eventcode, [code_on])
    cue_off = get_events_indices(eventcode, [code_off])
    if len(cue_on) != len(cue_off):
        cue_off += get_events_indices(eventcode, ['EndSession'])
    iti_on = get_events_indices(eventcode, [code_off, 'StartSession'])
    all_poke_rpm = []
    all_poke_iti_rpm = []

    for i in range(len(cue_on)):
        cue_on_idx = cue_on[i]
        cue_off_idx = cue_off[i]
        iti_on_idx = iti_on[i]
        cue_length_sec = (timecode[cue_off_idx] - timecode[cue_on_idx])
        total_events = 0
        if cue_length_sec > 0:
            for y in range(cue_on_idx, cue_off_idx):
                if eventcode[y] == counted_behavior and timecode[y] <= (timecode[cue_on_idx] + time):
                    total_events += 1
            poke_rpm = total_events / (time / 60)
        else:
            poke_rpm = 0
        all_poke_rpm += [poke_rpm]
        iti_poke = 0
        for x in range(iti_on_idx, cue_on_idx):
            if eventcode[x] == counted_behavior and timecode[x] >= (timecode[cue_on_idx] - time):
                iti_poke += 1
        if cue_length_sec > 0:
            iti_poke_rpm = iti_poke / (time / 60)
        else:
            iti_poke_rpm = 0
        all_poke_iti_rpm += [iti_poke_rpm]

    return round(statistics.mean(all_poke_rpm), 3), round(statistics.mean(all_poke_iti_rpm), 3)


def cue_iti_responding_PavCA(timecode, eventcode, code_on, code_off, counted_behavior):
    """
    :param timecode: list of time codes from operant conditioning file
    :param eventcode: list of event codes from operant conditioning file
    :param code_on: event code for the beginning of a cue
    :param code_off: event code for the end of a cue
    :param counted_behavior: event code for counted behavior
    :return: mean rpm of head pokes during cue and mean rpm of head pokes during equivalent ITI preceding cue
    """
    cue_on = get_events_indices(eventcode, [code_on])
    cue_off = get_events_indices(eventcode, [code_off])
    if len(cue_on) != len(cue_off):
        cue_off += get_events_indices(eventcode, ['EndSession'])
    iti_on = get_events_indices(eventcode, [code_off, 'StartSession'])
    all_poke_rpm = []
    all_poke_iti_rpm = []

    for i in range(len(cue_on)):
        cue_on_idx = cue_on[i]
        cue_off_idx = cue_off[i]
        iti_on_idx = iti_on[i]
        cue_length_sec = (timecode[cue_off_idx] - timecode[cue_on_idx])
        if cue_length_sec > 0:
            poke_rpm = ((eventcode[cue_on_idx:cue_off_idx].count(counted_behavior)) / (cue_length_sec / 60))
        else:
            poke_rpm = 0
        all_poke_rpm += [poke_rpm]
        iti_poke = 0
        for x in range(iti_on_idx, cue_on_idx):
            if eventcode[x] == counted_behavior and timecode[x] >= (timecode[cue_on_idx] - cue_length_sec):
                iti_poke += 1
        if cue_length_sec > 0:
            iti_poke_rpm = iti_poke / (cue_length_sec / 60)
        else:
            iti_poke_rpm = 0
        all_poke_iti_rpm += [iti_poke_rpm]

    return round(statistics.mean(all_poke_rpm), 3), round(statistics.mean(all_poke_iti_rpm), 3), len(
        [j for j in all_poke_rpm if j > 0])


def binned_responding(timecode, eventcode, code_on, code_off, counted_behavior, trial_count):
    """
       :param timecode: list of time codes from operant conditioning file
       :param eventcode: list of event codes from operant conditioning file
       :param code_on: event code for the beginning of a cue
       :param code_off: event code for the end of a cue
       :param counted_behavior: event code for behavior you want counted
       :param trial_count: number of bins
       :return: mean rpm of head pokes during cue and mean rpm of head pokes during equivalent ITI preceding cue
       """
    cue_on = get_events_indices(eventcode, [code_on])
    cue_off = get_events_indices(eventcode, [code_off])
    iti_on = get_events_indices(eventcode, [code_off, 'StartSession'])
    all_poke_rpm = []
    all_poke_iti_rpm = []

    for i in range(trial_count):
        cue_on_idx = cue_on[i]
        cue_off_idx = cue_off[i]
        iti_on_idx = iti_on[i]
        cue_length_sec = (timecode[cue_off_idx] - timecode[cue_on_idx])
        poke_rpm = ((eventcode[cue_on_idx:cue_off_idx].count(counted_behavior)) / (cue_length_sec / 60))
        all_poke_rpm += [poke_rpm]
        iti_poke = 0
        for x in range(iti_on_idx, cue_on_idx):
            if eventcode[x] == counted_behavior and timecode[x] >= (timecode[cue_on_idx] - cue_length_sec):
                iti_poke += 1
        iti_poke_rpm = iti_poke / (cue_length_sec / 60)
        all_poke_iti_rpm += [iti_poke_rpm]

    return round(statistics.mean(all_poke_rpm), 3), round(statistics.mean(all_poke_iti_rpm), 3)

def binned_responding_duration(timecode, eventcode, code_on, code_off, counted_behavior_on, counted_behavior_off):
    """
       :param timecode: list of time codes from operant conditioning file
       :param eventcode: list of event codes from operant conditioning file
       :param code_on: event code for the beginning of a cue
       :param code_off: event code for the end of a cue
       :param counted_behavior: event code for behavior you want counted
       :param trial_count: number of bins
       :return: mean rpm of head pokes during cue and mean rpm of head pokes during equivalent ITI preceding cue
       """
    cue_on = get_events_indices(eventcode, [code_on])
    cue_off = get_events_indices(eventcode, [code_off])
    iti_on = get_events_indices(eventcode, [code_off, 'StartSession'])
    all_poke_dur = []
    all_iti_poke_dur = []
    all_cue_duration = []
    all_iti_duration = []

    for i in range(5):
        cue_on_idx = cue_on[i]
        cue_off_idx = cue_off[i]
        iti_on_idx = iti_on[i]
        cue_length_sec = (timecode[cue_off_idx] - timecode[cue_on_idx])
        in_cue_duration = 0
        iti_cue_duration = 0

        for x in range(cue_on_idx, cue_off_idx):
            if eventcode[x - 1] == code_on and eventcode[x] == counted_behavior_off:
                poke_dur = timecode[x] - timecode[x - 1]
                all_poke_dur += [poke_dur]
                in_cue_duration += poke_dur
            elif eventcode[x] == code_off and eventcode[x - 1] == code_on and eventcode[x + 1] == counted_behavior_off:
                poke_dur = timecode[x] - timecode[x - 1]
                all_poke_dur += [poke_dur]
                in_cue_duration += poke_dur
            elif eventcode[x] == counted_behavior_on and (
                    eventcode[x + 1] == counted_behavior_off or eventcode[x + 1] == code_off):
                poke_dur = timecode[x + 1] - timecode[x]
                all_poke_dur += [poke_dur]
                in_cue_duration += poke_dur
        all_cue_duration += [in_cue_duration]

        for x in range(iti_on_idx, cue_on_idx):
            if eventcode[x] == counted_behavior_on and timecode[x] >= (timecode[cue_on_idx] - cue_length_sec):
                if eventcode[x - 1] == code_on and eventcode[x] == counted_behavior_off:
                    poke_dur = timecode[x] - timecode[x - 1]
                    all_iti_poke_dur += [poke_dur]
                    iti_cue_duration += poke_dur
                elif eventcode[x] == code_off and eventcode[x - 1] == code_on and eventcode[
                    x + 1] == counted_behavior_off:
                    poke_dur = timecode[x] - timecode[x - 1]
                    all_iti_poke_dur += [poke_dur]
                    iti_cue_duration += poke_dur
                elif eventcode[x] == counted_behavior_on and (
                        eventcode[x + 1] == counted_behavior_off or eventcode[x + 1] == code_off):
                    poke_dur = timecode[x + 1] - timecode[x]
                    all_iti_poke_dur += [poke_dur]
                    iti_cue_duration += poke_dur
        all_iti_duration += [iti_cue_duration]

    if not all_cue_duration:
        all_cue_duration += [0]
    if not all_poke_dur:
        all_poke_dur += [0]
    if not all_iti_duration:
        all_iti_duration += [0]
    if not all_iti_poke_dur:
        all_iti_poke_dur += [0]

    return round(statistics.mean(all_poke_dur), 3), round(statistics.mean(all_cue_duration), 3), \
           round(statistics.mean(all_iti_poke_dur), 3), round(statistics.mean(all_iti_duration), 3)

def cue_responding_duration(timecode, eventcode, code_on, code_off, counted_behavior_on, counted_behavior_off):
    """
    :param timecode: list of time codes from operant conditioning file
    :param eventcode: list of event codes from operant conditioning file
    :param code_on: event code for the beginning of a cue
    :param code_off: event code for the end of a cue
    :param counted_behavior_off: event code for the beginning of target behavior
    :param counted_behavior_on: event code for the end of target behavior
    :return: mean duration of individual head pokes during cue, mean total duration of head poking during cue, also these for ITI preceeding cue
    """
    cue_on = get_events_indices(eventcode, [code_on])
    cue_off = get_events_indices(eventcode, [code_off])
    if len(cue_on) != len(cue_off):
        cue_off += get_events_indices(eventcode, ['EndSession', 'Schedule Shutdown Event-(SYSTEM)-nan-nan-nan'])
    iti_on = get_events_indices(eventcode, [code_off, 'StartSession', 'Schedule Startup Event-(SYSTEM)-nan-nan-nan'])
    all_poke_dur = []
    all_iti_poke_dur = []
    all_cue_duration = []
    all_iti_duration = []

    for i in range(len(cue_on)):
        cue_on_idx = cue_on[i]
        cue_off_idx = cue_off[i]
        iti_on_idx = iti_on[i]
        cue_length_sec = (timecode[cue_off_idx] - timecode[cue_on_idx])
        in_cue_duration = 0
        iti_cue_duration = 0

        for x in range(cue_on_idx, cue_off_idx):
            if eventcode[x - 1] == code_on and eventcode[x] == counted_behavior_off:
                poke_dur = timecode[x] - timecode[x - 1]
                all_poke_dur += [poke_dur]
                in_cue_duration += poke_dur
            elif eventcode[x] == code_off and eventcode[x - 1] == code_on and eventcode[x + 1] == counted_behavior_off:
                poke_dur = timecode[x] - timecode[x - 1]
                all_poke_dur += [poke_dur]
                in_cue_duration += poke_dur
            elif eventcode[x] == counted_behavior_on and (
                    eventcode[x + 1] == counted_behavior_off or eventcode[x + 1] == code_off):
                poke_dur = timecode[x + 1] - timecode[x]
                all_poke_dur += [poke_dur]
                in_cue_duration += poke_dur
        all_cue_duration += [in_cue_duration]

        for x in range(iti_on_idx, cue_on_idx):
            if eventcode[x] == counted_behavior_on and timecode[x] >= (timecode[cue_on_idx] - cue_length_sec):
                if eventcode[x - 1] == code_on and eventcode[x] == counted_behavior_off:
                    poke_dur = timecode[x] - timecode[x - 1]
                    all_iti_poke_dur += [poke_dur]
                    iti_cue_duration += poke_dur
                elif eventcode[x] == code_off and eventcode[x - 1] == code_on and eventcode[
                    x + 1] == counted_behavior_off:
                    poke_dur = timecode[x] - timecode[x - 1]
                    all_iti_poke_dur += [poke_dur]
                    iti_cue_duration += poke_dur
                elif eventcode[x] == counted_behavior_on and (
                        eventcode[x + 1] == counted_behavior_off or eventcode[x + 1] == code_off):
                    poke_dur = timecode[x + 1] - timecode[x]
                    all_iti_poke_dur += [poke_dur]
                    iti_cue_duration += poke_dur
        all_iti_duration += [iti_cue_duration]

    if not all_cue_duration:
        all_cue_duration += [0]
    if not all_poke_dur:
        all_poke_dur += [0]
    if not all_iti_duration:
        all_iti_duration += [0]
    if not all_iti_poke_dur:
        all_iti_poke_dur += [0]

    return round(statistics.mean(all_poke_dur), 3), round(statistics.mean(all_cue_duration), 3), \
           round(statistics.mean(all_iti_poke_dur), 3), round(statistics.mean(all_iti_duration), 3)


def lever_pressing(eventcode, lever1, lever2=False):
    """
    :param eventcode: list of event codes from operant conditioning file
    :param lever1: eventcode for lever pressing or
    :param lever2: optional parameter for second lever eventcode if two levers are used
    :return: count of first lever presses, second lever presses, and total lever presses, as int
    """
    lever1_presses = eventcode.count(lever1)

    if lever2:
        lever2_presses = eventcode.count(lever2)
    else:
        lever2_presses = 0

    total_lever_presses = lever1_presses + lever2_presses

    return lever1_presses, lever2_presses, total_lever_presses


def lever_press_latency(timecode, eventcode, lever_on, lever_press):
    """
    :param timecode: list of times (in seconds) when events occurred
    :param eventcode: list of events that happened in a session
    :param lever_on: event name for lever presentation
    :param lever_press: event name for lever press
    :return: the mean latency to press the lever in seconds
    """
    lever_on = get_events_indices(eventcode, [lever_on, 'EndSession'])
    press_latency = []

    for i in range(len(lever_on) - 1):
        lever_on_idx = lever_on[i]
        if lever_press in eventcode[lever_on_idx:lever_on[i + 1]]:
            lever_press_idx = eventcode[lever_on_idx:lever_on[i + 1]].index(lever_press)
            press_latency += [round(timecode[lever_on_idx + lever_press_idx] - timecode[lever_on_idx], 2)]
        else:
            pass

    if len(press_latency) > 0:
        return round(statistics.mean(press_latency), 3)
    else:
        return 0


def lever_press_latency_PavCA(timecode, eventcode, lever_on, lever_press, pres_len):
    """
    :param timecode: list of times (in seconds) when events occurred
    :param eventcode: list of events that happened in a session
    :param lever_on: event name for lever presentation
    :param lever_press: event name for lever press
    :return: the mean latency to press the lever in seconds
    """
    lever_on = get_events_indices(eventcode, [lever_on, 'EndSession'])
    press_latency = []

    for i in range(len(lever_on) - 1):
        lever_on_idx = lever_on[i]
        if lever_press in eventcode[lever_on_idx:lever_on[i + 1]]:
            lever_press_idx = eventcode[lever_on_idx:lever_on[i + 1]].index(lever_press)
            if round(timecode[lever_on_idx + lever_press_idx] - timecode[lever_on_idx], 2) <= pres_len:
                press_latency += [round(timecode[lever_on_idx + lever_press_idx] - timecode[lever_on_idx], 2)]
            else:
                press_latency += [10]
        else:
            press_latency += [10]

    if len(press_latency) > 0:
        return round(statistics.mean(press_latency), 3)
    else:
        return 0


def total_head_pokes(eventcode):
    """
    :param eventcode: list of event codes from operant conditioning file
    :return: total number of times animal poked head into reward receptacle
    """
    return eventcode.count('PokeOn1')


def num_successful_go_nogo_trials(eventcode):
    """
    :param eventcode: list of event codes from operant conditioning file
    :return: number of successful go and no go trials in the go/no go tasks
    """
    return eventcode.count('SuccessfulGoTrial'), eventcode.count('SuccessfulNoGoTrial')


def count_go_nogo_trials(eventcode):
    """
    :param eventcode: list of event codes from operant conditioning file
    :return: number of go and no go trials in the go/no go tasks
    """
    lever_on = get_events_indices(eventcode, ['RLeverOn', 'LLeverOn'])
    (go_trials, nogo_trials) = (0, 0)

    for lever in lever_on:
        if eventcode[lever + 1] in ('LightOn1', 'LightOn2'):
            nogo_trials += 1
        else:
            go_trials += 1

    return go_trials, nogo_trials


def num_switch_trials(eventcode):
    """
    :param eventcode: list of event codes from operant conditioning file
    :return: number of large and small rewards in the switch task
    """
    return eventcode.count('LargeReward'), eventcode.count('SmallReward')


def bin_by_time(timecode, eventcode, bin_length, counted_event):
    """
    :param timecode: list of time codes from operant conditioning file
    :param eventcode: list of event codes from operant conditioning file
    :param bin_length: length of time in seconds to split the session into
    :param counted_event: event that is counted in each bin, in list format
    :return: a list of counts of specified event for each bin
    """
    event_on_list = get_events_indices(eventcode, counted_event)

    if timecode[-1] % bin_length != 0:
        num_bins = int(timecode[-1] // bin_length) + 1
    elif timecode[-1] % bin_length == 0:
        num_bins = int(timecode[-1] // bin_length)
    counts_for_each_bin = [0] * num_bins

    for i in range(num_bins):
        for event_on in event_on_list:
            if (i + 1) != num_bins and (i + 1) * bin_length > timecode[event_on] >= i * bin_length:
                counts_for_each_bin[i] += 1
            elif (i + 1) == num_bins and timecode[event_on] >= i * bin_length:
                counts_for_each_bin[i] += 1

    return counts_for_each_bin


def lever_press_lat_gng(timecode, eventcode, lever_on, lever_press):
    """
    :param timecode: list of times (in seconds) when events occurred
    :param eventcode: list of events that happened in a session
    :param lever_on: event name for lever presentation
    :param lever_press: event name for lever press
    :return: the mean latency to press the lever in seconds
    """
    lever_on = get_events_indices(eventcode, [lever_on, 'EndSession'])
    press_latency = []

    for i in range(len(lever_on) - 1):
        lever_on_idx = lever_on[i]
        if lever_press in eventcode[lever_on_idx:lever_on[i + 1]]:
            lever_press_idx = eventcode[lever_on_idx:lever_on[i + 1]].index(lever_press)
            press_latency += [round(timecode[lever_on_idx + lever_press_idx] - timecode[lever_on_idx], 2)]
        else:
            pass

    if len(press_latency) > 0:
        return round(statistics.mean(press_latency), 3)
    else:
        return 0


def RVI_gng_weird(timecode, eventcode, lever_on, lever_press, cue_length):
    """
    :param timecode: list of times (in seconds) when events occurred
    :param eventcode: list of events that happened in a session
    :param lever_on: event name for lever presentation
    :param lever_press: event name for lever press
    :return: the mean latency to press the lever in seconds
    """
    lever_on = get_events_indices(eventcode, [lever_on, 'EndSession'])
    press_latency = []
    incorrect_trials = 0

    for i in range(len(lever_on) - 1):
        lever_on_idx = lever_on[i]
        if lever_press in eventcode[lever_on_idx:lever_on[i + 1]]:
            lever_press_idx = eventcode[lever_on_idx:lever_on[i + 1]].index(lever_press)
            press_latency += [round(timecode[lever_on_idx + lever_press_idx] - timecode[lever_on_idx], 2)]
        else:
            press_latency += [cue_length]

    final_press_latency = []

    for x in press_latency:
        if x > cue_length:
            incorrect_trials += 1
        else:
            final_press_latency += [x]

    if len(final_press_latency) > 0:
        return round(statistics.mean(final_press_latency), 3), incorrect_trials
    else:
        return 0, incorrect_trials


def RVI_nogo_latency(timecode, eventcode, lever_on, cue_length):
    """
    :param timecode: list of times (in seconds) when events occurred
    :param eventcode: list of events that happened in a session
    :param lever_on: event name or list for lever presentation
    :param lever_press: event name or list for lever press
    :return: the mean latency to press the lever in seconds
    """

    lever_on = get_events_indices(eventcode, [lever_on, 'EndSession'])
    press_latency = []

    for i in range(len(lever_on) - 1):
        lever_on_idx = lever_on[i]
        if 'LPressOn' in eventcode[lever_on_idx:lever_on[i + 1]]:
            lever_press_idx = eventcode[lever_on_idx:lever_on[i + 1]].index('LPressOn')
            if timecode[lever_on_idx + lever_press_idx] - timecode[lever_on_idx] < cue_length:
                press_latency += [round(timecode[lever_on_idx + lever_press_idx] - timecode[lever_on_idx], 2)]
        elif 'RPressOn' in eventcode[lever_on_idx:lever_on[i + 1]]:
            lever_press_idx = eventcode[lever_on_idx:lever_on[i + 1]].index('RPressOn')
            if timecode[lever_on_idx + lever_press_idx] - timecode[lever_on_idx] < cue_length:
                press_latency += [round(timecode[lever_on_idx + lever_press_idx] - timecode[lever_on_idx], 2)]
        else:
            press_latency += [cue_length]

    if len(press_latency) > 0:
        return round(statistics.mean(press_latency), 3)
    else:
        return 0


def lever_press_latency_Switch(timecode, eventcode):
    """
    :param timecode: list of times (in seconds) when events occurred
    :param eventcode: list of events that happened in a session
    :param lever_on: event name for lever presentation
    :param lever_press: event name for lever press
    :return: the mean latency to press the lever in seconds
    """
    lever_on = get_events_indices(eventcode, ['LLeverOn', 'RLeverOn', 'EndSession'])
    press_latency = []

    for i in range(len(lever_on) - 1):
        lever_on_idx = lever_on[i]
        if len(press_latency) < 10:
            if 'LPressOn' in eventcode[lever_on_idx:lever_on[i + 1]]:
                lever_press_idx = eventcode[lever_on_idx:lever_on[i + 1]].index('LPressOn')
                press_latency += [round(timecode[lever_on_idx + lever_press_idx] - timecode[lever_on_idx], 2)]
            elif 'RPressOn' in eventcode[lever_on_idx:lever_on[i + 1]]:
                lever_press_idx = eventcode[lever_on_idx:lever_on[i + 1]].index('RPressOn')
                press_latency += [round(timecode[lever_on_idx + lever_press_idx] - timecode[lever_on_idx], 2)]
            else:
                pass

    if len(press_latency) > 0:
        return round(statistics.mean(press_latency), 3)
    else:
        return 0


def response_rate_across_cue_iti(timecode, eventcode, code_on, code_off, counted_behavior):
    """
    :param timecode: list of times (in seconds) when events occurred
    :param eventcode: list of events that happened in a session
    :param code_on: event name for lever presentation
    :param code_off: event name for lever press
    :param code_off: event name for lever press
    :return: 3 lists of cue, iti, and the subtracted responding across seconds
    """
    cue_on = get_events_indices(eventcode, [code_on])
    cue_off = get_events_indices(eventcode, [code_off])
    if len(cue_on) != len(cue_off):
        cue_off += get_events_indices(eventcode, ['EndSession'])
    iti_on = get_events_indices(eventcode, [code_off, 'StartSession'])
    cue_length_sec = int(timecode[cue_off[6]] - timecode[cue_on[6]])
    all_cue_length_poke_rates = [0] * cue_length_sec
    all_iti_length_poke_rates = [0] * cue_length_sec

    for i in range(len(cue_on)):
        cue_on_idx = cue_on[i]
        cue_off_idx = cue_off[i]
        iti_on_idx = iti_on[i]
        cue_length_poke_rates = []
        iti_length_poke_rates = []
        for y in range(int(cue_length_sec)):
            pokes = 0
            iti_pokes = 0
            for x in range(cue_on_idx, cue_off_idx):
                if eventcode[x] == counted_behavior and (timecode[cue_on_idx] + y) <= timecode[x] < (
                        timecode[cue_on_idx] + y + 1):
                    pokes += 1
                else:
                    pokes += 0
            cue_length_poke_rates += [pokes]
            for t in range(iti_on_idx, cue_on_idx):
                if eventcode[t] == counted_behavior and (timecode[cue_on_idx] - (cue_length_sec - y)) \
                        <= timecode[t] < (timecode[cue_on_idx] - (cue_length_sec - (y + 1))):
                    iti_pokes += 1
                else:
                    iti_pokes += 0
            iti_length_poke_rates += [iti_pokes]
        all_cue_length_poke_rates = [cue_length_poke_rates[i] + all_cue_length_poke_rates[i] for i in
                                     range(len(all_cue_length_poke_rates))]
        all_iti_length_poke_rates = [iti_length_poke_rates[i] + all_iti_length_poke_rates[i] for i in
                                     range(len(all_iti_length_poke_rates))]

    all_cue_length_poke_rates = [all_cue_length_poke_rates[i] / len(cue_on) for i in
                                 range(len(all_cue_length_poke_rates))]
    all_iti_length_poke_rates = [all_iti_length_poke_rates[i] / len(cue_on) for i in
                                 range(len(all_iti_length_poke_rates))]
    subtracted_poke_rates = [all_cue_length_poke_rates[i] - all_iti_length_poke_rates[i] for i in
                             range(len(all_cue_length_poke_rates))]

    return all_cue_length_poke_rates, all_iti_length_poke_rates, subtracted_poke_rates


def duration_across_cue_iti(timecode, eventcode, code_on, code_off, counted_behavior_on, counted_behavior_off):
    """
    :param timecode: list of times (in seconds) when events occurred
    :param eventcode: list of events that happened in a session
    :param code_on: event name for lever presentation
    :param code_off: event name for lever press
    :param code_off: event name for lever press
    :return: 3 lists of cue, iti, and the subtracted responding across seconds
    """
    cue_on = get_events_indices(eventcode, [code_on])
    cue_off = get_events_indices(eventcode, [code_off])
    poke_on = get_events_indices(eventcode, [counted_behavior_on])
    poke_off = get_events_indices(eventcode, [counted_behavior_off])
    if len(cue_on) != len(cue_off):
        cue_off += get_events_indices(eventcode, ['EndSession'])
    cue_length_sec = int(timecode[cue_off[8]] - timecode[cue_on[8]])
    all_cue_length_poke_dur = [0] * int(cue_length_sec)
    all_iti_length_poke_dur = [0] * int(cue_length_sec)

    for i in range(len(cue_on)):
        cue_on_idx = cue_on[i]
        cue_off_idx = cue_off[i]
        cue_length_poke_dur = []
        iti_length_poke_dur = []
        for y in range(int(cue_length_sec)):
            poke_dur = 0
            iti_poke_dur = 0
            for c in range(len(poke_off)):
                # pokes that span whole seconds
                if timecode[poke_on[c]] < (timecode[cue_on_idx] + y) and timecode[poke_off[c]] > \
                        (timecode[cue_on_idx] + y + 1):
                    poke_dur += 1
                    break
                # pokes contained within a second
                elif (timecode[cue_on_idx] + y) <= timecode[poke_on[c]] < timecode[poke_off[c]] \
                        < (timecode[cue_on_idx] + y + 1):
                    poke_dur += timecode[poke_off[c]] - timecode[poke_on[c]]
                # pokes that start in a second of a cue
                elif (timecode[cue_on_idx] + y) <= timecode[poke_on[c]] < (timecode[cue_on_idx] + y + 1) \
                        < timecode[poke_off[c]]:
                    poke_dur += ((timecode[cue_on_idx] + y + 1) - timecode[poke_on[c]])
                # pokes that end in a second of a cue
                elif timecode[poke_on[c]] < (timecode[cue_on_idx] + y) <= timecode[poke_off[c]] \
                        < (timecode[cue_on_idx] + y + 1):
                    poke_dur += (timecode[poke_off[c]] - (timecode[cue_on_idx] + y))
                # pokes not occurring in the cue
                else:
                    poke_dur += 0
            cue_length_poke_dur += [round(poke_dur, 3)]
            for d in range(len(poke_off)):
                # pokes that span whole seconds
                if timecode[poke_on[d]] < (timecode[cue_on_idx] - (cue_length_sec - y)) and timecode[poke_off[d]] \
                        > (timecode[cue_on_idx] - (cue_length_sec - (y + 1))):
                    iti_poke_dur += 1
                    break
                # pokes contained within a second
                elif (timecode[cue_on_idx] - (cue_length_sec - y)) <= timecode[poke_on[d]] < timecode[poke_off[d]] \
                        < (timecode[cue_on_idx] - (cue_length_sec - (y + 1))):
                    iti_poke_dur += (timecode[poke_off[d]] - timecode[poke_on[d]])
                # pokes that start in a second of an ITI
                elif (timecode[cue_on_idx] - (cue_length_sec - y)) <= timecode[poke_on[d]] \
                        < (timecode[cue_on_idx] - (cue_length_sec - (y + 1))) < timecode[poke_off[d]]:
                    iti_poke_dur += ((timecode[cue_on_idx] - (cue_length_sec - (y + 1))) - timecode[poke_on[d]])
                # pokes that end in a second of an ITI
                elif timecode[poke_on[d]] < (timecode[cue_on_idx] - (cue_length_sec - y)) <= timecode[poke_off[d]] \
                        < (timecode[cue_on_idx] - (cue_length_sec - (y + 1))):
                    iti_poke_dur += (timecode[poke_off[d]] - (timecode[cue_on_idx] - (cue_length_sec - y)))
                # pokes not occurring in the ITI
                else:
                    iti_poke_dur += 0
            iti_length_poke_dur += [round(iti_poke_dur, 3)]
        all_cue_length_poke_dur = [cue_length_poke_dur[i] + all_cue_length_poke_dur[i] for i in
                                   range(len(all_cue_length_poke_dur))]
        all_iti_length_poke_dur = [iti_length_poke_dur[i] + all_iti_length_poke_dur[i] for i in
                                   range(len(all_iti_length_poke_dur))]

    all_cue_length_poke_dur = [all_cue_length_poke_dur[i] / len(cue_on) for i in
                               range(len(all_iti_length_poke_dur))]
    all_iti_length_poke_dur = [all_iti_length_poke_dur[i] / len(cue_on) for i in
                               range(len(all_iti_length_poke_dur))]
    subtracted_poke_dur = [all_cue_length_poke_dur[i] - all_iti_length_poke_dur[i] for i in
                           range(len(all_cue_length_poke_dur))]

    return all_cue_length_poke_dur, all_iti_length_poke_dur, subtracted_poke_dur

def duration_across_trace_iti(timecode, eventcode, code_on, code_off, counted_behavior_on, counted_behavior_off, cue_time):
    """
    :param timecode: list of times (in seconds) when events occurred
    :param eventcode: list of events that happened in a session
    :param code_on: event name for lever presentation
    :param code_off: event name for lever press
    :param code_off: event name for lever press
    :return: 3 lists of cue, iti, and the subtracted responding across seconds
    """
    cue_on = get_events_indices(eventcode, [code_on])
    cue_off = get_events_indices(eventcode, [code_off])
    poke_on = get_events_indices(eventcode, [counted_behavior_on])
    poke_off = get_events_indices(eventcode, [counted_behavior_off])
    if len(cue_on) != len(cue_off):
        cue_off += get_events_indices(eventcode, ['EndSession'])
    cue_length_sec = int(timecode[cue_off[6]] - timecode[cue_on[6]])
    all_cue_length_poke_dur = [0] * int(cue_length_sec)
    all_iti_length_poke_dur = [0] * int(cue_length_sec)

    for i in range(len(cue_on)):
        cue_on_idx = cue_on[i]
        cue_off_idx = cue_off[i]
        cue_length_poke_dur = []
        iti_length_poke_dur = []
        for y in range(int(cue_length_sec)):
            poke_dur = 0
            iti_poke_dur = 0
            for c in range(len(poke_off)):
                # pokes that span whole seconds
                if timecode[poke_on[c]] < (timecode[cue_on_idx] + y) and timecode[poke_off[c]] > \
                        (timecode[cue_on_idx] + y + 1):
                    poke_dur += 1
                    break
                # pokes contained within a second
                elif (timecode[cue_on_idx] + y) <= timecode[poke_on[c]] < timecode[poke_off[c]] \
                        < (timecode[cue_on_idx] + y + 1):
                    poke_dur += timecode[poke_off[c]] - timecode[poke_on[c]]
                # pokes that start in a second of a cue
                elif (timecode[cue_on_idx] + y) <= timecode[poke_on[c]] < (timecode[cue_on_idx] + y + 1) \
                        < timecode[poke_off[c]]:
                    poke_dur += ((timecode[cue_on_idx] + y + 1) - timecode[poke_on[c]])
                # pokes that end in a second of a cue
                elif timecode[poke_on[c]] < (timecode[cue_on_idx] + y) <= timecode[poke_off[c]] \
                        < (timecode[cue_on_idx] + y + 1):
                    poke_dur += (timecode[poke_off[c]] - (timecode[cue_on_idx] + y))
                # pokes not occurring in the cue
                else:
                    poke_dur += 0
            cue_length_poke_dur += [round(poke_dur, 3)]
            for d in range(len(poke_off)):
                # pokes that span whole seconds
                if timecode[poke_on[d]] < (timecode[cue_on_idx] - (cue_length_sec + cue_time - y)) and timecode[poke_off[d]] \
                        > (timecode[cue_on_idx] - (cue_length_sec + cue_time - (y + 1))):
                    iti_poke_dur += 1
                    break
                # pokes contained within a second
                elif (timecode[cue_on_idx] - (cue_length_sec + cue_time - y)) <= timecode[poke_on[d]] < timecode[poke_off[d]] \
                        < (timecode[cue_on_idx] - (cue_length_sec + cue_time - (y + 1))):
                    iti_poke_dur += (timecode[poke_off[d]] - timecode[poke_on[d]])
                # pokes that start in a second of an ITI
                elif (timecode[cue_on_idx] - (cue_length_sec + cue_time - y)) <= timecode[poke_on[d]] \
                        < (timecode[cue_on_idx] - (cue_length_sec + cue_time - (y + 1))) < timecode[poke_off[d]]:
                    iti_poke_dur += ((timecode[cue_on_idx] - (cue_length_sec + cue_time - (y + 1))) - timecode[poke_on[d]])
                # pokes that end in a second of an ITI
                elif timecode[poke_on[d]] < (timecode[cue_on_idx] - (cue_length_sec + cue_time - y)) <= timecode[poke_off[d]] \
                        < (timecode[cue_on_idx] - (cue_length_sec + cue_time - (y + 1))):
                    iti_poke_dur += (timecode[poke_off[d]] - (timecode[cue_on_idx] - (cue_length_sec + cue_time - y)))
                # pokes not occurring in the ITI
                else:
                    iti_poke_dur += 0
            iti_length_poke_dur += [round(iti_poke_dur, 3)]
        all_cue_length_poke_dur = [cue_length_poke_dur[i] + all_cue_length_poke_dur[i] for i in
                                   range(len(all_cue_length_poke_dur))]
        all_iti_length_poke_dur = [iti_length_poke_dur[i] + all_iti_length_poke_dur[i] for i in
                                   range(len(all_iti_length_poke_dur))]

    all_cue_length_poke_dur = [all_cue_length_poke_dur[i] / len(cue_on) for i in
                               range(len(all_iti_length_poke_dur))]
    all_iti_length_poke_dur = [all_iti_length_poke_dur[i] / len(cue_on) for i in
                               range(len(all_iti_length_poke_dur))]
    subtracted_poke_dur = [all_cue_length_poke_dur[i] - all_iti_length_poke_dur[i] for i in
                           range(len(all_cue_length_poke_dur))]

    return all_cue_length_poke_dur, all_iti_length_poke_dur, subtracted_poke_dur


def closest(lst, K):
    return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - K))]

