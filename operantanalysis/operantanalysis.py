import statistics
import os
import glob
from tkinter import filedialog
from tkinter import *  # noqa
import pandas as pd
from .eventcodes import eventcodes_dictionary

__all__ = ["loop_over_days", "load_file", "extract_info_from_file", "get_events_indices", "reward_retrieval", "cue_iti_responding",
           "lever_pressing", "lever_press_latency", "total_head_pokes", "num_successful_go_nogo_trials", "count_go_nogo_trials",
           "bin_by_time"]


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
        next_group = remaining.split(':')
        fields_dictionary[next_group[0]] = next_group[1]

    return fields_dictionary


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
    :return: mean rpm of head pokes during cue and mean rpm of head pokes during equivalent ITI preceding cue
    """
    cue_on = get_events_indices(eventcode, [code_on])
    cue_off = get_events_indices(eventcode, [code_off])
    iti_on = get_events_indices(eventcode, [code_off, 'StartSession'])
    all_poke_rpm = []
    all_poke_iti_rpm = []

    for i in range(len(cue_on)):
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


def lever_pressing(eventcode, lever1, lever2=False):
    """
    :param eventcode: list of event codes from operant conditioning file
    :param lever1: eventcode for lever pressing
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
    :param leveron: event name for lever presentation
    :param leverpress: event name for lever press
    :return: the mean latency to press the lever in seconds
    """
    lever_on = get_events_indices(eventcode, [lever_on, 'EndSession'])
    press_latency = []

    for i in range(len(lever_on) - 1):
        lever_on_idx = lever_on[i]
        if lever_press in eventcode[lever_on_idx:lever_on[i + 1]]:
            lever_press_idx = eventcode[lever_on_idx:lever_on[i + 1]].index(lever_press)
            press_latency += [round(timecode[lever_on_idx + lever_press_idx] - timecode[lever_on_idx], 2)]
            break
        else:
            pass
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
