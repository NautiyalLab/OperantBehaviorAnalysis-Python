from operantanalysis import load_file, extract_info_from_file, reward_retrieval, cue_iti_responding, lever_pressing, \
    lever_press_latency, total_head_pokes, num_successful_go_nogo_trials, count_go_nogo_trials, bin_by_time


def test_load_files():
    (dictionary) = load_file("../operantanalysis/sampledata/!2018-11-27_08h39m.Subject _0001.txt")
    assert "W" in dictionary
    assert "Subject" in dictionary
    assert len(dictionary) == 12
    (dictionary2) = load_file("../operantanalysis/sampledata/!2014-01-31_11h16m.Subject 818.txt")
    assert "W" in dictionary2
    assert "Subject" in dictionary2
    assert len(dictionary2) == 14
    
    
def test_extract_info_from_file():
    (dictionary) = load_file("../operantanalysis/sampledata/!2018-11-27_08h39m.Subject _0001.txt")
    (timecode, eventcode) = extract_info_from_file(dictionary, 500)
    assert len(timecode) == len(eventcode)
    assert all(map(lambda x: x >= 0, timecode))


def test_reward_retrieval():
    assert reward_retrieval([0, 1, 2, 3, 4], ['PokeOn1', 'DipOn', 'DipOff', 'PokeOff1', 'PokeOn1']) == (1, 1, 0)
    assert reward_retrieval([0, 1, 2, 3, 4], ['DipOn', 'PokeOn1', 'DipOff', 'PokeOff1', 'PokeOn1']) == (1, 1, 1)
    assert reward_retrieval([0, 1, 2, 3, 4, 5, 6], ['DipOn', 'PokeOn1', 'PokeOff1', 'PokeOn1', 'DipOff', 'PokeOff1', 'PokeOn1']) == (1, 1, 1)
    assert reward_retrieval([0, 1, 2, 3, 4, 5, 6, 7], ['PokeOn1', 'DipOn', 'DipOff', 'DipOn', 'DipOff', 'PokeOff1', 'PokeOn1', 'PokeOff1']) == (2, 2, 0)


def test_cue_iti_responding():
    assert cue_iti_responding([0, 1, 2, 3, 4, 5], ['StartSession', 'PokeOn1', 'LPressOn', 'PokeOn1', 'RPressOn', 'PokeOn1'], 'LPressOn', 'RPressOn', 'PokeOn1') == (30.0, 30.0)
    assert cue_iti_responding([0, 1, 2, 3, 4, 5], ['StartSession', 'LPressOn', 'PokeOn1', 'PokeOn1', 'RPressOn', 'PokeOn1'], 'LPressOn', 'RPressOn', 'PokeOn1') == (40.0, 0.0)
    assert cue_iti_responding([0, 1, 2, 3, 4, 5], ['StartSession', 'PokeOn1', 'PokeOn1', 'LPressOn', 'RPressOn', 'PokeOn1'], 'LPressOn', 'RPressOn', 'PokeOn1') == (0.0, 60.0)


def test_lever_pressing():
    assert lever_pressing(['StartSession', 'PokeOn1', 'LPressOn', 'PokeOn1', 'RPressOn', 'PokeOn1'], 'LPressOn', 'RPressOn') == (1, 1, 2)
    assert lever_pressing(['StartSession', 'LPressOn', 'PokeOn1', 'PokeOn1', 'RPressOn', 'PokeOn1'], 'LPressOn') == (1, 0, 1)
    assert lever_pressing(['StartSession', 'PokeOn1', 'PokeOn1', 'LPressOn', 'RPressOn', 'RPressOn', 'PokeOn1'], 'LPressOn', 'RPressOn') == (1, 2, 3)


def test_lever_press_latency():
    assert lever_press_latency([0, 1, 2, 3, 4, 5, 6], ['StartSession', 'PokeOn1', 'PokeOn1', 'LPressOn', 'LPressOn', 'RPressOn', 'EndSession'], 'LPressOn', 'RPressOn') == 1
    assert lever_press_latency([0, 1, 2, 3, 4, 5, 6], ['StartSession', 'PokeOn1', 'PokeOn1', 'LPressOn', 'LPressOn', 'PokeOn1', 'EndSession'], 'LPressOn', 'RPressOn') == 0
    assert lever_press_latency([0, 1, 2, 3, 4, 5, 6], ['StartSession', 'PokeOn1', 'PokeOn1', 'LPressOn', 0, 'RPressOn', 'EndSession'], 'LPressOn', 'RPressOn') == 2

    
def test_total_head_pokes():
    assert total_head_pokes(['StartSession', 'PokeOn1', 'LPressOn', 'PokeOn1', 'RPressOn', 'PokeOn1']) == 3
    assert total_head_pokes(['StartSession', 'LPressOn', 'PokeOn1', 'PokeOn1', 'RPressOn', 'PokeOn1']) == 3
    assert total_head_pokes(['StartSession', 'PokeOn1', 'PokeOn1', 'LPressOn', 'RPressOn', 'RPressOn', 'PokeOn1']) == 3


def test_num_successful_go_nogo_trials():
    assert num_successful_go_nogo_trials(['StartSession', 'SuccessfulGoTrial', 'PokeOn1', 'RPressOn', 'PokeOn1']) == (1, 0)
    assert num_successful_go_nogo_trials(['StartSession', 'LPressOn', 'PokeOn1', 'PokeOn1', 'RPressOn', 'PokeOn1']) == (0, 0)
    assert num_successful_go_nogo_trials(['StartSession', 'SuccessfulNoGoTrial', 'SuccessfulNoGoTrial', 'LPressOn', 'RPressOn', 'SuccessfulGoTrial']) == (1, 2)


def test_count_go_nogo_trials():
    assert count_go_nogo_trials(['StartSession', 'PokeOn1', 'LightOn1', 'LightOn1', 'RLeverOn', 'EndSession']) == (1, 0)
    assert count_go_nogo_trials(['StartSession', 'RLeverOn', 'PokeOn1', 'RLeverOn', 'LightOn1', 'RLeverOn', 'LightOn1']) == (1, 2)
    assert count_go_nogo_trials(['StartSession', 'RLeverOn', 'PokeOn1', 'SuccessfulNoGoTrial', 'RLeverOn', 'LightOn1']) == (1, 1)
    
    
def test_bin_by_time():
    assert bin_by_time([0, 1, 2, 3, 4, 5],
                       ['StartSession', 'PokeOn1', 'LPressOn', 'PokeOn1', 'RPressOn', 'PokeOn1'], 1, 'RPressOn') == [0, 0, 0, 0, 1]
    assert bin_by_time([0, 1, 2, 3, 4, 5],
                       ['StartSession', 'LPressOn', 'PokeOn1', 'PokeOn1', 'RPressOn', 'PokeOn1'], 2, 'RPressOn') == [0, 0, 1]
    assert bin_by_time([0, 1, 2, 3, 4, 5],
                       ['StartSession', 'PokeOn1', 'PokeOn1', 'LPressOn', 'RPressOn', 'PokeOn1'], 3, 'RPressOn') == [0, 1]
