#!/usr/bin/env python3

# This file will contain function calls used in analyzing Lickometer data. 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
font = {'family' : 'monospace',
        'weight' : 'bold',
        'size'   : 11}
rc('font', **font)
rc('lines', lw=2)
rc('figure', figsize=(16,12))
import natsort

# These keys are the default column names from the .ms8.txt file. 
# This dictionary is used to retype DataFrames produced in read_raw_files and gen_summary_dataframe 
retype_dict = {'PRESENTATION': 'int',
 'TUBE': 'category',
 'CONCENTRATION': 'category',
 'SOLUTION': 'category',
 'IPI': 'float',
 'LTL': 'float',
 'MAX LICKS': 'float',
 'LICKS': 'int',
 'Latency': 'float'}


##### INPUT FUNCTIONS ##### 

def read_raw_files(files, drop_empty_trials=True):
    '''
    :PARAM files: A list of paths to raw .txt files for analysis.
    :RETURN (df_dictionary,        : A dictionary containing individual DataFrames for each animal
             interlick_intervals   : A dictionary containing interlick interval data for each animal. 
             animals)              : A list of animals. 
    '''
    
    df_dictionary = {}

    # Because of the variablility in number of licks, use a dictionary to store
    # the interlick intervals for each presentation for each animal. 
    interlick_intervals = {}


    for data_file in files:
        with open(data_file, 'r') as f:
            raw_data = f.read()

        lines = raw_data.splitlines()
        # Line 5 is the subject ID. The line format is 'Animal ID, A252', e.g.
        animal_id = lines[5].split(',')[1].strip()


        # In the event that the number of trials differs, calculate the number of presentations dynamically. 
        # The first line of the summary table is at line 11. There will always be a blank line at the end of this table. 
        # find the location of that blank line, and then get the presentation number of the preceding (i.e. final) presentation. 

        #Occasionally the the summary table is a line higher than expected, putting the first row of data at 10 and the column headers
        # at 9. 
        # We'll add a stupid noodge factor that is determined by whether or not "PRESENTATION" is the first value of line 10. 

        # TODO: Come up with a more dynamic way of determining table start. 

        if lines[10].split(',')[0] != 'PRESENTATION':
            noodge = 1
        else:
            noodge = 0

        counter = 11 - noodge
        line_value = lines[counter]
        while line_value != '':
            counter+=1
            line_value = lines[counter]
        last_summary_table_line = counter - 1
        try:
            presentations = int(lines[last_summary_table_line].split(',')[0].strip())
        # If the animal did not make any licks, then the table will be empty and the value found
        # at the specified indices will be PRESENTATION. Attempting to convert this to int will throw a ValueError.
        except ValueError:
            # If the animal did not lick, skip the rest of the loop. 
            continue

        # Column Names are always in line 10. 
        cols = []
        for col in lines[10-noodge].split(','):
            cols.append(col.strip())

        df_dictionary[animal_id] = pd.DataFrame(index=range(1, presentations+1), columns = cols)
        interlick_intervals[animal_id] = {}

        # Data start on line 11 and run until 11+the number of presentations.
        for idx, line in enumerate(range((11-noodge),(11-noodge)+presentations), start=1):

            ###### POPULATING df_dictionary ######
            
            # Read data and simultaneously remove any extra spaces around the data.   
            sanitized_data = np.array([x.strip() for x in lines[line].split(',')])
            df_dictionary[animal_id].loc[idx] = sanitized_data
        
            # Sanitizes concentration input. 
            try:
                if df_dictionary[animal_id].loc[idx, 'CONCENTRATION'][0] == '.':
                    # If the concentration is fractional, and the leading character is a decimal point, add a 0 in front of it. 
                    df_dictionary[animal_id].loc[idx, 'CONCENTRATION'] = f"0{df_dictionary[animal_id].loc[idx, 'CONCENTRATION']}"
            except IndexError:
                    df_dictionary[animal_id].loc[idx, 'CONCENTRATION'] = np.nan

            ###### POPULATING interlick_intervals ######

            # The interlick intervals for a given presentation are contained in a line presentations+1 below the row
            # containing summary information. 
            ili_line = np.array(lines[line+presentations+1].split(','), dtype='int')
            presentation_number = ili_line[0]

            # These should always match. 
            if presentation_number == idx:
                # If they do match, you can remove the presentation number and move along.
                ilis = np.delete(ili_line, 0)
            else:
                # If they don't, it's the wrong data. 
                raise ValueError

            # It is also the case that because there are INTER-lick intervals, if an animal executed only a single lick, 
                # there will be no data here. 
            # To facilitate the use these data as timestamps later on, 
                # a 0 is inserted at the beginning of each array to reflect that.

            if int(df_dictionary[animal_id].loc[idx, 'LICKS']) > 0:
                # Do this only if the animal licked during this presentation.
                ilis = np.insert(ilis, 0, 0)

            # Save the final list to the dictionary. 
            interlick_intervals[animal_id][presentation_number] = ilis


        df_dictionary[animal_id] = df_dictionary[animal_id].astype(retype_dict)

        # Remove trials without licking
        if drop_empty_trials:
            empty_trials = df_dictionary[animal_id][df_dictionary[animal_id].LICKS==0].index
            df_dictionary[animal_id].drop(empty_trials, inplace=True)

    # Creating a variable here is done solely for readability.
    animals = sorted(list(df_dictionary.keys()))

    return df_dictionary, interlick_intervals, animals

