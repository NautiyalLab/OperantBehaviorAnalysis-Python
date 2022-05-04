from operantanalysis import loop_over_days, extract_info_from_file, reward_retrieval, \
    cue_iti_responding_PavCA, lever_press_latency_PavCA
import pandas as pd


column_list = ['Subject', 'Day', 'Dippers', 'ITI Poke Rate', 'Poke Rate', 'Press Rate', 'Prob Poke', 'Prob Press', 'Poke Latency', 'Press Latency']


def pavCA(loaded_file, i):
    """
    :param loaded_file: file output from operant box
    :param i: number of days analyzing
    :return: data frame of all analysis extracted from file (one animal)
    """
    (timecode, eventcode) = extract_info_from_file(loaded_file, 500)
    (dippers, dippers_retrieved, retrieval_latency) = reward_retrieval(timecode, eventcode)
    if loaded_file['MSN'] == 'PavCA_LeftUnpaired_2020' or loaded_file['MSN'] == 'PavCA_RightUnpaired_2020':
        (inactive_poke, inactive_iti_poke, trials_w_poke) = cue_iti_responding_PavCA(timecode, eventcode, 'NoRewardTrialStart', 'NoRewardTrialEnd', 'PokeOn1')
        (inactive_press, inactive_iti_press, trials_w_press) = cue_iti_responding_PavCA(timecode, eventcode, 'NoRewardTrialStart', 'NoRewardTrialEnd', 'InactivePress')
        poke_lat = lever_press_latency_PavCA(timecode, eventcode, 'NoRewardTrialStart', 'PokeOn1', 10)
        press_lat = lever_press_latency_PavCA(timecode, eventcode, 'NoRewardTrialStart', 'InactivePress', 10)
        poke = inactive_poke
        press = inactive_press
        prob_poke = trials_w_poke / 35
        prob_press = trials_w_press / 35
        iti_poke = inactive_iti_poke
    elif loaded_file['MSN'] == 'PavCA_LeftPaired_2020' or loaded_file['MSN'] == 'PavCA_RightPaired_2020':
        (active_poke, active_iti_poke, trials_w_poke) = cue_iti_responding_PavCA(timecode, eventcode, 'RewardTrialStart', 'RewardTrialEnd', 'PokeOn1')
        (active_press, active_iti_press, trials_w_press) = cue_iti_responding_PavCA(timecode, eventcode, 'RewardTrialStart', 'RewardTrialEnd', 'ActivePress')
        poke_lat = lever_press_latency_PavCA(timecode, eventcode, 'RewardTrialStart', 'PokeOn1', 10)
        press_lat = lever_press_latency_PavCA(timecode, eventcode, 'RewardTrialStart', 'ActivePress', 10)
        poke = active_poke
        press = active_press
        prob_poke = trials_w_poke / 35
        prob_press = trials_w_press / 35
        iti_poke = active_iti_poke
    df2 = pd.DataFrame([[loaded_file['Subject'], int(i + 1), float(dippers), float(iti_poke), float(poke),
                         float(press), float(prob_poke), float(prob_press), float(poke_lat), float(press_lat)]],
                       columns=column_list)

    return df2


(days, df) = loop_over_days(column_list, pavCA)
print(df.to_string())
df.to_excel("output.xlsx")
