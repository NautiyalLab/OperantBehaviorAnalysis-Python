from operantanalysis import loop_over_days, extract_info_from_file, reward_retrieval, lever_pressing
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt  # noqa

column_list = ['Subject', 'Day', 'Training', 'Dippers', 'Dippers Retrieved', 'Retrieval Latency',
               'Lever Presses']


def habit_training_function(loaded_file, i):
    """
    :param loaded_file: file output from operant box
    :param i: number of days analyzing
    :return: data frame of all analysis extracted from file (one animal)
    """
    (timecode, eventcode) = extract_info_from_file(loaded_file, 500)
    (dippers, dippers_retrieved, retrieval_latency) = reward_retrieval(timecode, eventcode)
    (left_presses, right_presses, total_presses) = lever_pressing(eventcode, 'LPressOn', 'RPressOn')

    df2 = pd.DataFrame([[loaded_file['Subject'], int(i + 1), loaded_file['Training'],
                         float(dippers), float(dippers_retrieved), float(retrieval_latency), float(total_presses)]],
                       columns=column_list)

    return df2


(days, df) = loop_over_days(column_list, habit_training_function)

group_means = df.groupby(['Day', 'Training'])['Dippers', 'Lever Presses'].mean().unstack()
group_sems = df.groupby(['Day', 'Training'])['Dippers', 'Lever Presses'].sem().unstack()

group_means['Lever Presses'].plot(legend=True, yerr=group_sems['Lever Presses'],
                                  xlim=[0, days + 1], xticks=(range(1, days + 1, 1)), marker='o', capsize=3, elinewidth=1)
plt.ylabel('Lever Presses')

group_means['Dippers'].plot(legend=True, yerr=group_sems['Dippers'], ylim=[0, 60],
                            xlim=[0, days + 1], xticks=(range(1, days + 1, 1)), marker='o', capsize=3, elinewidth=1)
plt.ylabel('Dippers')
plt.show()
