from operantanalysis import loop_over_days, extract_info_from_file, reward_retrieval,\
    count_go_nogo_trials, num_successful_go_nogo_trials
import pandas as pd


column_list = ['Subject', 'tts', 'Day', 'Dippers', 'Go Trials', 'Successful Go Trials']


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
    df2 = pd.DataFrame([[loaded_file['Subject'], loaded_file['tts'], int(i + 1), float(dippers), float(go_trials),
                         float(successful_go_trials)]],
                       columns=column_list)

    return df2


(days, df) = loop_over_days(column_list, Go_NoGo)
print(df.to_string())
df.to_excel("output.xlsx")

group_means = df.groupby(['Day', 'tts'])['Dippers', 'Successful Go Trials'].mean()
group_sems = df.groupby(['Day', 'tts'])['Dippers', 'Successful Go Trials'].sem()

print(df.groupby(['Day', 'tts'])['Dippers', 'Successful Go Trials'].mean().unstack().to_string())
print(df.groupby(['Day', 'tts'])['Dippers', 'Successful Go Trials'].sem().unstack().to_string())