def gen_summary_dataframe(animal_dataframes, animals, experiment_label, drop_first_block=True, group_by_concentration=True):
    '''
    :PARAM animal_dataframes: A dictionary containing individual DataFrames for each animal. Generated by read_raw_files.
    :PARAM animals: a list of animal ids. 
    :PARAM grouping_criteria: A boolean that determines whether data are grouped by concentration. Defaults to True.

    :RETURN total_dataframe: A long-form dataframe summarizing the data for all animals. Each row is a presentation for a single animal. 
    :RETURN total_dataframe_by_animal: A DataFrame containing all the information of the above, but grouped using a multi-index
                                       to allow easy access to individual animal data. 
    '''

    #Determine the size of the dataframe dynamically. 
    total_presentations = sum(animal_dataframes[animal].shape[0] for animal in animals)
    
    # The columns in all dataframes should be the same, so just grab an arbitrary one. 
    cols = animal_dataframes[animals[0]].columns
    total_dataframe = pd.DataFrame(index=range(1, total_presentations+1), columns=list(cols)+['AnimalID', 'Water_Normalized_Licking'])


    idx_start = 1
    for c, animal in enumerate(animals): 
        
        # Determine the target indices to which to write: 
        len_index = animal_dataframes[animal].shape[0]
        if len_index == 0:
            continue
        new_index = pd.Index(range(idx_start, idx_start+len_index))
        # ...and increment idx_start for the next loop.
        idx_start = new_index[-1]+1
        # Reset the index of the individual animal's DataFrame as well because of the way 
            # that pandas deals with writing from one DataFrame to another (i.e. the indices of the source DataFrame 
            # override the indices of the target, meaning you want them to match.)
        animal_dataframes[animal].set_index(new_index, inplace=True)
        
        # Write the data.
        try:
            total_dataframe.loc[new_index, cols] = animal_dataframes[animal].loc[new_index, cols]
        except KeyError:
            for col in cols:
                try:
                    total_dataframe.loc[new_index, col] = animal_dataframes[animal].loc[new_index, col]
                except KeyError:
                    print(f'{col} not found for {animal}. Storing as NaN.')
                    total_dataframe.loc[new_index, col] = np.nan

        total_dataframe.loc[new_index, 'AnimalID'] = animal

        # If grouping by concentrations, normalize licking by water consumption. 
        if group_by_concentration:
   
            # Use drop_first_block flag in calculating average licking during water. 
            if drop_first_block:
                min_presentation = 1
            else:
                min_presentation = 0
  
            avg_water_licking = animal_dataframes[animal].loc[(animal_dataframes[animal].SOLUTION=='Water')&
                                                              (animal_dataframes[animal].PRESENTATION>min_presentation),
                                                              'LICKS'].mean()
            # If an animal has not licked, avg_water_licking will be 0 and the calculation of Water_Normalized_Licking will throw
                # an error. 
            if avg_water_licking==0:
                avg_water_licking = 1                                                 
           
            total_dataframe.loc[new_index, 'Water_Normalized_Licking'] = total_dataframe.loc[new_index, 'LICKS'] / avg_water_licking

    # If grouping by TUBE, Water_Normalized_Licking is empty. 
    if not group_by_concentration:
        total_dataframe.drop('Water_Normalized_Licking', axis=1, inplace=True)
    else:
        total_dataframe.loc[:, 'Water_Normalized_Licking'] = total_dataframe.loc[:, 'Water_Normalized_Licking'].astype('float')


    total_dataframe = total_dataframe.astype(retype_dict)
    total_dataframe.to_csv(f'MasterDataFrame_{experiment_label}.csv')
    # Will create a multi-index of (AnimalID, Presentation #).
    # This will permit easy access to each animal's data. Because each presentation # only occurs
        # once per animal, neither sum() nor mean() will actually alter the data.  
    total_dataframe_by_animal = total_dataframe.groupby(['AnimalID', 'PRESENTATION']).mean()
    return total_dataframe, total_dataframe_by_animal


