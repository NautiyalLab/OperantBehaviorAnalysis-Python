from operantanalysis import loop_over_days, extract_info_from_file, reward_retrieval, lever_pressing, bin_by_time
#    lever_press_latency, cue_iti_responding
import pandas as pd
import matplotlib

matplotlib.use("TkAgg")
from matplotlib import pyplot as plt  # noqa

column_list = ['Subject', 'Day', 'Dippers', 'Total Presses']


def first10_function(loaded_file, i):
    """
    :param loaded_file: file output from operant box
    :param i: number of days analyzing
    :return: data frame of all analysis extracted from file (one animal)
    """
    (timecode, eventcode) = extract_info_from_file(loaded_file, 500)
    timecode[:] = [time for time in timecode if time <= 600]

    n = len(eventcode)
    for event in range(0, n - len(timecode)):
        eventcode.pop()
    dippers = eventcode.count('DipOn')

    (left_presses, right_presses, total_presses) = lever_pressing(eventcode, 'LPressOn', 'RPressOn')

    (timecode, eventcode) = extract_info_from_file(loaded_file, 500)
    binned_list = bin_by_time(timecode, eventcode, 300, 'DipOn')

    new_cols = ['Subject'] + ['Bin_' + str(i + 1) for i in range(len(binned_list))]
    across_cue_df = pd.DataFrame(
        [([loaded_file['Subject']] + binned_list)],
        columns=new_cols)

    df2 = pd.DataFrame([[loaded_file['Subject'], int(i + 1), float(dippers),
                         float(total_presses)]], columns=column_list)
    df2 = pd.merge(df2, across_cue_df, how='left', on=['Subject'])

    return df2


(days, df) = loop_over_days(column_list, first10_function)
print(df.to_string())
df.to_excel("output.xlsx")