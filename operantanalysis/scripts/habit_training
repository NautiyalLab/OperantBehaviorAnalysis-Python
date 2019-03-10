from operantanalysis import load_file, extract_info_from_file,  reward_retrieval, lever_pressing
import glob
from tkinter import filedialog
from tkinter import *  # noqa
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt  # noqa

days = int(input("How many days would you like to analyze?"))
column_list = ['Subject', 'Sex', 'Day', 'Training', 'Dippers', 'Dippers Retrieved', 'Retrieval Latency',
               'Lever Presses']
df = pd.DataFrame(columns=column_list)


for i in range(days):
    root = Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    x = folder_selected + '/*'

    for file in sorted(glob.glob(x)):
        loaded_file = load_file(file)
        (timecode, eventcode) = extract_info_from_file(loaded_file, 500)
        (dippers, dippers_retrieved, retrieval_latency) = reward_retrieval(timecode, eventcode)
        (left_presses, right_presses, total_presses) = lever_pressing(eventcode, 'LPressOn', 'RPressOn')
        df2 = pd.DataFrame([[loaded_file['Subject'], loaded_file['Sex'], int(i + 1), loaded_file['Training'],
                             float(dippers), float(dippers_retrieved), float(retrieval_latency), float(total_presses)]], columns=column_list)
        df = df.append(df2, ignore_index=True)

group_means = df.groupby(['Day', 'Training'])['Dippers', 'Lever Presses'].mean().unstack()
group_sems = df.groupby(['Day', 'Training'])['Dippers', 'Lever Presses'].sem().unstack()

group_means['Lever Presses'].plot(legend=True, yerr=group_sems['Lever Presses'], ylim=[0, 5000],
                                  xlim=[0, days+1], xticks=(range(1, days+1, 1)), marker='o', capsize=3, elinewidth=1)
plt.ylabel('Lever Presses')

group_means['Dippers'].plot(legend=True, yerr=group_sems['Dippers'], ylim=[0, 60],
                            xlim=[0, days+1], xticks=(range(1, days+1, 1)), marker='o', capsize=3, elinewidth=1)
plt.ylabel('Dippers')
plt.show()