##### DATA PROCESSING FUNCTIONS ##### 

def summarize_lick_bouts(ili_data, animal_dataframes, animals, concentrations, experiment_label, burst_threshold = 1000, subject_grouping_data = None):
    '''
    :PARAM ili_data: a dictionary containing interlick intervals (produced by read_raw_files())
    :PARAM animal_dataframes: df_dictionary from read_raw_files. Used to determine presentations during which different solutions were given.
    :PARAM animals: a list of animal IDs. 
    :PARAM concentrations: a list of the concentrations presented during testing.
    :PARAM experiment_label: A string to use for labeling the comma separated value file. 
    :PARAM burst_threshold: tohe cutoff (in ms) for defining bursts. Defaults to 1000 ms based on literature (e.g. 10.1016/j.appet.2009.12.007)
    :PARAM subject_grouping_data: an optional dataframe (index = animal IDs, columns = independent variable labels)
                                  containing grouping data. 
    :RETURN lick_df: a pandas DataFrame containing data summarizing interlick interval data across subjects and concentrations. 
    '''

    ##SET UP DATAFRAME##

    column_labels = ['Total_Licks', 'Burst_Threshold', 'Burst_Number', 'Avg_BurstLength', 'AvgLicksInBurst']
    try:
        # If user has provided grouping data, include group labels. 
        column_labels.extend(subject_grouping_data.columns)
    except AttributeError: 
        pass


    # Create a multi-index if user provided more than a single concentration.
    if len(concentrations) == 1:
        lick_df_index = animals
    else:
        lick_df_index = pd.MultiIndex.from_product([concentrations, animals], names=['Concentration', 'SubjectID'])

    lick_df = pd.DataFrame(index = lick_df_index, columns = column_labels)


    ##CALCULATE METRICS##

    for concentration in concentrations:
        for animal in animals:
            # Pull the presentation numbers during which target concentration was presented. 
            presentations = animal_dataframes[animal][animal_dataframes[animal].CONCENTRATION==concentration].loc[:, 'PRESENTATION'].values

            total_licks = 0
            burst_count = 0
            burst_lengths = {'Time': [], 'Licks': []}
            for presentation in presentations:
                # Pull the raw data out for ease of processing. 
                ilis = np.array(ili_data[animal][presentation])

                # Count total licks
                total_licks+=ilis.size
                
                if len(ilis)<2:
                    # If there are fewer than two licks, there's no burst.
                    continue


                #Identify bursts
                    # licks in a burst will be 2 or more consecutive events separated by the threshold or less. 

                # Any number below threshold corresponds to a lick within a burst with the following caveats:
                    # The first lick is marked as "0". There is no guarantee that more licks follow, however. 
                    # The first lick in a bout will always be marked False because, definitionally, it must occur
                        # more than burst_threshold milliseconds after the last lick.
                ilis_under_thresh = ilis<=burst_threshold
                # To make the first bout consistent with all others, the first value is set to False based on logic above.
                ilis_under_thresh[0] = False

                # Identify burst edges. 
                transitions = np.diff(ilis_under_thresh.astype(int))
                #  1: Corresponds to False followed by True. Indicates 2nd lick in burst (see above)
                # -1: Corresponds to True followed by False. Indicates end of burst.
                #  0: Indicates False-False or True-True. Indicates no state change. 

                # The number of occurrences of -1 will be the number of bursts.  
                burst_count+=sum(transitions==1)
                
                # If no bursts are detected, skip. 
                if sum(transitions==1)<1:
                    continue

                # Gets the indices of all second licks. 

                second_lick_indices = np.nonzero(transitions==1)
                burst_idxs = []
                for idx in second_lick_indices[0]: # np.nonzero returns a tuple of arrays for each input dimension.                    
                    # The indices of transitions and ilis are offset by one because of np.diff.
                    # Therefore, the index of the second lick in a bout in "transitions" will be the same 
                        # as the index of the first lick in "ilis"
                    
                    # Start the list licks for the current burst with the first ili.
                    burst = [ilis[idx]]
                    
                    # Set the "active ili" as that of the second lick because it is definitely below threshold
                    i = idx+1
                    ili = ilis[i]

                    # Iterate over ilis starting from second lick in burst and continue adding to list as 
                        # long as they are below threshold. 
                    while ili <= burst_threshold:
                        burst.append(ili)
                        i+=1
                        try:
                            ili = ilis[i]
                        except:
                            # If the last lick in a presentation period is part of a burst, attempting
                                # to increment "ilis[i]" will result in an index error. The loop is done.
                            break
                    burst_idxs.append(burst)                                



                # Calculate the total time from first lick to last lick (i.e. the sum of ilis excluding the firsts)
                    # for each presentation and save the average.
                burst_lengths['Time'].append(np.mean([sum(burst[1:]) for burst in burst_idxs]))

                # Use the same logic to count the average number of licks in each bout. 
                burst_lengths['Licks'].append(np.mean([len(burst) for burst in burst_idxs]))
           
            # POPULATE DATAFRAME

            # Determine index format. 
            if len(concentrations) == 1:
                row_index = animal
            else:
                row_index = (concentration, animal)


            lick_df.loc[row_index, 'Total_Licks'] = total_licks
            lick_df.loc[row_index, 'Burst_Threshold'] = burst_threshold
            lick_df.loc[row_index, 'Burst_Number'] = burst_count
            lick_df.loc[row_index, 'Avg_BurstLength'] = np.mean(burst_lengths['Time'])
            lick_df.loc[row_index, 'AvgLicksInBurst'] = np.mean(burst_lengths['Licks'])

            try:
                for ind_var in subject_grouping_data.columns:
                    lick_df.loc[row_index, ind_var] = subject_grouping_data.loc[animal, ind_var]
            except AttributeError: 
                pass


    lick_df.to_csv(f'LickBoutData_{experiment_label}.csv')

    return lick_df


