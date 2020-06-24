from operantanalysis import loop_over_days, extract_info_from_file, RVI_nogo_latency, RVI_gng_weird
import pandas as pd


column_list = ['Subject', 'Day', 'Small Go Trials', 'Large Go Trials', 'Successful Small Go Trials',
               'Successful Large Go Trials', 'Small Go Latency', 'Large Go Latency', 'Small No Go Trials',
               'Large No Go Trials', 'Successful Small No Go Trials',
               'Successful Large No Go Trials', 'Small No Go Latency', 'Large No Go Latency',
               'Incorrect Trials Small', 'Incorrect Trials Large']


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
    (small_go_latency, incorrect_trials_small) = RVI_gng_weird(timecode, eventcode, 'GoTrialBegSmallReward', 'GoTrialSuccessSmallReward', 5)
    (large_go_latency, incorrect_trials_large) = RVI_gng_weird(timecode, eventcode, 'GoTrialBegLargeReward', 'GoTrialSuccessLargeReward', 5)
    small_nogo_latency = RVI_nogo_latency(timecode, eventcode, 'NoGoTrialBegSmallReward', 5)
    large_nogo_latency = RVI_nogo_latency(timecode, eventcode, 'NoGoTrialBegLargeReward', 5)

    df2 = pd.DataFrame([[loaded_file['Subject'], int(i + 1), float(small_go_trials), float(large_go_trials),
                         float(small_go_success - incorrect_trials_small),
                         float(large_go_success - incorrect_trials_large),
                         float(small_go_latency), float(large_go_latency),
                         float(small_no_go_trials - incorrect_trials_small),
                         float(large_no_go_trials - incorrect_trials_large), float(small_no_go_success),
                         float(large_no_go_success), float(small_nogo_latency), float(large_nogo_latency),
                         float(incorrect_trials_small), float(incorrect_trials_large)]],
                       columns=column_list)

    return df2


(days, df) = loop_over_days(column_list, RVI_Go_NoGo_P2)
print(df.to_string())
df.to_excel("output.xlsx")
