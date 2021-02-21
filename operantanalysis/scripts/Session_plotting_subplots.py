from operantanalysis import extract_info_from_file, load_file, get_events_indices
import matplotlib

matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

import numpy as np
import tkinter as tk
from tkinter.filedialog import askopenfilename

# opening data file
root = tk.Tk()
root.withdraw()
file = askopenfilename()
loaded_file = load_file(file)

# data transformed into lists of time- and eventcodes
(timecode, eventcode) = extract_info_from_file(loaded_file, 500)

# user input for choosing which events to graph
dip = input("Type 1 if you want to display Dipper values, type 0 otherwise:")
dip = int(dip)
poke = input("Type 1 if you want to display Poke values, type 0 otherwise:")
poke = int(poke)
lever = input("Type 1 if you want to display Lever On/Off values, type 0 otherwise:")
lever = int(lever)
leverpress = input("Type 1 if you want to display Lever Press values, type 0 otherwise:")
leverpress = int(leverpress)

# getting lists of indices for different events
dip_on = get_events_indices(eventcode, ['DipOn'])
dip_off = get_events_indices(eventcode, ['DipOff', 'EndSession'])
poke_on = get_events_indices(eventcode, ['StartTrial'])
poke_off = get_events_indices(eventcode, ['EndTrial', 'EndSession'])
lever_on = get_events_indices(eventcode, ['RLeverOn'])
lever_off = get_events_indices(eventcode, ['RLeverOff', 'EndSession'])
lever_press = get_events_indices(eventcode, ['RPressOn'])

fig, ax = plt.subplots(4)

# plotting different events

subplot = 0

while subplot < 4:
    if dip == 1:
        for i in range(len(dip_on)):
            dip_on_idx = dip_on[i]
            dip_off_idx = dip_off[i]
            # plotting horizontal line for each dip-on/dip-off pair
            ax[subplot].plot([timecode[dip_on_idx], timecode[dip_off_idx]], [4, 4], color='b')
        ax[subplot].plot([timecode[dip_on_idx], timecode[dip_off_idx]], [4, 4], color='b', label='Dipper')

    if poke == 1:
        for i in range(len(poke_on)):
            poke_on_idx = poke_on[i]
            poke_off_idx = poke_off[i]
            # plotting horizontal line for each poke-on/poke-off pair
            ax[subplot].plot([timecode[poke_on_idx], timecode[poke_off_idx]], [3, 3], color='r')
        ax[subplot].plot([timecode[poke_on_idx], timecode[poke_off_idx]], [3, 3], color='r', label='Pokes')

    if lever == 1:
        for i in range(len(lever_on)):
            lever_on_idx = lever_on[i]
            lever_off_idx = lever_off[i]
            # plotting horizontal line for each lever-on/lever-off pair
            ax[subplot].plot([timecode[lever_on_idx], timecode[lever_off_idx]], [2, 2], color='g')
        ax[subplot].plot([timecode[lever_on_idx], timecode[lever_off_idx]], [2, 2], color='g', label='Lever')

    if leverpress == 1:
        for i in range(len(lever_press)):
            lever_press_idx = lever_press[i]
            # scatter plotting for each leverpress
            ax[subplot].scatter(timecode[lever_press_idx], 1, color='m', s=12, marker='.')
        ax[subplot].scatter(timecode[lever_press_idx], 1, color='m', marker='.', s=12, label='Lever Press')
    ax[subplot].set_yticks([])
    subplot += 1

# finding time for end of session
end_session = get_events_indices(eventcode, ['EndSession'])
end_idx = end_session[0]
end = timecode[end_idx]
new_end = end / 4

# defining graph properties
ax[0].set(title='Data Visualization')
ax[3].set(xlabel='Time (sec)')
ax[0].legend()
ax[0].set(xlim=(0, new_end), ylim=(0, 8))
ax[1].set(xlim=(new_end, 2 * new_end), ylim=(0, 8))
ax[2].set(xlim=(2 * new_end, 3 * new_end), ylim=(0, 8))
ax[3].set(xlim=(3 * new_end, end), ylim=(0, 8))
fig.set_size_inches(20, 10)
fig.savefig('pythonplot3.png')  # saving figure as image
plt.show()  # showing figure
