from operantanalysis import loop_over_days, extract_info_from_file, reward_retrieval, cue_responding_duration, \
    total_head_pokes, cue_iti_responding, duration_across_cue_iti, get_events_indices
import pandas as pd

column_list = ['Subject', 'Day', 'Dippers', 'Dippers Retrieved', 'Retrieval Latency', 'Avg Poke Dur', 'Tot Poke Dur',
               'Total Pokes Count']


def PCER_dur_function(loaded_file, i):
    """
    :param loaded_file: file output from operant box
    :param i: number of days analyzing
    :return: data frame of all analysis extracted from file (one animal)
    """

    (timecode, eventcode) = extract_info_from_file(loaded_file, 500)
    print(timecode)

    # code to delete trials immediately before or overlapping with cue
    dip_on2 = get_events_indices(eventcode, ['DipOn'])
    trial_on = get_events_indices(eventcode, ['StartTrial'])
    trial_off = get_events_indices(eventcode, ['EndTrial', 'EndSession'])
    delete_trial = []
    for j in range(len(trial_on)):
        for k in range(len(dip_on2)):
            cue_on_idx2 = trial_on[j]
            cue_off_idx2 = trial_off[j]
            dip_on_idx2 = dip_on2[k]
            if (timecode[cue_on_idx2] - 5) <= timecode[dip_on_idx2] <= (timecode[cue_on_idx2] + 8):
                if cue_on_idx2 not in delete_trial:
                    delete_trial += [cue_on_idx2]
                    if eventcode[cue_off_idx2] != eventcode[-1]:
                        delete_trial += [cue_off_idx2]
    print(delete_trial)
    for trial in reversed(delete_trial):
        del timecode[trial]
        del eventcode[trial]

    (dippers, dippers_retrieved, retrieval_latency) = reward_retrieval(timecode, eventcode)
    cue_iti_responding(timecode, eventcode, 'StartTrial', 'EndTrial', 'PokeOn1')
    (ind_dur, tot_dur, ind_dur_iti, tot_dur_iti) = cue_responding_duration(timecode, eventcode, 'StartTrial',
                                                                           'EndTrial', 'PokeOn1', 'PokeOff1')
    total_pokes = total_head_pokes(eventcode)
    (all_cue_length_poke_dur, all_iti_length_poke_dur, subtracted_poke_dur) = \
        duration_across_cue_iti(timecode, eventcode, 'StartTrial', 'EndTrial', 'PokeOn1', 'PokeOff1')
    new_cols = ['Subject'] + ['Cue_' + str(i + 1) for i in range(len(all_cue_length_poke_dur))] + \
               ['ITI_' + str(i + 1) for i in range(len(all_cue_length_poke_dur))] + \
               ['ES_' + str(i + 1) for i in range(len(all_cue_length_poke_dur))]
    across_cue_df = pd.DataFrame(
        [([loaded_file['Subject']] + all_cue_length_poke_dur + all_iti_length_poke_dur + subtracted_poke_dur)],
        columns=new_cols)

    df2 = pd.DataFrame([[loaded_file['Subject'], int(i + 1), float(dippers), float(dippers_retrieved),
                         float(retrieval_latency), float(ind_dur), float(tot_dur), float(total_pokes)]],
                       columns=column_list)
    df2 = pd.merge(df2, across_cue_df, how='left', on=['Subject'])

    return df2


(days, df) = loop_over_days(column_list, PCER_dur_function)
print(df.to_string())
df.to_excel("output.xlsx")
