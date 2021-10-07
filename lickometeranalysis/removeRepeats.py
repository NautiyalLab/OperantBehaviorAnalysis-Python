#!/usr/bin/env python3

# The MED-PC Lickometer program apparently simply copies and overwrites the most recent .ms8.txt file when creating a new one
# in the same session. This means that if one animal completes 30 trials, for example, and the next completes only 17, the 13 trials
# from the first animal will still appear in the data file for the second animal. The purpose of this script will be to take as input
# a directory containing data-files from a single day and create new files in which any artifactual repeats are removed. 

import LickometerAnalysisKit
import glob
import pandas as pd
import numpy as np
from sys import argv
from os import path


path_to_files = argv[1]

target_file_search_term = path.join(path_to_files, '*.ms8.txt')
files = glob.glob(target_file_search_term)

df_dict, ili_dict, animals = LickometerAnalysisKit.read_raw_files(files, drop_empty_trials=False)
subjects = list(df_dict.keys())



start_times_dict = {}
for file in files:
    with open(file, 'r') as the_file:
        raw_data = the_file.read()

    lines = raw_data.splitlines()
    start_time = lines[4].split(',')[1].strip()
    animal_id = lines[5].split(',')[1].strip()
    start_times_dict[animal_id] = start_time

subjects = sorted(subjects, key=lambda subj: start_times_dict[subj])

for i in range(1, len(subjects)):
    # Compare each file to the one before it.
    print(f'{subjects[i]} vs. {subjects[i-1]}')
    rows_to_keep = []
    for idx in df_dict[subjects[i]].index:
        rows_to_keep.append(not df_dict[subjects[i]].loc[idx, ['LICKS', 'Latency']].equals(df_dict[subjects[i-1]].loc[idx, ['LICKS', 'Latency']]))

    total_presentations = len(rows_to_keep)

    old_file_name = glob.glob(f'*{subjects[i]}.ms8.txt')[0]
    date = old_file_name[:4]
    with open(old_file_name, 'r') as the_file:
        old_file = the_file.read()

    old_file_lines = old_file.splitlines()
    # Note that the line index is 0-based while the line numbers in the actual files are of course 1-based.
    # The INDEX for this list is used throughout the section below, which can lead to an apparent mismatch if you try to compare it directly to the
    # original data files.  

    new_file_name = f'{date}{subjects[i]}_ReplicatesRemoved.ms8.txt'
    path_to_new_file = path.join(path_to_files, new_file_name)

    print(f'Writing {new_file_name}')

    with open(path_to_new_file, 'w') as the_file:
        # Header information + Summary table header are rows 0-10
        for l in range(11):
            the_file.write(f'{old_file_lines[l]}\n')

        # Summary Table Rows: 11 through [Total # Presentations + 10]
        for data_table_row, l in enumerate(range(11, 11+total_presentations)):
            if rows_to_keep[data_table_row]:
                the_file.write(f'{old_file_lines[l]}\n')

        the_file.write('\n')

        # ILI rows are located at [11 + Total Presentations + Trial #]
        for trial_num, write_toggle in enumerate(rows_to_keep, start=1):
            old_file_line_num = trial_num + total_presentations + 11
            if write_toggle:
                the_file.write(f'{old_file_lines[old_file_line_num]}\n')

