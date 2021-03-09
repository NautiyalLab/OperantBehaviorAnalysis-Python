from operantanalysis import loop_over_days, extract_info_from_file, lever_pressing
import pandas as pd

column_list = ['Subject', 'Day', 'CS+ Lever Presses', 'CS- Lever Presses']


def PIT_test_function(loaded_file, i):
    """
    :param loaded_file: file output from operant box
    :param i: number of days analyzing
    :return: data frame of all analysis extracted from file (one animal)
    """
    (timecode, eventcode) = extract_info_from_file(loaded_file, 500)
    (csplus_presses, csmin_presses, total_presses) = lever_pressing(eventcode, 'ActivePress', 'InactivePress')

    df2 = pd.DataFrame([[loaded_file['Subject'], int(i + 1), float(csplus_presses), float(csmin_presses)]], columns=column_list)

    return df2


(days, df) = loop_over_days(column_list, PIT_test_function)
print(df.to_string())
df.to_excel("output.xlsx")