from operantanalysis import loop_over_days, extract_info_from_file, cue_iti_responding
import pandas as pd


column_list = ['Subject', 'Condition', 'Day', 'Pre Pokes', 'Pre ITI', 'Pre ES', 'Con Pokes',
               'Con ITI', 'Con ES']


def LI_function(loaded_file, i):
    """
    :param loaded_file: file output from operant box
    :param i: number of days analyzing
    :return: data frame of all analysis extracted from file (one animal)
    """

    (timecode, eventcode) = extract_info_from_file(loaded_file, 500)
    (A_responding, A_iti) = cue_iti_responding(timecode, eventcode, 'ExcitorATrialStart', 'ExcitorATrialEnd', 'PokeOn1')
    (B_responding, B_iti) = cue_iti_responding(timecode, eventcode, 'ExcitorBTrialStart', 'ExcitorBTrialEnd', 'PokeOn1')

    df2 = pd.DataFrame([[loaded_file['Subject'], loaded_file['MSN'], int(i + 1),
                         float(A_responding), float(A_iti), (float(A_responding) - float(A_iti)),
                         float(B_responding), float(B_iti), (float(B_responding) - float(B_iti))]],
                       columns=column_list)

    return df2


(days, df) = loop_over_days(column_list, LI_function)
print(df.to_string())
df.to_excel("output.xlsx")