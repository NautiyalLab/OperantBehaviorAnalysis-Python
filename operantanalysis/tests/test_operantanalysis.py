from operantanalysis import load_file, reward_retrieval, cue_iti_responding, lever_pressing


def test_load_files():
    (subject_number, timecode, eventcode) = load_file("../operantanalysis/sampledata/!2018-11-27_08h39m.Subject _0001.txt")
    assert len(timecode) == len(eventcode)
    assert all(map(lambda x: x >= 0, timecode))
    assert all(map(lambda x: x >= 0, eventcode))


def test_reward_retrieval():
    assert reward_retrieval([0, 1, 2, 3, 4], [1011, 25, 26, 1001, 1011]) == (1, 1, 0)
    assert reward_retrieval([0, 1, 2, 3, 4], [25, 1011, 26, 1001, 1011]) == (1, 1, 1)
    assert reward_retrieval([0, 1, 2, 3, 4, 5, 6], [25, 1011, 1001, 1011, 26, 1001, 1011]) == (1, 1, 1)
    assert rreward_retrieval([0, 1, 2, 3, 4, 5, 6, 7], [1011, 25, 26, 25, 26, 1001, 1011, 1001]) == (2, 2, 0)


def test_cue_iti_responding():
    assert cue_iti_responding([0, 1, 2, 3, 4, 5], [113, 1011, 1, 1011, 2, 1011], 1, 2) == (30.0, 30.0)
    assert cue_iti_responding([0, 1, 2, 3, 4, 5], [113, 1, 1011, 1011, 2, 1011], 1, 2) == (40.0, 0.0)
    assert cue_iti_responding([0, 1, 2, 3, 4, 5], [113, 1011, 1011, 1, 2, 1011], 1, 2) == (0.0, 60.0)

    
def test_lever_pressing():
    assert lever_pressing([113, 1011, 1, 1011, 2, 1011], 1, 2) == (1, 1, 2)
    assert lever_pressing([113, 1, 1011, 1011, 2, 1011], 1) == (1, 0, 1)
    assert lever_pressing([113, 1011, 1011, 1, 2, 2, 1011], 1, 2) == (1, 2, 3)
