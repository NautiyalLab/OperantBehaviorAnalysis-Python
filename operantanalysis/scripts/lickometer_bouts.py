import numpy as np
import os
import glob
from tkinter import filedialog
from tkinter import *  # noqa
import pandas as pd
import math
import statistics

root = Tk()  # noqa
root.withdraw()
folder_selected = filedialog.askdirectory()
file_pattern = os.path.join(folder_selected, '*')

for file in sorted(glob.glob(file_pattern)):
    df = pd.read_csv(file)
df.rename(columns=df.iloc[0]).drop(df.index[0])
print(df)
df2 = pd.DataFrame()
df3 = pd.DataFrame()
df4means = pd.DataFrame()

for colname, col in df.iteritems():
    bout_list = []
    rate_list = []
    bout = 0
    lick_count = 0
    x2 = 0
    nan = 0
    for x in col:
        x2 += 1
        if x <= 1000:
            bout += x
            lick_count += 1
            if x2 == len(col):
                bout_list += [bout]
                if bout > 0:
                    rate_list += [lick_count / bout]
                bout = 0
        elif x > 1000:
            bout_list += [bout]
            if bout > 0:
                rate_list += [lick_count / bout]
            bout = 0
            lick_count = 1
        elif math.isnan(x) and nan < 1:
            nan += 1
            bout_list += [bout]
            if bout > 0:
                rate_list += [lick_count / bout]
            bout = 0
    if len(rate_list) == 0:
        mean_bout_l = 0
        mean_rate = 0
    else:
        mean_bout_l = sum(bout_list)/len(rate_list)
        mean_rate = sum(rate_list)/len(rate_list)
    dftemp = pd.DataFrame(np.array(bout_list))
    df2 = pd.concat([df2, dftemp], ignore_index=True, axis=1)
    dftemp2 = pd.DataFrame(np.array(rate_list))
    df3 = pd.concat([df3, dftemp2], ignore_index=True, axis=1)
    dftempmeans = pd.DataFrame(np.array([np.count_nonzero(~np.isnan(col)), len(rate_list), mean_bout_l, mean_rate]))
    df4means = pd.concat([df4means, dftempmeans], ignore_index=True, axis=1)

df2.columns = df.columns
df3.columns = df.columns
df4means.columns = df.columns
df2.to_excel("boutlength.xlsx")
df3.to_excel("lickrate.xlsx")
df4means.to_excel("summarydata.xlsx")

