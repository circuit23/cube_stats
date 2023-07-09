import matplotlib.pyplot as plt
import numpy as np
import re
import seaborn as sns


# Get WCA average (drop fastest and slowest, get mean) from any list of times
def find_wca_avg(list_of_times):
    truncated_list = [i for i in list_of_times if min(list_of_times) < i < max(list_of_times)]
    tlist_mean = np.mean(truncated_list)
    return tlist_mean


def avg_over_x(list_of_times, x):
    a_o_x = []
    for i, _ in enumerate(list_of_times):
        if i + 1 < x:
            continue
        else:
            a_o_x.append((i + 1, find_wca_avg(list_of_times[i - x + 1:i + 1])))

    return a_o_x


# Read the export file into a str object
export = open('cstimer_20230708_203358.txt', 'r').read()

# Create a regex to match the actual times
pattern = re.compile(r"\[\[0,(\d+)]")

# Extract the times and convert them into floats
times = [int(t) * 0.001 for t in pattern.findall(export)]

# Set up Seaborn stylez
sns.set_style("darkgrid")

# Lay out plot
plt.plot(times, marker='o')
plt.xlabel('Number of solves')
plt.ylabel('Time in seconds')
plt.title('Cube solving times')
# Ao5, Ao12, Ao100
if len(times) >= 5:
    plt.plot(*zip(*avg_over_x(times, 5)), label='Ao5')
if len(times) >= 12:
    plt.plot(*zip(*avg_over_x(times, 12)), label='Ao12')
if len(times) >= 100:
    plt.plot(*zip(*avg_over_x(times, 100)), label='Ao100')

# Mean line
total_mean = np.mean(times)
plt.axhline(total_mean, color='red', linestyle='--', linewidth=3, label=f"Mean: {total_mean}")

plt.legend()
plt.show()
