from operantanalysis import loop_over_days, extract_info_from_file, binned_responding_duration
import pandas as pd


column_list = ['Subject', 'Noise Poke', 'Inhibitor Poke']


def CI_summation_bin_function(loaded_file, i):
    """
    :param loaded_file: file output from operant box
    :param i: number of days analyzing
    :return: data frame of all analysis extracted from file (one animal)
    """
    (timecode, eventcode) = extract_info_from_file(loaded_file, 500)
    (B_dur_individual, B_dur_total, BITI_dur_individual, BITI_dur_total) = binned_responding_duration(timecode, eventcode, 'ExcitorBTrialStart', 'ExcitorBTrialEnd', 'PokeOn1', 'PokeOff1')
    (BX_dur_individual, BX_dur_total, BXITI_dur_individual, BXITI_dur_total) = binned_responding_duration(timecode, eventcode, 'InhibitorTrialStart', 'InhibitorTrialEnd', 'PokeOn1', 'PokeOff1')
    df2 = pd.DataFrame([[loaded_file['Subject'], float(B_dur_total), float(BX_dur_total)]], columns=column_list)
    # change bins in operantanalysis file
    return df2


(days, df) = loop_over_days(column_list, CI_summation_bin_function)
print(df.to_string())
df.to_excel("output.xlsx")
