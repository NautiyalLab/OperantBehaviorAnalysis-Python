from operantanalysis import loop_over_days, extract_info_from_file, cue_responding_duration
import pandas as pd


column_list = ['Subject', 'Condition', 'Day', 'Click Pokes Duration', 'Click ITI', 'Noise Pokes Duration',
               'Noise ITI', 'Inhibitor Pokes Duration', 'Inhibitor ITI']


def CI_training_function(loaded_file, i):
    """
    :param loaded_file: file output from operant box
    :param i: number of days analyzing
    :return: data frame of all analysis extracted from file (one animal)
    """

    (timecode, eventcode) = extract_info_from_file(loaded_file, 500)
    (A_dur_individual, A_dur_total, AITI_dur_individual, AITI_dur_total) = cue_responding_duration(timecode, eventcode, 'ExcitorATrialStart', 'ExcitorATrialEnd', 'PokeOn1', 'PokeOff1')
    (B_dur_individual, B_dur_total, BITI_dur_individual, BITI_dur_total) = cue_responding_duration(timecode, eventcode, 'ExcitorBTrialStart', 'ExcitorBTrialEnd', 'PokeOn1', 'PokeOff1')
    (X_dur_individual, X_dur_total, XITI_dur_individual, XITI_dur_total) = cue_responding_duration(timecode, eventcode, 'InhibitorTrialStart', 'InhibitorTrialEnd', 'PokeOn1', 'PokeOff1')

    df2 = pd.DataFrame([[loaded_file['Subject'], loaded_file['MSN'], int(i + 1),
                         float(A_dur_total), float(AITI_dur_total), float(B_dur_total), float(BITI_dur_total),
                         float(X_dur_total), float(XITI_dur_total)]], columns=column_list)

    return df2


(days, df) = loop_over_days(column_list, CI_training_function)
print(df.to_string())
df.to_excel("output.xlsx")
