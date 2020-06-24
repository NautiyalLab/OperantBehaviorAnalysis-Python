from operantanalysis import loop_over_days, extract_info_from_file, reward_retrieval, num_switch_trials,\
    lever_press_latency_Switch
import pandas as pd
import matplotlib

matplotlib.use("TkAgg")

column_list = ['Subject', 'Program', 'Day', 'Dippers', 'Large Rewards', 'Small Rewards', 'Forced Latency']


def crf_function(loaded_file, i):
    """
    :param loaded_file: file output from operant box
    :param i: number of days analyzing
    :return: data frame of all analysis extracted from file (one animal)
    """
    (timecode, eventcode) = extract_info_from_file(loaded_file, 500)
    (dippers, dippers_retrieved, retrieval_latency) = reward_retrieval(timecode, eventcode)
    (large_rewards, small_rewards) = num_switch_trials(eventcode)
    (forced_latency) = lever_press_latency_Switch(timecode, eventcode)

    df2 = pd.DataFrame([[loaded_file['Subject'], loaded_file['MSN'], int(i + 1), float(dippers),
                         float(large_rewards), float(small_rewards), float(forced_latency)]], columns=column_list)

    return df2


(days, df) = loop_over_days(column_list, crf_function)
print(df.to_string())
df.to_excel("output.xlsx")
