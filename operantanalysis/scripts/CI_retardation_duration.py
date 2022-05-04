from operantanalysis import loop_over_days, extract_info_from_file, cue_responding_duration
import pandas as pd


column_list = ['Subject', 'Condition', 'Day', 'Light Poke Duration', 'LightITI']


def CI_retardation_function(loaded_file, i):
    """
    :param loaded_file: file output from operant box
    :param i: number of days analyzing
    :return: data frame of all analysis extracted from file (one animal)
    """
    (timecode, eventcode) = extract_info_from_file(loaded_file, 500)
    (X_dur_individual, X_dur_total, XITI_dur_individual, XITI_dur_total) = cue_responding_duration(timecode, eventcode, 'InhibitorTrialStart', 'InhibitorTrialEnd', 'PokeOn1', 'PokeOff1')
    df2 = pd.DataFrame([[loaded_file['Subject'], loaded_file['MSN'], int(i + 1),
                         float(X_dur_total), float(XITI_dur_total)]], columns=column_list)

    return df2


(days, df) = loop_over_days(column_list, CI_retardation_function)
print(df.to_string())
df.to_excel("output.xlsx")
