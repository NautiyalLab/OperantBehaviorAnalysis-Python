from operantanalysis import loop_over_days, extract_info_from_file, reward_retrieval, \
    cue_iti_responding
import pandas as pd


column_list = ['Subject', 'Day', 'Dippers', 'Inactive Poke Rate', 'Inactive Press Rate', 'Active Poke Rate',
               'Active Press Rate']


def signtracking(loaded_file, i):
    """
    :param loaded_file: file output from operant box
    :param i: number of days analyzing
    :return: data frame of all analysis extracted from file (one animal)
    """
    (timecode, eventcode) = extract_info_from_file(loaded_file, 500)
    (dippers, dippers_retrieved, retrieval_latency) = reward_retrieval(timecode, eventcode)
    (inactive_poke, inactive_iti_poke) = cue_iti_responding(timecode, eventcode, 'NoRewardTrialStart', 'NoRewardTrialEnd', 'PokeOn1')
    (inactive_press, inactive_iti_press) = cue_iti_responding(timecode, eventcode, 'NoRewardTrialStart', 'NoRewardTrialEnd', 'InactivePress')
    (active_poke, active_iti_poke) = cue_iti_responding(timecode, eventcode, 'RewardTrialStart', 'RewardTrialEnd', 'PokeOn1')
    (active_press, active_iti_press) = cue_iti_responding(timecode, eventcode, 'RewardTrialStart', 'RewardTrialEnd', 'ActivePress')

    df2 = pd.DataFrame([[loaded_file['Subject'], int(i + 1), float(dippers), float(inactive_poke),
                         float(inactive_press), float(active_poke), float(active_press)]],
                       columns=column_list)

    return df2


(days, df) = loop_over_days(column_list, signtracking)
print(df.to_string())
df.to_excel("output.xlsx")
