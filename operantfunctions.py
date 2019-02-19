import statistics


def accessfiles(filename):
    fileref = open(filename, "r")
    filestring = fileref.read()
    fileref.close()

    subjectlocation = filestring.index('Subject:')
    subjectnumber = filestring[subjectlocation+9:subjectlocation+15]

    warraybegin = filestring.index('W:')
    timeeventcodes = filestring[warraybegin+1:].split()[2:]

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
    dipperon = [i for i in range(len(eventcode)) if eventcode[i] == 25]
    dipperoff = [i for i in range(len(eventcode)) if eventcode[i] == 26]
    pokeon = [i for i in range(len(eventcode)) if eventcode[i] == 1011]
    pokeoff = [i for i in range(len(eventcode)) if eventcode[i] == 1001]

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
                
    return dippersretrieved, round(statistics.mean(latencytoretrievedipper), 3)
