from operantanalysis import loop_over_days, extract_info_from_file, lever_pressing, cue_iti_responding, cue_responding_duration
import pandas as pd

column_list = ['Subject', 'Day', 'CS+ Lever+ Presses RPM', 'CS+ Lever- Presses RPM', 'CS- Lever+ PressesRPM',
               'CS- Lever- Presses RPM', 'ITI Lever+ Presses RPM', 'ITI Lever- PressesRPM', 'CS+ Poke RPM',
               'CS- Poke RPM', 'ITI Poke RPM', 'CS+ Poke Dur', 'CS- Poke Dur', 'ITI Poke Dur']


def RealPIT_test_function(loaded_file, i):
    """
    :param loaded_file: file output from operant box
    :param i: number of days analyzing
    :return: data frame of all analysis extracted from file (one animal)
    """
    (timecode, eventcode) = extract_info_from_file(loaded_file, 500)
    (cspluslevplus_presses, cspluslevmin_presses, CSPlustotal_presses) = lever_pressing(eventcode, 'ActivePress', 'InactivePress')
    (ITIlevplus_presses, ITIlevmin_presses, ITItotal_presses) = lever_pressing(eventcode, 'LPressOff', 'RPressOff')
    (csminlevplus_presses, csminlevmin_presses, CSMintotal_presses) = lever_pressing(eventcode, 'LPressOn', 'RPressOn')
    (A_responding, A_iti) = cue_iti_responding(timecode, eventcode, 'ExcitorATrialStart', 'ExcitorATrialEnd', 'PokeOn1')
    (B_responding, B_iti) = cue_iti_responding(timecode, eventcode, 'ExcitorBTrialStart', 'ExcitorBTrialEnd', 'PokeOn1')
    (A_dur_individual, A_dur_total, AITI_dur_individual, AITI_dur_total) = cue_responding_duration(timecode, eventcode,
                                                                                                   'ExcitorATrialStart',
                                                                                                   'ExcitorATrialEnd',
                                                                                                   'PokeOn1',
                                                                                                   'PokeOff1')
    (B_dur_individual, B_dur_total, BITI_dur_individual, BITI_dur_total) = cue_responding_duration(timecode, eventcode,
                                                                                                   'ExcitorBTrialStart',
                                                                                                   'ExcitorBTrialEnd',
                                                                                                   'PokeOn1',
                                                                                                   'PokeOff1')


    df2 = pd.DataFrame([[loaded_file['Subject'], int(i + 1), float(cspluslevplus_presses)/10, float(cspluslevmin_presses)/10,
                         float(csminlevplus_presses)/10, float(csminlevmin_presses)/10,
                         float(ITIlevplus_presses)/20, float(ITIlevmin_presses)/20, float(A_responding),
                         float(B_responding), (float(A_iti)+float(B_iti))/2, float(A_dur_total),
                         float(B_dur_total), (float(AITI_dur_total)+float(BITI_dur_total))/2]]
                       , columns=column_list)
    # numbers in divisors are number of trials so you end up with rpm

    return df2


(days, df) = loop_over_days(column_list, RealPIT_test_function)
print(df.to_string())
df.to_excel("output.xlsx")