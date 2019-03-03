import statistics
from eventcodes import eventcodes_dictionary
__all__ = ["load_file", "extract_info_from_file", "reward_retrieval", "cue_iti_responding", "lever_pressing", "lever_press_latency"]


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

    timecode = []
    eventcode = []
    first_timecode = (float(time_event_codes[0][:-6]) / time_conversion)

    for num in time_event_codes:
        if num == time_event_codes[0]:
            timecode += [0.0]
        else:
            timecode += [round((float(num[:-6]) / time_conversion) - first_timecode, 2)]
        eventcode += [eventcodes_dictionary[int(num[-6:-2])]]

    return timecode, eventcode


def reward_retrieval(timecode, eventcode):
    """

    :param timecode: list of time codes from operant conditioning file
    :param eventcode: list of event codes from operant conditioning file
    :return: number of reinforcers (dippers) presented, number retrieved, and latency to retrieve as floats
    """
    dip_on = [i for i, event in enumerate(eventcode) if event == 'DipOn']
    dip_off = [i for i, event in enumerate(eventcode) if event == 'DipOff']
    poke_on = [i for i, event in enumerate(eventcode) if event == 'PokeOn1']
    poke_off = [i for i, event in enumerate(eventcode) if event == 'PokeOff1']
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
    return len(dip_on), dips_retrieved, round(statistics.mean(latency_dip_retrieval), 3)


def cue_iti_responding(timecode, eventcode, code_on, code_off):
    """

    :param timecode: list of time codes from operant conditioning file
    :param eventcode: list of event codes from operant conditioning file
    :param code_on: event code for the beginning of a cue
    :param code_off: event code for the end of a cue
    :return: mean rpm of head pokes during cue and mean rpm of head pokes during equivalent ITI preceding cue
    """
    cue_on = [i for i, event in enumerate(eventcode) if event == code_on]
    cue_off = [i for i, event in enumerate(eventcode) if event == code_off]
    iti_on = [i for i, event in enumerate(eventcode) if event == code_off or event == 'StartSession']
    all_poke_rpm = []
    all_poke_iti_rpm = []

    for i in range(len(cue_on)):
        cue_on_idx = cue_on[i]
        cue_off_idx = cue_off[i]
        iti_on_idx = iti_on[i]
        cue_length_sec = (timecode[cue_off_idx] - timecode[cue_on_idx])
        poke_rpm = ((eventcode[cue_on_idx:cue_off_idx].count('PokeOn1')) / (cue_length_sec / 60))
        all_poke_rpm += [poke_rpm]
        iti_poke = 0
        for x in range(iti_on_idx, cue_on_idx):
            if eventcode[x] == 'PokeOn1' and timecode[x] >= (timecode[cue_on_idx] - cue_length_sec):
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
    if bool(lever2):
        lever2_presses = eventcode.count(lever2)
    else:
        lever2_presses = 0
    total_lever_presses = lever1_presses + lever2_presses

    return lever1_presses, lever2_presses, total_lever_presses


def lever_press_latency(timecode, eventcode, leveron, leverpress):
    """

    :param timecode: list of times (in seconds) when events occurred
    :param eventcode: list of events that happened in a session
    :param leveron: event name for lever presentation
    :param leverpress: event name for lever press
    :return: the mean latency to press the lever in seconds
    """
    leveron = [i for i, event in enumerate(eventcode) if event == leveron or event == 'EndSession']
    latencytopress = []
    for i in range(len(leveron)-1):
        leveronidx = leveron[i]
        if leverpress in eventcode[leveronidx:leveron[i + 1]]:
            leverpressidx = eventcode[leveronidx:leveron[i + 1]].index(leverpress)
            latencytopress += [round(timecode[leveronidx + leverpressidx] - timecode[leveronidx], 2)]
            break
        else:
            None
    if len(latencytopress) > 0:
        return round(statistics.mean(latencytopress), 3)
    else:
        return "No presses"
