from operantanalysis import concat_lickometer_files
import numpy as np
import pandas as pd
import math

days = int(input("How many days would you like to analyze?"))

df = pd.DataFrame()

for i in range(days):
        
    lick_df = concat_lickometer_files()

    df2 = pd.DataFrame()
    df3 = pd.DataFrame()
    df4means = pd.DataFrame()

    for colname, col in lick_df.iteritems():
        bout_list = []
        rate_list = []
        bout = 0
        lick_count = 0
        x2 = 0
        nan = 0
        totaltime = -col[0]
        lick_count_2 = 0
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
            totaltime += x
            if totaltime <= 120000:
                lick_count_2 += 1
        if len(rate_list) == 0:
            mean_bout_l = 0
            mean_rate = 0
        else:
            mean_bout_l = sum(bout_list)/len(rate_list)
            mean_rate = sum(rate_list)/len(rate_list)
        lick_rate_2min = lick_count_2 / 120000
        dftemp = pd.DataFrame(np.array(bout_list))
        df2 = pd.concat([df2, dftemp], ignore_index=True, axis=1)
        dftemp2 = pd.DataFrame(np.array(rate_list))
        df3 = pd.concat([df3, dftemp2], ignore_index=True, axis=1)
        dftempmeans = pd.DataFrame(np.array([np.count_nonzero(~np.isnan(col)), len(rate_list), mean_bout_l, mean_rate, lick_rate_2min]))
        df4means = pd.concat([df4means, dftempmeans], ignore_index=True, axis=1)

    df2.columns = lick_df.columns
    df3.columns = lick_df.columns
    df4means.columns = lick_df.columns
    df4means = df4means.transpose()
    df4means.columns = ['Total Licks', 'Total Bouts', 'Bout Length', 'Lick Rate', 'Lick Rate 2 min']
    df = df.append(df4means)

df.to_excel("summarydata.xlsx")
