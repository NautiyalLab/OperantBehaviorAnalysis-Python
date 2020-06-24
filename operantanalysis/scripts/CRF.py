from operantanalysis import loop_over_days, extract_info_from_file, reward_retrieval, lever_pressing
#    lever_press_latency, cue_iti_responding
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt  # noqa

column_list = ['Subject', 'Day', 'Dippers', 'Dippers Retrieved', 'Retrieval Latency',
               'Left Lever Presses', 'Right Lever Presses', 'Total Presses']


def crf_function(loaded_file, i):
    """
    :param loaded_file: file output from operant box
    :param i: number of days analyzing
    :return: data frame of all analysis extracted from file (one animal)
    """
    (timecode, eventcode) = extract_info_from_file(loaded_file, 500)
    (dippers, dippers_retrieved, retrieval_latency) = reward_retrieval(timecode, eventcode)
    (left_presses, right_presses, total_presses) = lever_pressing(eventcode, 'LPressOn', 'RPressOn')

#    Use this code for latencies and rates
#
#    if 'LLeverOn' in eventcode:
#        press_latency = lever_press_latency(timecode, eventcode, 'LLeverOn', 'LPressOn')
#        (lever_press_rate, iti_rate) = cue_iti_responding(timecode, eventcode, 'StartSession', 'EndSession', 'LPressOn')
#    elif 'RLeverOn' in eventcode:
#        press_latency = lever_press_latency(timecode, eventcode, 'RLeverOn', 'RPressOn')
#        (lever_press_rate, iti_rate) = cue_iti_responding(timecode, eventcode, 'StartSession', 'EndSession', 'RPressOn')
        
    df2 = pd.DataFrame([[loaded_file['Subject'], int(i + 1), float(dippers),
                         float(dippers_retrieved), float(retrieval_latency), float(left_presses),
                         float(right_presses), float(total_presses)]], columns=column_list)
    
    return df2


(days, df) = loop_over_days(column_list, crf_function)
print(df.to_string())
df.to_excel("output.xlsx")
