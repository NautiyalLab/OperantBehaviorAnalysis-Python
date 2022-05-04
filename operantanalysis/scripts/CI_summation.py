from operantanalysis import loop_over_days, extract_info_from_file, cue_iti_responding, binned_responding
import pandas as pd


column_list = ['Subject', 'Condition', 'Day', 'Noise Responding', 'Noise ITI', 'Inhibitor Trial Responding',
               'Inhibitor ITI', 'Noise Responding 5', 'Noise ITI 5', 'Inhibitor Trial Responding 5', 'Inhibitor ITI 5']


def CI_summation_function(loaded_file, i):
    """
    :param loaded_file: file output from operant box
    :param i: number of days analyzing
    :return: data frame of all analysis extracted from file (one animal)
    """
    (timecode, eventcode) = extract_info_from_file(loaded_file, 500)
    (B_responding, B_iti) = cue_iti_responding(timecode, eventcode, 'ExcitorBTrialStart', 'ExcitorBTrialEnd', 'PokeOn1')
    (inhibitor_responding, inhibitor_iti) = cue_iti_responding(timecode, eventcode, 'InhibitorTrialStart', 'InhibitorTrialEnd', 'PokeOn1')
    (B_responding_5, B_iti_5) = binned_responding(timecode, eventcode, 'ExcitorBTrialStart', 'ExcitorBTrialEnd', 'PokeOn1', 5)
    (inhibitor_responding_5, inhibitor_iti_5) = binned_responding(timecode, eventcode, 'InhibitorTrialStart', 'InhibitorTrialEnd', 'PokeOn1', 5)
    df2 = pd.DataFrame([[loaded_file['Subject'], loaded_file['MSN'], int(i + 1), float(B_responding),
                         float(B_iti), float(inhibitor_responding), float(inhibitor_iti), float(B_responding_5),
                         float(B_iti_5), float(inhibitor_responding_5), float(inhibitor_iti_5)]], columns=column_list)

    return df2


(days, df) = loop_over_days(column_list, CI_summation_function)
print(df.to_string())
df.to_excel("output.xlsx")
