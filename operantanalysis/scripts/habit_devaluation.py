from operantanalysis import loop_over_days, extract_info_from_file, reward_retrieval
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt  # noqa

column_list = ['Subject', 'Sex', 'Day', 'Training', 'Dippers', 'Dippers Retrieved', 'Retrieval Latency']


def habit_training_function(loaded_file, i):
    """
    :param loaded_file: file output from operant box
    :param i: number of days analyzing
    :return: data frame of all analysis extracted from file (one animal)
    """
    (timecode, eventcode) = extract_info_from_file(loaded_file, 500)
    (dippers, dippers_retrieved, retrieval_latency) = reward_retrieval(timecode, eventcode)

    df2 = pd.DataFrame([[loaded_file['Subject'], loaded_file['Sex'], int(i + 1), loaded_file['Training'],
                         float(dippers), float(dippers_retrieved), float(retrieval_latency)]], columns=column_list)

    return df2


(days, df) = loop_over_days(column_list, habit_training_function)

group_means = df.groupby(['Day', 'Training'])['Dippers', 'Retrieval Latency'].mean().unstack()
group_sems = df.groupby(['Day', 'Training'])['Dippers', 'Retrieval Latency'].sem().unstack()

group_means['Retrieval Latency'].plot(legend=True, yerr=group_sems['Retrieval Latency'], xticks=(range(1, days + 1, 1)),
                                      xlim=[0, days + 1], marker='o', capsize=3, elinewidth=1)
plt.ylabel('Retrieval Latency (sec)')

group_means['Dippers'].plot(legend=True, yerr=group_sems['Dippers'], ylim=[0, 30],
                            xlim=[0, days + 1], xticks=(range(1, days + 1, 1)), marker='o', capsize=3, elinewidth=1)
plt.ylabel('Dippers')
plt.show()
