from operantanalysis import loop_over_days, extract_info_from_file, lever_pressing, bin_by_time
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt  # noqa

column_list = ['Subject', 'Sex', 'Day', 'Training', 'Lever Presses', 'Bins']


def habit_extinction_function(loaded_file, i):
    """
    :param loaded_file: file output from operant box
    :param i: number of days analyzing
    :return: data frame of all analysis extracted from file (one animal)
    """
    (timecode, eventcode) = extract_info_from_file(loaded_file, 500)
    (left_presses, right_presses, total_presses) = lever_pressing(eventcode, 'LPressOn', 'RPressOn')
    pressing_across_test = bin_by_time(timecode, eventcode, (5 * 60), ['LPressOn', 'RPressOn'])

    df2 = pd.DataFrame([[loaded_file['Subject'], loaded_file['Sex'], int(i + 1), loaded_file['Training'],
                         float(total_presses), pressing_across_test]], columns=column_list)
    bins_df = df2['Bins'].apply(pd.Series)
    bins_df = bins_df.rename(columns=lambda x: (x + 1) * 5)
    df2 = pd.concat([df2[:], bins_df[:]], axis=1)
    return df2


(days, df) = loop_over_days(column_list, habit_extinction_function)

binned_columns = [col for col in df.columns if type(col) == int]

dfnew = pd.melt(df, id_vars=['Subject', 'Sex', 'Day', 'Training', 'Lever Presses'], value_vars=binned_columns,
                var_name='Bin', value_name='Lever_Pressing_During_Bin')
