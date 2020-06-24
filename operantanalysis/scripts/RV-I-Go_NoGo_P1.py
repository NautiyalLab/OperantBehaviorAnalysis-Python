from operantanalysis import loop_over_days, extract_info_from_file, lever_press_latency
import pandas as pd


column_list = ['Subject', 'Day', 'Small Go Trials', 'Large Go Trials', 'Successful Small Go Trials',
               'Successful Large Go Trials', 'Small Go Latency', 'Large Go Latency']


def RVI_Go_NoGo_P1(loaded_file, i):
    """
    :param loaded_file: file output from operant box
    :param i: number of days analyzing
    :return: data frame of all analysis extracted from file (one animal)
    """
    (timecode, eventcode) = extract_info_from_file(loaded_file, 500)
    (small_go_trials, large_go_trials, small_go_success, large_go_success) = (eventcode.count('GoTrialBegSmallReward'),
                                                                              eventcode.count('GoTrialBegLargeReward'),
                                                                              eventcode.count('GoTrialSuccessSmallReward'),
                                                                              eventcode.count('GoTrialSuccessLargeReward'))
    small_go_latency = lever_press_latency(timecode, eventcode, 'GoTrialBegSmallReward', 'GoTrialSuccessSmallReward')
    large_go_latency = lever_press_latency(timecode, eventcode, 'GoTrialBegLargeReward', 'GoTrialSuccessLargeReward')

    df2 = pd.DataFrame([[loaded_file['Subject'], int(i + 1), float(small_go_trials), float(large_go_trials),
                         float(small_go_success), float(large_go_success), float(small_go_latency),
                         float(large_go_latency)]],
                       columns=column_list)

    return df2


(days, df) = loop_over_days(column_list, RVI_Go_NoGo_P1)
print(df.to_string())
df.to_excel("output.xlsx")
