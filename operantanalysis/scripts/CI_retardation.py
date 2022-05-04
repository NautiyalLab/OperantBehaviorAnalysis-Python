from operantanalysis import loop_over_days, extract_info_from_file, cue_iti_responding
import pandas as pd


column_list = ['Subject', 'Condition', 'Day', 'Light Responding', 'Light ITI']


def CI_retardation_function(loaded_file, i):
    """
    :param loaded_file: file output from operant box
    :param i: number of days analyzing
    :return: data frame of all analysis extracted from file (one animal)
    """
    (timecode, eventcode) = extract_info_from_file(loaded_file, 500)
    (X_responding, X_iti) = cue_iti_responding(timecode, eventcode, 'InhibitorTrialStart', 'InhibitorTrialEnd', 'PokeOn1')
    df2 = pd.DataFrame([[loaded_file['Subject'], loaded_file['MSN'], int(i + 1), float(X_responding),
                         float(X_iti)]], columns=column_list)

    return df2


(days, df) = loop_over_days(column_list, CI_retardation_function)
print(df.to_string())
df.to_excel("output.xlsx")
