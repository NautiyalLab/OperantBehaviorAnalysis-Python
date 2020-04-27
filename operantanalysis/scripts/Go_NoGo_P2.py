from operantanalysis import loop_over_days, extract_info_from_file, reward_retrieval, \
    count_go_nogo_trials, num_successful_go_nogo_trials, lever_press_lat_gng_new

import pandas as pd
import matplotlib

matplotlib.use("TkAgg")
from matplotlib import pyplot as plt  # noqa

column_list = ['Subject', 'Day', 'Dippers', 'Successful Go Trials', 'Successful NoGo Trials', 'Hit Rate',
               'False Alarm Rate', 'Lever Press Latency Go', 'Lever Press Latency NoGo', 'Impulsivity Index']

def Go_NoGo(loaded_file, i):
    """
    :param loaded_file: file output from operant box
    :param i: number of days analyzing
    :return: data frame of all analysis extracted from file (one animal)
    """
    (timecode, eventcode) = extract_info_from_file(loaded_file, 500)
    (dippers, dippers_retrieved, retrieval_latency) = reward_retrieval(timecode, eventcode)
    (go_trials) = 30
    (nogo_trials) = 30
    (successful_go_trials, successful_nogo_trials) = num_successful_go_nogo_trials(eventcode)
    (press_latency_go, press_latency_nogo) = lever_press_lat_gng_new(timecode, eventcode)

    df2 = pd.DataFrame([[loaded_file['Subject'], int(i + 1), float(dippers),
                         float(successful_go_trials),
                         float(successful_nogo_trials),
                         float(successful_go_trials) / float(go_trials) * 100,
                         (float(nogo_trials) - float(successful_nogo_trials)) / float(nogo_trials) * 100,
                         float(press_latency_go),
                         float(press_latency_nogo),
                         float(successful_go_trials) - float(successful_nogo_trials)]],
                       columns=column_list)

    return df2

(days, df) = loop_over_days(column_list, Go_NoGo)
print(df.to_string())
df.to_excel("output.xlsx")

group_means = df.groupby(['Day'])[
    'Dippers', 'Hit Rate', 'False Alarm Rate', 'Lever Press Latency Go', 'Lever Press Latency NoGo', 'Impulsivity Index'].mean().unstack()
group_sems = df.groupby(['Day'])[
    'Dippers', 'Hit Rate', 'False Alarm Rate', 'Lever Press Latency Go', 'Lever Press Latency NoGo', 'Impulsivity Index'].sem().unstack()

print(df.groupby(['Day'])[
          'Dippers', 'Hit Rate', 'False Alarm Rate', 'Lever Press Latency Go', 'Lever Press Latency NoGo', 'Impulsivity Index'].mean().unstack().to_string())
print(df.groupby(['Day'])[
          'Dippers', 'Hit Rate', 'False Alarm Rate', 'Lever Press Latency Go', 'Lever Press Latency NoGo', 'Impulsivity Index'].sem().unstack().to_string())

group_means['Hit Rate'].plot(legend=True, yerr=group_sems['Hit Rate'], ylim=[0, 100],
                             xlim=[0, days + 1], xticks=(range(1, days + 1, 1)), marker='o', capsize=3, elinewidth=1)
plt.ylabel('Hit Rate')

group_means['False Alarm Rate'].plot(legend=True, yerr=group_sems['False Alarm Rate'], ylim=[0, 100],
                                     xlim=[0, days + 1], xticks=(range(1, days + 1, 1)), marker='o', capsize=3,
                                     elinewidth=1)
plt.ylabel('False Alarm Rate')

group_means['Lever Press Latency Go'].plot(legend=True, yerr=group_sems['Lever Press Latency Go'],
                                        xlim=[0, days + 1], xticks=(range(1, days + 1, 1)), marker='o', capsize=3,
                                        elinewidth=1)
plt.ylabel('Lever Press Latency Go')

group_means['Lever Press Latency NoGo'].plot(legend=True, yerr=group_sems['Lever Press Latency NoGo'],
                                        xlim=[0, days + 1], xticks=(range(1, days + 1, 1)), marker='o', capsize=3,
                                        elinewidth=1)
plt.ylabel('Lever Press Latency NoGo')

group_means['Impulsivity Index'].plot(legend=True, yerr=group_sems['Impulsivity Index'],
                                      xlim=[0, days + 1], xticks=(range(1, days + 1, 1)), marker='o', capsize=3,
                                      elinewidth=1)
plt.ylabel('Impulsivity Index')

plt.show()
