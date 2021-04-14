#!/usr/bin/env python3

import LickometerAnalysisKit
import glob
from sys import argv
from os import path

##### PREAMBLE #####

# Handling of user arguments to avoid errors based on ordering
user_args = argv

# Remove script name from list of arguments. 
user_args.pop(0)

# Check for arguments pertaining to preferences for graphing
if 'use_defaults' in user_args:
	drop_first_block = True
	norm_by_water = True
	grouping_criteria = 'CONCENTRATION'
	user_args.remove('use_defaults')
else:
	if 'drop_first_block' in user_args:
		drop_first_block = True
		user_args.remove('drop_first_block')
	if 'norm_by_water' in user_args:
		norm_by_water = True
		user_args.remove('drop_first_block')

	if 'group_by_TUBE' in user_args:
		grouping_criteria = 'TUBE'
		user_args.remove('group_by_TUBE')
	else:
		grouping_criteria = 'CONCENTRATION'

# With all other possible arguments removed, check for a path to files
try:
	path_to_files = user_args[0]
except IndexError:
	print('User did not provide path to files.')
	path_to_files = input('Please enter it now. (Press enter to prompt GUI).    ')

if path_to_files == '':
	#TODO: Add Tk interface to select directory path.


# Pull the name of the directory containing files to use as 
base_folder_name = os.path.basename(path_to_files)

target_file_search_term = os.path.join(path_to_files, '*.txt')
files = glob.glob(target_file_search_term)


##### EXECUTION #####


# Read in files
df_dict, ili_dict, animals = LickometerAnalysisKit.read_raw_files(files)
# Create DataFrames
total_df, total_df_by_animals = LickometerAnalysisKit.gen_summary_dataframe(df_dict, animals, base_folder_name,
																		    grouping_criteria=grouping_criteria)

# Make graphs.

LickometerAnalysisKit.graph_cumulative_licks(total_df_by_animals, animals, base_folder_name)

LickometerAnalysisKit.individual_graph_by_group(total_df, animals, base_folder_name, 
												grouping_criteria=grouping_criteria, 
												drop_first_block=drop_first_block, 
												normalize_by_water_consumption=norm_by_water)

LickometerAnalysisKit.summarize_licking_curve(total_df, base_folder_name, 
												grouping_criteria=grouping_criteria, 
												drop_first_block=drop_first_block, 
												normalize_by_water_consumption=norm_by_water)
