from operantanalysis import loop_over_days, extract_info_from_file, reward_retrieval, cue_responding_duration,\
    total_head_pokes
import pandas as pd

column_list = ['Subject', 'Day', 'Dippers', 'Dippers Retrieved', 'Retrieval Latency', 'Avg Poke Dur', 'Tot Poke Dur',
               'Total Pokes Count']


def trough_train_function(loaded_file, i):
    """
    :param loaded_file: file output from operant box
    :param i: number of days analyzing
    :return: data frame of all analysis extracted from file (one animal)
    """
    (timecode, eventcode) = extract_info_from_file(loaded_file, 500)
    (dippers, dippers_retrieved, retrieval_latency) = reward_retrieval(timecode, eventcode)
    (ind_dur, tot_dur, ind_dur_iti, tot_dur_iti) = cue_responding_duration(timecode, eventcode, 'StartSession', 'EndSession', "PokeOn1", "PokeOff1")
    # ITI is meaningless here because we are using the whole session
    total_pokes = total_head_pokes(eventcode)

    df2 = pd.DataFrame([[loaded_file['Subject'], int(i + 1), float(dippers), float(dippers_retrieved),
                         float(retrieval_latency), float(ind_dur), float(tot_dur), float(total_pokes)]],
                       columns=column_list)

    return df2


(days, df) = loop_over_days(column_list, trough_train_function)
print(df.to_string())
df.to_excel("output.xlsx")
