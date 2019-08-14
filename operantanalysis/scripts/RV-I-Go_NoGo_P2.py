from operantanalysis import loop_over_days, extract_info_from_file, lever_press_lat_gng, RVI_gng_weird
import pandas as pd


column_list = ['Subject', 'Day', 'Small Go Trials', 'Large Go Trials', 'Successful Small Go Trials',
               'Successful Large Go Trials', 'Small Go Latency', 'Large Go Latency', 'Small No Go Trials',
               'Large No Go Trials', 'Successful Small No Go Trials',
               'Successful Large No Go Trials', 'Incorrect Trials']


def RVI_Go_NoGo_P2(loaded_file, i):
    """
    :param loaded_file: file output from operant box
    :param i: number of days analyzing
    :return: data frame of all analysis extracted from file (one animal)
    """
    (timecode, eventcode) = extract_info_from_file(loaded_file, 500)
    (small_go_trials, large_go_trials, small_go_success, large_go_success, small_no_go_trials, large_no_go_trials,
     small_no_go_success, large_no_go_success) = (eventcode.count('GoTrialBegSmallReward'),
                                                  eventcode.count('GoTrialBegLargeReward'),
                                                  eventcode.count('GoTrialSuccessSmallReward'),
                                                  eventcode.count('GoTrialSuccessLargeReward'),
                                                  eventcode.count('NoGoTrialBegSmallReward'),
                                                  eventcode.count('NoGoTrialBegLargeReward'),
                                                  eventcode.count('NoGoTrialSuccessSmallReward'),
                                                  eventcode.count('NoGoTrialSuccessLargeReward'))
    (small_go_latency, incorrect_trials) = RVI_gng_weird(timecode, eventcode, 'GoTrialBegSmallReward', 'GoTrialSuccessSmallReward')
    large_go_latency = lever_press_lat_gng(timecode, eventcode, 'GoTrialBegLargeReward', 'GoTrialSuccessLargeReward')

    df2 = pd.DataFrame([[loaded_file['Subject'], int(i + 1), float(small_go_trials), float(large_go_trials),
                         float(small_go_success - incorrect_trials), float(large_go_success), float(small_go_latency),
                         float(large_go_latency), float(small_no_go_trials - incorrect_trials),
                         float(large_no_go_trials), float(small_no_go_success), float(large_no_go_success),
                         float(incorrect_trials)]],
                       columns=column_list)

    return df2


(days, df) = loop_over_days(column_list, RVI_Go_NoGo_P2)
print(df.to_string())
df.to_excel("output.xlsx")

group_means = df.groupby(['Day'])['Successful Small Go Trials', 'Successful Large Go Trials', 'Small Go Latency',
                                  'Large Go Latency', 'Successful Small No Go Trials',
                                  'Successful Large No Go Trials'].mean()
group_sems = df.groupby(['Day'])['Successful Small Go Trials', 'Successful Large Go Trials', 'Small Go Latency',
                                 'Large Go Latency', 'Successful Small No Go Trials',
                                 'Successful Large No Go Trials'].sem()

print(df.groupby(['Day'])['Successful Small Go Trials', 'Successful Large Go Trials', 'Small Go Latency',
                          'Large Go Latency', 'Successful Small No Go Trials',
                          'Successful Large No Go Trials'].mean().unstack().to_string())
print(df.groupby(['Day'])['Successful Small Go Trials', 'Successful Large Go Trials', 'Small Go Latency',
                          'Large Go Latency', 'Successful Small No Go Trials',
                          'Successful Large No Go Trials'].sem().unstack().to_string())
