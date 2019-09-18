import numpy as np
import os
import glob
from tkinter import filedialog
from tkinter import *  # noqa
import pandas as pd

root = Tk()  # noqa
root.withdraw()
folder_selected = filedialog.askdirectory()
file_pattern = os.path.join(folder_selected, '*')

for file in sorted(glob.glob(file_pattern)):
    df = pd.read_csv(file)
df.rename(columns=df.iloc[0]).drop(df.index[0])

df2 = pd.DataFrame()

for colname, col in df.iteritems():
    bout_list = []
    bout = 0
    for x in col:
        if x <= 1000:
            bout += x
        elif x > 1000:
            bout_list += [bout]
            bout = 0
    dftemp = pd.DataFrame(np.array(bout_list))
    df2 = pd.concat([df2, dftemp], ignore_index=True, axis=1)

df2.columns = df.columns
df2.to_excel("output.xlsx")
