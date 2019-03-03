from operantanalysis import load_file, extract_info_from_file,  reward_retrieval, cue_iti_responding, lever_pressing, lever_press_latency


def test_load_files():
    (dictionary) = load_file("../operantanalysis/sampledata/!2018-11-27_08h39m.Subject _0001.txt")
    assert "W" in dictionary
    assert "Subject" in dictionary
    assert len(dictionary) == 12
    
    
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
    assert cue_iti_responding([0, 1, 2, 3, 4, 5], ['StartSession', 'PokeOn1', 'LPressOn', 'PokeOn1', 'RPressOn', 'PokeOn1'], 'LPressOn', 'RPressOn') == (30.0, 30.0)
    assert cue_iti_responding([0, 1, 2, 3, 4, 5], ['StartSession', 'LPressOn', 'PokeOn1', 'PokeOn1', 'RPressOn', 'PokeOn1'], 'LPressOn', 'RPressOn') == (40.0, 0.0)
    assert cue_iti_responding([0, 1, 2, 3, 4, 5], ['StartSession', 'PokeOn1', 'PokeOn1', 'LPressOn', 'RPressOn', 'PokeOn1'], 'LPressOn', 'RPressOn') == (0.0, 60.0)


def test_lever_pressing():
    assert lever_pressing(['StartSession', 'PokeOn1', 'LPressOn', 'PokeOn1', 'RPressOn', 'PokeOn1'], 'LPressOn', 'RPressOn') == (1, 1, 2)
    assert lever_pressing(['StartSession', 'LPressOn', 'PokeOn1', 'PokeOn1', 'RPressOn', 'PokeOn1'], 'LPressOn') == (1, 0, 1)
    assert lever_pressing(['StartSession', 'PokeOn1', 'PokeOn1', 'LPressOn', 'RPressOn', 'RPressOn', 'PokeOn1'], 'LPressOn', 'RPressOn') == (1, 2, 3)


def test_lever_press_latency():
    assert lever_press_latency([0, 1, 2, 3, 4, 5, 6], ['StartSession', 'PokeOn1', 'PokeOn1', 'LPressOn', 'LPressOn', 'RPressOn', 'EndSession'], 'LPressOn', 'RPressOn') == 1
    assert lever_press_latency([0, 1, 2, 3, 4, 5, 6], ['StartSession', 'PokeOn1', 'PokeOn1', 'LPressOn', 'LPressOn', 'PokeOn1', 'EndSession'], 'LPressOn', 'RPressOn') == "No presses"
    assert lever_press_latency([0, 1, 2, 3, 4, 5, 6], ['StartSession', 'PokeOn1', 'PokeOn1', 'LPressOn', 0, 'RPressOn', 'EndSession'], 'LPressOn', 'RPressOn') == 2
