from operantanalysis import load_file, extract_info_from_file, reward_retrieval
import glob
from tkinter import filedialog
from tkinter import *  # noqa
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt  # noqa

days = int(input("How many days would you like to analyze?"))
column_list = ['Subject', 'Day', 'Dippers', 'Dippers Retrieved', 'Retrieval Latency']
df = pd.DataFrame(columns=column_list)


for i in range(days):
    root = Tk()  # noqa
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    x = folder_selected + '/*'

    for file in sorted(glob.glob(x)):
        loaded_file = load_file(file)
        (timecode, eventcode) = extract_info_from_file(loaded_file, 500)
        (dippers, dippers_retrieved, retrieval_latency) = reward_retrieval(timecode, eventcode)
        df2 = pd.DataFrame([[loaded_file['Subject'], int(i + 1), float(dippers), float(dippers_retrieved),
                             float(retrieval_latency)]], columns=column_list)
        df = df.append(df2, ignore_index=True)

group_means = df.groupby(['Day'])['Dippers Retrieved', 'Retrieval Latency'].mean()
group_sems = df.groupby(['Day'])['Dippers Retrieved', 'Retrieval Latency'].sem()

plt.subplot(121)
group_means['Dippers Retrieved'].plot(legend=True, yerr=group_sems['Dippers Retrieved'], ylim=[0, 60], xlim=[0, days + 1],
                                      xticks=(range(1, days + 1, 1)), marker='o', capsize=3, elinewidth=1)
plt.ylabel('Dippers Retrieved')

plt.subplot(122)
group_means['Retrieval Latency'].plot(legend=True, yerr=group_sems['Retrieval Latency'], ylim=[0, 20], xlim=[0, days + 1],
                                      xticks=(range(1, days + 1, 1)), marker='o', capsize=3, elinewidth=1)
plt.ylabel('Retrieval Latency (sec)')
plt.show()