##### GRAPHING FUNCTIONS ##### 

def graph_cumulative_licks(data_frame_by_animal, animals, experiment_label):
    '''
    :PARAM data_frame_by_animal: total_dataframe_by_animal from gen_summary_dataframe()
    :PARAM animals: list of animal ids. 
    :PARAM experiment_label: The label to use for naming the produced figure.  
    :RETURN: None

    Creates a plot of each animal's cumulative licking over all presentations. 
    '''

    for animal in animals:
        try:
            x_vals = data_frame_by_animal.loc[animal, :].index
            y_vals = data_frame_by_animal.loc[animal, 'LICKS'].values.cumsum()
            plt.plot(x_vals, y_vals, label=animal, marker='+')
        except:
            pass   
    plt.xlabel('Presentation #')
    plt.ylabel('Total Licks')
    plt.title('Cumulative Licks Over Session')
    plt.savefig(f'CumulativeLickCount_{experiment_label}.png')
    plt.close('all')

def individual_graph_by_group(data_frame, experiment_label, grouping_criteria='CONCENTRATION', drop_first_block=True, normalize_by_water_consumption=True):
    '''
    :PARAM data_frame: total_dataframe from gen_summary_dataframe()
    :PARAM experiment_label: The label to use for naming the produced figure.  
    :PARAM grouping_criteria: The category by which to group data (CONCENTRATION/TUBE).
    :PARAM drop_first_block: Determines whether to include the first block of presentations in the average.
    :PARAM normalize_by_water_consumption: Determines whether to use water-normalized licking. 
    :RETURN: None

    Creates a plot of each animal's total licking during each stimulus. 
    '''

    # Determine groups for graphing and calculate block size (if necessary) based on this. 
    groups = natsort.natsorted(set(data_frame.loc[:, grouping_criteria]))

    if drop_first_block:
        block_size = len(groups)
        # Filter out first block by only selecting rows in which the presentation number
            # is greater than the number of presentations in a block.
        data_frame = data_frame.query(f'PRESENTATION>{block_size}')

    # Group data by animal and grouping criteria in preparation for graphing.
    graphing_DF = data_frame.groupby(['AnimalID', grouping_criteria]).mean()

    if normalize_by_water_consumption:
        dv_to_graph = 'Water_Normalized_Licking'
    else:
        dv_to_graph = 'LICKS'

    animals = graphing_DF.index.levels[0]

    for animal in animals:
        x_labels = groups
        x_vals = range(len(x_labels))

        y_vals = graphing_DF.loc[(animal, groups), dv_to_graph].values
        
        plt.plot(x_vals, y_vals, marker='*', label=animal)

    plt.title(f'Licks at each {grouping_criteria}')

    plt.legend()
    
    plt.xticks(x_vals, x_labels)
    plt.xlabel(grouping_criteria)
    
    plt.ylabel(dv_to_graph)
    

    plt.savefig(f'Total{dv_to_graph}DuringPresentation_{experiment_label}.png')
    plt.close('all')

