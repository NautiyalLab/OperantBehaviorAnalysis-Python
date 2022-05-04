from operantanalysis import loop_over_days, extract_info_from_file, reward_retrieval,\
    count_go_nogo_trials, num_successful_go_nogo_trials, lever_press_lat_gng
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt  # noqa


column_list = ['Subject', 'Day', 'Dippers', 'Hit Rate', 'False Alarm Rate', 'Impulsivity Index', 'Go Latency']


def Go_NoGo(loaded_file, i):
    """
    :param loaded_file: file output from operant box
    :param i: number of days analyzing
    :return: data frame of all analysis extracted from file (one animal)
    """
    (timecode, eventcode) = extract_info_from_file(loaded_file, 500)
    (dippers, dippers_retrieved, retrieval_latency) = reward_retrieval(timecode, eventcode)
    (go_trials, nogo_trials) = count_go_nogo_trials(eventcode)
    (successful_go_trials, successful_nogo_trials) = num_successful_go_nogo_trials(eventcode)
    go_latency = lever_press_lat_gng(timecode, eventcode, 'LLeverOn', 'SuccessfulGoTrial') + \
                 lever_press_lat_gng(timecode, eventcode, 'RLeverOn', 'SuccessfulGoTrial')
    df2 = pd.DataFrame([[loaded_file['Subject'], int(i + 1), float(dippers),
                         float(successful_go_trials) / float(go_trials),
                         (float(nogo_trials) - float(successful_nogo_trials)) / float(nogo_trials),
                         (float(successful_go_trials) / float(go_trials)) - (float(successful_nogo_trials) / float(nogo_trials)),
                         float(go_latency)]],
                       columns=column_list)

    return df2


(days, df) = loop_over_days(column_list, Go_NoGo)
print(df.to_string())
df.to_excel("output.xlsx")
