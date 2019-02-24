import statistics
from operantanalysis import accessfiles, rewardretrieval, respondingduringcueanditi


def test_accessfiles():
    (subjectnumber, timecode, eventcode) = accessfiles(
        "/Users/stephanie/Documents/MatLab/OC1/PCER - 11-27-18/!2018-11-27_08h39m.Subject _0001.txt")
    assert len(timecode) == len(eventcode)
    for i in timecode:
        assert bool(i >= 0)
    for i in eventcode:
        assert bool(i >= 0)


def test_rewardretrieval():
    assert rewardretrieval([0, 1, 2, 3, 4], [1011, 25, 26, 1001, 1011]) == (1, 1, 0)
    assert rewardretrieval([0, 1, 2, 3, 4], [25, 1011, 26, 1001, 1011]) == (1, 1, 1)
    assert rewardretrieval([0, 1, 2, 3, 4, 5, 6], [25, 1011, 1001, 1011, 26, 1001, 1011]) == (1, 1, 1)
    assert rewardretrieval([0, 1, 2, 3, 4, 5, 6, 7], [1011, 25, 26, 25, 26, 1001, 1011, 1001]) == (2, 2, 0)


def test_respondingduringcueanditi():
    assert respondingduringcueanditi([0, 1, 2, 3, 4, 5], [113, 1011, 1, 1011, 2, 1011], 1, 2) == (30.0, 30.0)
    assert respondingduringcueanditi([0, 1, 2, 3, 4, 5], [113, 1, 1011, 1011, 2, 1011], 1, 2) == (40.0, 0.0)
    assert respondingduringcueanditi([0, 1, 2, 3, 4, 5], [113, 1011, 1011, 1, 2, 1011], 1, 2) == (0.0, 60.0)
