from operantanalysis import loop_over_days, extract_info_from_file, reward_retrieval, cue_responding_duration, \
    total_head_pokes, cue_iti_responding, response_rate_across_cue_iti
import pandas as pd

column_list = ['Subject', 'Day', 'Dippers', 'Dippers Retrieved', 'Retrieval Latency', 'Avg Poke Dur', 'Tot Poke Dur',
               'Total Pokes Count']


def PCER_P2_function(loaded_file, i):
    """
    :param loaded_file: file output from operant box
    :param i: number of days analyzing
    :return: data frame of all analysis extracted from file (one animal)
    """
    (timecode, eventcode) = extract_info_from_file(loaded_file, 500)
    (dippers, dippers_retrieved, retrieval_latency) = reward_retrieval(timecode, eventcode)
    (ind_dur, tot_dur, ind_dur_iti, tot_dur_iti) = cue_responding_duration(timecode, eventcode, 'StartTrial',
                                                                           'EndTrial', 'PokeOn1', 'PokeOff1')
    total_pokes = total_head_pokes(eventcode)
    (paired_length_poke_rates, paired_iti_length_poke_rates, paired_subtracted_poke_rates) = \
        response_rate_across_cue_iti(timecode, eventcode, 'ToneOn1', 'DipOn', 'PokeOn1')
    (unpaired_length_poke_rates, unpaired_iti_length_poke_rates, unpaired_subtracted_poke_rates) = \
        response_rate_across_cue_iti(timecode, eventcode, 'StartTrial', 'EndTrial', 'PokeOn1')
    new_cols = ['Subject'] + ['Paired_' + str(i + 1) for i in range(len(paired_length_poke_rates))] + \
               ['Paired_ITI_' + str(i + 1) for i in range(len(paired_length_poke_rates))] + \
               ['Paired_ES_' + str(i + 1) for i in range(len(paired_length_poke_rates))] + \
               ['Unpaired_' + str(i + 1) for i in range(len(paired_length_poke_rates))] + \
               ['Unpaired_ITI_' + str(i + 1) for i in range(len(paired_length_poke_rates))] + \
               ['Unpaired_ES_' + str(i + 1) for i in range(len(paired_length_poke_rates))]
    across_cue_df = pd.DataFrame([([loaded_file['Subject']] + paired_length_poke_rates + paired_iti_length_poke_rates +
                                   paired_subtracted_poke_rates + unpaired_length_poke_rates + unpaired_iti_length_poke_rates +
                                   unpaired_subtracted_poke_rates)],
                                 columns=new_cols)

    df2 = pd.DataFrame([[loaded_file['Subject'], int(i + 1), float(dippers), float(dippers_retrieved),
                         float(retrieval_latency), float(ind_dur), float(tot_dur), float(total_pokes)]],
                       columns=column_list)
    df2 = pd.merge(df2, across_cue_df, how='left', on=['Subject'])

    return df2


(days, df) = loop_over_days(column_list, PCER_P2_function)
print(df.to_string())
df.to_excel("output.xlsx")
