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

# user input for how many events of each type (On/Off and discrete) to plot
long_events = input("How many behavioral On/Off events do you want to show?")
long_events = int(long_events)
short_events = input("How many discrete events would you like to show?")
short_events = int(short_events)

fig, ax = plt.subplots()

y = 1

# for-loop plotting On/Off events
for a in range(0, long_events):
    # user input for correct event title, then getting list of indices for event
    event1 = input(
        "Type the correct event title for a longer event turning ""On"" as written in the eventcodes dictionary (eg. DipOn):")
    on = get_events_indices(eventcode, [event1])
    event2 = input(
        "Type the correct event title for a longer event turning ""Off"" as written in the eventcodes dictionary (eg. DipOff):")
    eventlabel = input("What do you want to label this longer event (eg. Dipper):")
    off = get_events_indices(eventcode, [event2, 'EndSession'])
    # randomizing color for plotting of event
    r = np.random.random()
    b = np.random.random()
    g = np.random.random()
    col = (r, g, b)
    for i in range(len(on)):
        on_idx = on[i]
        off_idx = off[i]
        # plotting horizontal line for each On/Off pair
        ax.plot([timecode[on_idx], timecode[off_idx]], [y, y], color=col)
    ax.plot([timecode[on_idx], timecode[off_idx]], [y, y], color=col, label=eventlabel)
    y += 1

# for-loop potting discrete events
for b in range(0, short_events):
    # user input for correct event title, then getting list of indices for event
    event = input(
        "Type the correct event title of the discrete event as written in the eventcodes dictionary (eg. RPressOn):")
    on = get_events_indices(eventcode, [event])
    eventlabel = input("What do you want to label this discrete event (eg. Lever Press):")
    # randomizing color for plotting of event
    r = np.random.random()
    b = np.random.random()
    g = np.random.random()
    col = (r, g, b)
    for i in range(len(on)):
        on_idx = on[i]
        # scatter plotting for each occurence of discrete event
        ax.scatter(timecode[on_idx], y, color=col, s=12, marker='.')
    ax.scatter(timecode[on_idx], y, color=col, marker='.', s=12, label=eventlabel)
    y += 1

y += 2

# finding time for end of session
end_session = get_events_indices(eventcode, ['EndSession'])
end_idx = end_session[0]
end = timecode[end_idx]

# defining graph properties
ax.legend()
ax.set(xlabel='Time (sec)', title='Data Visualization')
ax.set(xlim=(0, end), ylim=(0, y))
ax.set_yticks([])
fig.set_size_inches(20, 10)
fig.savefig('pythonplot2.png')  # saving figure as image
plt.show()  # showing figure
