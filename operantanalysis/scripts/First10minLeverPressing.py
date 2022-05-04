from operantanalysis import loop_over_days, extract_info_from_file, reward_retrieval, lever_pressing
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
    timecode[:] = [time for time in timecode if time <= 300]
    n = len(eventcode)
    for event in range(0, n - len(timecode)):
        eventcode.pop()
    dippers = eventcode.count('DipOn')
    (left_presses, right_presses, total_presses) = lever_pressing(eventcode, 'LPressOn', 'RPressOn')

    df2 = pd.DataFrame([[loaded_file['Subject'], int(i + 1), float(dippers),
                         float(total_presses)]], columns=column_list)

    return df2


(days, df) = loop_over_days(column_list, first10_function)
print(df.to_string())
df.to_excel("output.xlsx")