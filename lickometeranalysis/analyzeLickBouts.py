#!/usr/bin/env python3

import LickometerAnalysisKit
import pandas as pd
import glob
import natsort
from sys import argv
from os import path
from tkinter import filedialog
from tkinter import *  # noqa


'''
This script will perform lick bout analysis of data pulled from raw .ms8.txt files. 

USAGE: 

analyzeLickBouts.py [path_to_files, -t THRESHOLD_IN_MILLISECONDS, -s CSV_CONTAINING_EXPERIMENTAL_GROUP_INFO]

'''


##### PREAMBLE #####

# Safely remove script name from list of arguments . 
user_args = argv.copy()
user_args.pop(0)


# If the user has provided path to files use that.
if len(user_args) != 0:
    if '-t' in user_args:
        # If user provides flag indicated threshold, find index of threshold. 
        thresh_idx = user_args.index('-t')+1 # It should immediately follow flag.
        burst_threshold = user_args[thresh_idx]
  
        # Remove both from list of args.
        user_args.pop(thresh_idx)
        user_args.remove('-t')
    else:
        burst_threshold = 1000
    if '-s' in user_args:
        # If user indicates that a csv containing subject data has been passed, read it in. 
        subj_idx = user_args.index('-s')+1
        group_df = pd.read_csv(user_args[subj_idx], index_col=0)

        user_args.pop(subj_idx)
        user_args.remove('-s')
    else:
    	group_df = None


    # With all other possible, valid arguments removed, check for a path to files
    try:
        path_to_files = user_args[0]
    except IndexError:
        print('User did not provide path to files.')
        path_to_files = input('Please enter it now. (Press enter to prompt GUI).    ')

    # If no path provided, use a GUI prompt.
    if path_to_files == '':
        root = Tk()  # noqa
        root.withdraw()
        path_to_files = filedialog.askdirectory()

# If no user input was provided, prompt for it. 
else:
    print('Please select a directory containing files for analysis.')
    root = Tk()  # noqa
    root.withdraw()
    path_to_files = filedialog.askdirectory()


# Pull the name of the directory containing files to use as .png name. 

if path_to_files[-1] == path.sep:
    # If the last character in the path is a separator, remove that character.
        # Otherwise path.basename(path_to_folder) will return nothing.
    path_to_files = path_to_files[:-1]

base_folder_name = path.basename(path_to_files)

target_file_search_term = path.join(path_to_files, '*.txt')
files = glob.glob(target_file_search_term)

if len(files) == 0:
    print(f'{target_file_search_term} yielded no files. Try again.')
    raise RuntimeError



# Read in files
df_dict, ili_dict, animals = LickometerAnalysisKit.read_raw_files(files)

# Use an arbitrary animal to pull concentrations. 
concentrations = list(set(df_dict[animals[0]].CONCENTRATION))
concentrations = natsort.natsorted(concentrations)

# summarize_lick_bouts automatically saves ili_df. 
ili_df = LickometerAnalysisKit.summarize_lick_bouts(ili_dict, df_dict, animals, 
                              concentrations, base_folder_name,
                              burst_threshold = burst_threshold,
                              subject_grouping_data = group_df)