def summarize_licking_curve(data_frame, experiment_label, grouping_criteria='CONCENTRATION', drop_first_block=True, normalize_by_water_consumption=True): 
    '''
    :PARAM data_frame: total_dataframe from gen_summary_dataframe()
    :PARAM experiment_label: The label to use for naming the produced figure.  
    :PARAM grouping_criteria: The category by which to group data (CONCENTRATION/TUBE).
    :PARAM drop_first_block: Determines whether to include the first block of presentations in the average.
    :PARAM normalize_by_water_consumption: Determines whether to use water-normalized licking. 
    :RETURN: None

    Creates a plot of each animal's total licking during each stimulus. 
    '''

   # Determine groups for graphing and calculate block size (if necessary) based on this. 
    def conc_as_float(conc_as_str):
        return float(conc_as_str.replace('%', ''))
    if grouping_criteria == 'CONCENTRATION':
        sort_key = conc_as_float
    else:
        sort_key = None
    
    groups = natsort.natsorted(set(data_frame.loc[:, grouping_criteria]), key=sort_key)

    if drop_first_block:
        block_size = len(groups)
        # Filter out first block by only selecting rows in which the presentation number
            # is greater than the number of presentations in a block.
        data_frame = data_frame.query(f'PRESENTATION>{block_size}')

    if normalize_by_water_consumption:
        dv_to_graph = 'Water_Normalized_Licking'
    else:
        dv_to_graph = 'LICKS'

    # Group data by grouping criteria in preparation for graphing.
    means = data_frame.groupby([grouping_criteria]).mean()
    sems = data_frame.groupby([grouping_criteria]).sem()
    x_vals = range(len(groups))        
    plt.errorbar(x_vals, means.loc[groups, dv_to_graph], yerr=sems.loc[groups, dv_to_graph], marker='*')

    plt.title(f'Licks at each {grouping_criteria}')
    
    plt.xticks(x_vals, groups)
    plt.xlabel(grouping_criteria)
    
    plt.ylabel(dv_to_graph)
    
    plt.savefig(f'LickingCurveSummary_{dv_to_graph}_{experiment_label}.png')
    plt.close('all')

    