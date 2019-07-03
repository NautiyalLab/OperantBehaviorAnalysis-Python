from operantanalysis import DNAMIC_loop_over_days, bin_by_time
import pandas as pd

column_list = ['Subject', 'Day', 'Left Pokes', 'RightPokes', 'Middle Pokes', 'Total Pokes']


def DNAMIC_function(eventcode, timecode, fields_dictionary, i):
    """
    :param loaded_file: file output from operant box
    :param i: number of days analyzing
    :return: data frame of all analysis extracted from file (one animal)
    """
    left_count = bin_by_time(timecode, eventcode, 3600, ['LPokeOn'])
    right_count = bin_by_time(timecode, eventcode, 3600, ['RPokeOn'])
    middle_count = bin_by_time(timecode, eventcode, 3600, ['MPokeOn'])
    total_count = bin_by_time(timecode, eventcode, 3600, ['LPokeOn', 'RPokeOn', 'MPokeOn'])
    print(sum(total_count))

    df2 = pd.DataFrame([[fields_dictionary['Subject'], int(i + 1), left_count, right_count, middle_count,
                         total_count]], columns=column_list)

    return df2


(days, df) = DNAMIC_loop_over_days(column_list, DNAMIC_function)
df.to_excel("output.xlsx")

print(df.to_string())
