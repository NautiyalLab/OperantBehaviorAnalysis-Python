import statistics
__all__ = ["accessfiles", "rewardretrieval", "respondingduringcueanditi", "leverpressing"]


def accessfiles(filename):
    """

    :param filename: string that refers to operant file location, file is txt
    :return: subject number, list of time codes, and list of eventcodes
    """
    with open(filename, "r") as fileref:
        filestring = fileref.read()

    subjectlocation = filestring.index('Subject:')
    subjectnumber = filestring[subjectlocation + 9:subjectlocation + 15]

    warraybegin = filestring.index('W:')
    timeeventcodes = filestring[warraybegin + 1:].split()[2:]

    for num in timeeventcodes:
        if ':' in num:
            timeeventcodes.remove(num)

    timecode = []
    eventcode = []
    firsttimecode = (float(timeeventcodes[0][:-6]) / 500)

    for num in timeeventcodes:
        if num == timeeventcodes[0]:
            timecode += [0.0]
        else:
            timecode += [round((float(num[:-6]) / 500) - firsttimecode, 2)]
        eventcode += [int(num[-6:-2])]

    return subjectnumber, timecode, eventcode


def rewardretrieval(timecode, eventcode):
    """

    :param timecode: list of time codes from operant conditioning file
    :param eventcode: list of event codes from operant conditioning file
    :return: number of reinforcers (dippers) presented, number retrieved, and latency to retrieve as floats
    """
    dipperon = [i for i, event in enumerate(eventcode) if event == 25]
    dipperoff = [i for i, event in enumerate(eventcode) if event == 26]
    pokeon = [i for i, event in enumerate(eventcode) if event == 1011]
    pokeoff = [i for i, event in enumerate(eventcode) if event == 1001]
    dippersretrieved = 0
    latencytoretrievedipper = []

    for i in range(len(dipperon)):
        for x in range(len(pokeoff)):
            diponidx = dipperon[i]
            dipoffidx = dipperoff[i]
            if pokeon[x] < diponidx < pokeoff[x]:
                dippersretrieved += 1
                latencytoretrievedipper += [0]
                break
            elif 1011 in eventcode[diponidx:dipoffidx]:
                dippersretrieved += 1
                pokewhilediponidx = eventcode[diponidx:dipoffidx].index(1011)
                latencytoretrievedipper += [round(timecode[pokewhilediponidx + diponidx] - timecode[diponidx], 2)]
                break
    return len(dipperon), dippersretrieved, round(statistics.mean(latencytoretrievedipper), 3)


def respondingduringcueanditi(timecode, eventcode, codeon, codeoff):
    """

    :param timecode: list of time codes from operant conditioning file
    :param eventcode: list of event codes from operant conditioning file
    :param codeon: event code for the beginning of a cue
    :param codeoff: event code for the end of a cue
    :return: mean rpm of head pokes during cue and mean rpm of head pokes during equivalent ITI preceding cue
    """
    cueon = [i for i, event in enumerate(eventcode) if event == codeon]
    cueoff = [i for i, event in enumerate(eventcode) if event == codeoff]
    ition = [i for i, event in enumerate(eventcode) if event == codeoff or event == 113]
    allpokerpm = []
    allpokeitirpm = []

    for i in range(len(cueon)):
        cueonidx = cueon[i]
        cueoffidx = cueoff[i]
        itionidx = ition[i]
        cuelengthsec = (timecode[cueoffidx] - timecode[cueonidx])
        pokerpm = ((eventcode[cueonidx:cueoffidx].count(1011)) / (cuelengthsec / 60))
        allpokerpm += [pokerpm]
        itipoke = 0
        for x in range(itionidx, cueonidx):
            if eventcode[x] == 1011 and timecode[x] >= (timecode[cueonidx] - cuelengthsec):
                itipoke += 1
        itipokerpm = itipoke / (cuelengthsec / 60)
        allpokeitirpm += [itipokerpm]
    
    return round(statistics.mean(allpokerpm), 3), round(statistics.mean(allpokeitirpm), 3)


def leverpressing(eventcode, lever1, lever2=False):
    lever1presses = eventcode.count(lever1)
    if bool(lever2):
        lever2presses = eventcode.count(lever2)
    else:
        lever2presses = 0
    totalleverpresses = lever1presses + lever2presses

    return lever1presses, lever2presses, totalleverpresses
