from operantanalysis import load_file, extract_info_from_file, get_events_indices, closest

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

import os
import glob
from tkinter import filedialog
from tkinter import *  # noqa

total_closest_cue_list = []

root = Tk()  # noqa
root.withdraw()
folder_selected = filedialog.askdirectory()
file_pattern = os.path.join(folder_selected, '*')
for file in sorted(glob.glob(file_pattern)):
    loaded_file = load_file(file)

    (timecode, eventcode) = extract_info_from_file(loaded_file, 500)
    reward = get_events_indices(eventcode, ['DipOn'])
    cue = get_events_indices(eventcode, ['StartTrial'])
    cuetimecodes = [timecode[code] for code in cue]
    for event in reward:
        closestcue = closest(cuetimecodes, timecode[event])
        total_closest_cue_list += [timecode[event]-closestcue]

plt.hist(total_closest_cue_list, 20)
plt.show()
