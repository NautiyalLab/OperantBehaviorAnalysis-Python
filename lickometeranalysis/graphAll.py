#!/usr/bin/env python3

import LickometerAnalysisKit
import glob
from sys import argv
from os import path
from tkinter import filedialog
from tkinter import *  # noqa

def getFolderPath():
    folder_selected = filedialog.askdirectory()
    folderPath.set(folder_selected)

'''
This script will perform basic processing of .ms8.txt files produced by the MED-Associates
legacy-Davis Rig Lickometer. 

USAGE:

graphAll.py [path_to_files, use_first_block, no_normalization, group_by_TUBE]
reads in raw files and executes gen_summary_dataframe, graph_cumulative_licks, individual_graph_by_group, and summarize_licking_curve
'''



##### PREAMBLE #####

# Safely remove script name from list of arguments . 
user_args = argv.copy()
user_args.pop(0)


# If the user has provided arguments, process them.
if len(user_args) != 0:
    # Check for arguments pertaining to preferences for graphing
    if 'use_first_block' in user_args:
        drop_first_block = False
        user_args.remove('use_first_block')
        print('Including first presentation block in averages.')
    else:
        drop_first_block = True
        print('Excluding first presentation block from averages.')
    if 'no_normalization' in user_args:
        norm_by_water = False
        user_args.remove('no_normalization')
        print('Using raw lick counts for averages.')
    else:
        norm_by_water = True
        print('Normalizing lick counts to water consumption.')
    if 'group_by_TUBE' in user_args:
        grouping_criteria = 'TUBE'
        user_args.remove('group_by_TUBE')
    else:
        grouping_criteria = 'CONCENTRATION'
    print(f'Grouping by {grouping_criteria}')

    # With all other possible arguments removed, check for a path to files
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
# If no user input was provided, prompt for all variables. 
else:
    print('Please select a directory containing files for analysis.')
    root = Tk()  # noqa
    # root.withdraw()
    folderPath = StringVar()
    a = Label(root ,text="Enter name")
    a.grid(row=0,column = 0)
    E = Entry(root,textvariable=folderPath)
    E.grid(row=0,column=1)
    btnFind = Button(root, text="Browse Folder",command=getFolderPath)
    btnFind.grid(row=0,column=2)

    norm_label = Label(root, text='Normalize licking by water intake?')
    norm_label.grid(row=1, column=0)
    norm_true = IntVar()
    Checkbutton(root, text='Check for "Yes"', variable=norm_true).grid(row=1, column=1, sticky=W)

    drop_label = Label(root, text='Drop first block of presentations from analysis?')
    drop_label.grid(row=2, column=0)
    drop_true = IntVar()
    Checkbutton(root, text='Check for "Yes"', variable=drop_true).grid(row=2, column=1, sticky=W)

    group_label = Label(root, text='Grouping criteria:')
    group_label.grid(row=3, column=0)
    tube_group = IntVar()
    conc_group = IntVar()
    Checkbutton(root, text='Group by CONCENTRATION', variable=conc_group).grid(row=3, column=1, sticky=W)
    Checkbutton(root, text='Group by TUBE', variable=tube_group).grid(row=3, column=2, sticky=W)

    Button(root, text='Done', command=root.quit).grid(row=4, column=1, sticky=W, pady=3)

    root.eval('tk::PlaceWindow . center')

    mainloop()
    root.destroy()

    path_to_files = folderPath.get()

    norm_by_water = bool(norm_true.get())
    drop_first_block = bool(drop_true.get())
    if conc_group.get():
        grouping_criteria = 'CONCENTRATION'
    else:
        if not tube_group.get():
            print('No grouping criteria selected. Defaulting to TUBE.')
        grouping_criteria = 'TUBE'




# Pull the name of the directory containing files to use as .png name. 

if path_to_files[-1] == path.sep:
    # If the last character in the path is a separator, remove that character.
        # Otherwise path.basename(path_to_folder) will return nothing.
    path_to_files = path_to_files[:-1]

base_folder_name = path.basename(path_to_files)
print(f'Saving figures with name: {base_folder_name}')

target_file_search_term = path.join(path_to_files, '*.txt')
files = glob.glob(target_file_search_term)

if len(files) == 0:
    print(f'{target_file_search_term} yielded no files. Try again.')
    raise RuntimeError


##### EXECUTION #####


# Read in files
df_dict, ili_dict, animals = LickometerAnalysisKit.read_raw_files(files)
# Create DataFrames
total_df, total_df_by_animals = LickometerAnalysisKit.gen_summary_dataframe(df_dict, animals, base_folder_name,
                                                                            drop_first_block=drop_first_block,
                                                                            group_by_concentration=bool(grouping_criteria=='CONCENTRATION'))

# Make graphs.

LickometerAnalysisKit.graph_cumulative_licks(total_df_by_animals, animals, base_folder_name)

LickometerAnalysisKit.individual_graph_by_group(total_df, base_folder_name, 
                                                grouping_criteria=grouping_criteria, 
                                                drop_first_block=drop_first_block, 
                                                normalize_by_water_consumption=norm_by_water)

LickometerAnalysisKit.summarize_licking_curve(total_df, base_folder_name, 
                                                grouping_criteria=grouping_criteria, 
                                                drop_first_block=drop_first_block, 
                                                normalize_by_water_consumption=norm_by_water)
