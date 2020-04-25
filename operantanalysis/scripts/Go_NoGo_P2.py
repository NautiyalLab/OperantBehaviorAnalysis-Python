from operantanalysis import loop_over_days, extract_info_from_file, reward_retrieval, \
    count_go_nogo_trials, num_successful_go_nogo_trials, lever_press_lat_gng
import pandas as pd
import matplotlib

matplotlib.use("TkAgg")
from matplotlib import pyplot as plt  # noqa

column_list = ['Subject', 'Day', 'Dippers', 'Successful Go Trials', 'Successful NoGo Trials', 'Hit Rate',
               'False Alarm Rate', 'Lever Press Latency', 'Impulsivity Index']


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
    # (press_latency_go) = lever_press_lat_gng(timecode, eventcode, 'LLeverOn', 'SuccessfulGoTrial')
    # if in go trial (light off) then latency as above. If in no go trial then latency is lever on and lever press
    # must define latency as 2 different vars/2 different if statements, since from a data analysis perspective, there
        # is a difference between if a go trial latency is high and if a nogo trial latency is high
    # Need to avg press latency over all events
    # Also output presses? just to confirm latency makes sense? or can manually calculate latency?
    # print("NoGo success", successful_nogo_trials)
    # print("Go success", successful_go_trials)
    df2 = pd.DataFrame([[loaded_file['Subject'], int(i + 1), float(dippers),
                         float(successful_go_trials),
                         float(successful_nogo_trials),
                         float(successful_go_trials) / float(go_trials + 1) * 100,
                         (float(nogo_trials - 1) - float(successful_nogo_trials)) / float(nogo_trials - 1) * 100,
                         float(press_latency),
                         float(successful_go_trials) - float(successful_nogo_trials)]],
                       columns=column_list)

    return df2


(days, df) = loop_over_days(column_list, Go_NoGo)
print(df.to_string())
df.to_excel("output.xlsx")

group_means = df.groupby(['Day'])[
    'Dippers', 'Hit Rate', 'False Alarm Rate', 'Lever Press Latency', 'Impulsivity Index'].mean().unstack()
group_sems = df.groupby(['Day'])[
    'Dippers', 'Hit Rate', 'False Alarm Rate', 'Lever Press Latency', 'Impulsivity Index'].sem().unstack()

print(df.groupby(['Day'])[
          'Dippers', 'Hit Rate', 'False Alarm Rate', 'Lever Press Latency', 'Impulsivity Index'].mean().unstack().to_string())
print(df.groupby(['Day'])[
          'Dippers', 'Hit Rate', 'False Alarm Rate', 'Lever Press Latency', 'Impulsivity Index'].sem().unstack().to_string())

group_means['Hit Rate'].plot(legend=True, yerr=group_sems['Hit Rate'], ylim=[0, 100],
                             xlim=[0, days + 1], xticks=(range(1, days + 1, 1)), marker='o', capsize=3, elinewidth=1)
plt.ylabel('Hit Rate')

group_means['False Alarm Rate'].plot(legend=True, yerr=group_sems['False Alarm Rate'], ylim=[0, 100],
                                     xlim=[0, days + 1], xticks=(range(1, days + 1, 1)), marker='o', capsize=3,
                                     elinewidth=1)
plt.ylabel('False Alarm Rate')

group_means['Lever Press Latency'].plot(legend=True, yerr=group_sems['Lever Press Latency'],
                                        xlim=[0, days + 1], xticks=(range(1, days + 1, 1)), marker='o', capsize=3,
                                        elinewidth=1)
plt.ylabel('Lever Press Latency')

group_means['Impulsivity Index'].plot(legend=True, yerr=group_sems['Impulsivity Index'],
                                      xlim=[0, days + 1], xticks=(range(1, days + 1, 1)), marker='o', capsize=3,
                                      elinewidth=1)
plt.ylabel('Impulsivity Index')

plt.show()
