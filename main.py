import re
from math import ceil

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# TODO: create function for storing and retrieving stats from TinyDB and graphing on that instead
# TODO: implement the ability to import any/all cstimer exports in the directory, without creating dupes in TinyDB


def find_wca_avg(list_of_times):
    """
    Get WCA average (drop fastest and slowest, get mean) from any list of times
    """
    truncated_list = [i for i in list_of_times if min(list_of_times) < i < max(list_of_times)]
    tlist_mean = np.mean(truncated_list)
    return tlist_mean


def avg_over_x(list_of_times, x):
    """
    Get Average Over X/list slicing, using get_wca_avg method
    """
    a_o_x = []
    for i, _ in enumerate(list_of_times):
        if i + 1 < x:
            continue
        else:
            a_o_x.append((i + 1, find_wca_avg(list_of_times[i - x + 1:i + 1])))
    return a_o_x


# Read the export file into a str object
export = open('cstimer_20230708_203358.txt', 'r').read()
# Create a regex to match the actual penalties (like +2 or DNF) and times
pattern = re.compile(r"\[\[(\d+),(\d+)]")
# Extract the penalties and times, append them to the list
times = []
for penalty, time in pattern.findall(export):
    if int(penalty) == -1:  # Ignore DNFs; I just want solve stats
        continue
    else:
        times.append((int(penalty) + int(time)) * 0.001)
# Set up Seaborn stylez
sns.set_style("darkgrid")

# Lay out plot
plt.plot(range(1, len(times) + 1), times, marker='o')
plt.xticks(range(1, len(times) + 1))
plt.yticks(range(0, ceil(max(times, key=lambda x: float(x)))))
plt.xlabel('Number of solves')
plt.ylabel('Time in seconds')
plt.title('Cube solving times')
# Ao5, Ao12, Ao100
if len(times) >= 5:
    plt.plot(*zip(*avg_over_x(times, 5)), label='Ao5', marker='o')
if len(times) >= 12:
    plt.plot(*zip(*avg_over_x(times, 12)), label='Ao12', marker='o')
if len(times) >= 100:
    plt.plot(*zip(*avg_over_x(times, 100)), label='Ao100', marker='o')

# Mean line
total_mean = np.mean(times)
plt.axhline(total_mean, color='red', linestyle='--', label=f"Mean: {total_mean}")

plt.legend()
plt.show()
