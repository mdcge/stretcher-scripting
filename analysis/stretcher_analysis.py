import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import stats
import numpy as np

import read_stretcher_output as rs

# Get data ---
forces_PTFE, weights_PTFE, displacements_PTFE = rs.read_stretcher_file("/home/max/phd/fibre-measurements/data/stretching/stretcher_steel_with_PTFE_12hrs_25N.csv")
forces_no_PTFE, weights_no_PTFE, displacements_no_PTFE = rs.read_stretcher_file("/home/max/phd/fibre-measurements/data/stretching/stretcher_steel_without_PTFE_20hrs_25N.csv")
forces_no_PTFE_2, weights_no_PTFE_2, displacements_no_PTFE_2 = rs.read_stretcher_file("/home/max/phd/fibre-measurements/data/stretching/stretcher_steel_without_PTFE_19hrs_25N.csv")
forces_no_PTFE_long, weights_no_PTFE_long, displacements_no_PTFE_long = rs.read_stretcher_file("/home/max/phd/fibre-measurements/data/stretching/stretcher_steel_without_PTFE_72hrs_25N.csv")
forces_no_PTFE_3, weights_no_PTFE_3, displacements_no_PTFE_3 = rs.read_stretcher_file("/home/max/phd/fibre-measurements/data/stretching/stretcher_steel_without_PTFE_24hrs_25N.csv")
forces_no_PTFE_5N_1, weights_no_PTFE_5N_1, displacements_no_PTFE_5N_1 = rs.read_stretcher_file("/home/max/phd/fibre-measurements/data/stretching/stretcher_steel_without_PTFE_20hrs_5N.csv")
times_PTFE = np.arange(len(forces_PTFE))/60
times_no_PTFE = np.arange(len(forces_no_PTFE))/60
times_no_PTFE_2 = np.arange(len(forces_no_PTFE_2))/60
times_no_PTFE_long = np.arange(len(forces_no_PTFE_long))/60
times_no_PTFE_3 = np.arange(len(forces_no_PTFE_3))/60
times_no_PTFE_5N_1 = np.arange(len(forces_no_PTFE_5N_1))/60

def log_decay(x, A, x0, B):
    return -A * np.log(x + x0) + B

def log_decay_sigmoid(x, A, x0, B, As, k, x0s):
    return -A * np.log(x + x0) + (As / (1+np.exp(k*(x-x0s)))) + B

def group_mean(data, g):
    return np.array([np.mean(data[i:i+g]) for i in range(0, len(data), g)])

def group_mode(data, g):
    return np.array([stats.mode(data[i:i+g])[0] for i in range(0, len(data), g)])

def group_adaptive(data, g, group_size=60, ratio=0.5):
    limit = find_mean_mode_limit(data, group_size=group_size, ratio=ratio)
    return np.array([stats.mode(data[i:i+g])[0] if i>limit else np.mean(data[i:i+g]) for i in range(0, len(data), g)])

def find_mean_mode_limit(data, group_size=60, ratio=0.5):
    for i in range(len(data)):
        if i+group_size == len(data):
            return np.infty
        elements = set(data[i:i+group_size])
        ms, cs = [], []
        for e in elements:
            ms.append(e)
            cs.append(list(data[i:i+group_size]).count(e))
        idx = np.argmax(ms)
        m = ms[idx]
        c = cs[idx]
        r = c / np.sum(cs)
        if r >= ratio:
            return i

ranges_PTFE = (0, -1)
ranges_no_PTFE = (0, -1)
ranges_no_PTFE_2 = (0, -1)
ranges_no_PTFE_long = (0, -1)
ranges_no_PTFE_3 = (0, -1)
ranges_no_PTFE_5N_1 = (0, -1)


# Fit log decay ---
popt_PTFE, pcov_PTFE = curve_fit(log_decay, times_PTFE, forces_PTFE)
popt_no_PTFE, pcov_no_PTFE = curve_fit(log_decay, times_no_PTFE, forces_no_PTFE)
popt_no_PTFE_2, pcov_no_PTFE_2 = curve_fit(log_decay, times_no_PTFE_2, forces_no_PTFE_2)
popt_no_PTFE_long, pcov_no_PTFE_long = curve_fit(log_decay, times_no_PTFE_long[0:1200], forces_no_PTFE_long[0:1200])
popt_no_PTFE_long_full, pcov_no_PTFE_long_full = curve_fit(log_decay, times_no_PTFE_long, forces_no_PTFE_long)
popt_no_PTFE_3, pcov_no_PTFE_3 = curve_fit(log_decay, times_no_PTFE_3, forces_no_PTFE_3)
popt_no_PTFE_5N_1, pcov_no_PTFE_5N_1 = curve_fit(log_decay, times_no_PTFE_5N_1, forces_no_PTFE_5N_1)

print("With PTFE:\n")
for i, name in enumerate(["A", "x0", "B"]):
    print(f"{name} = {popt_PTFE[i]:.3f} +- {np.sqrt(np.diag(pcov_PTFE))[i]:.3f}")
print()
print("Without PTFE:\n")
for i, name in enumerate(["A", "x0", "B"]):
    print(f"{name} = {popt_no_PTFE[i]:.2f} +- {np.sqrt(np.diag(pcov_no_PTFE))[i]:.2f}")
print()
print("Without PTFE (run 2):\n")
for i, name in enumerate(["A", "x0", "B"]):
    print(f"{name} = {popt_no_PTFE_2[i]:.2f} +- {np.sqrt(np.diag(pcov_no_PTFE_2))[i]:.2f}")
print()
print("Without PTFE (long run):\n")
for i, name in enumerate(["A", "x0", "B"]):
    print(f"{name} = {popt_no_PTFE_long[i]:.2f} +- {np.sqrt(np.diag(pcov_no_PTFE_long))[i]:.2f}")
print()
print("Without PTFE (run 3):\n")
for i, name in enumerate(["A", "x0", "B"]):
    print(f"{name} = {popt_no_PTFE_3[i]:.2f} +- {np.sqrt(np.diag(pcov_no_PTFE_3))[i]:.2f}")
print()
print("Without PTFE (5N, run 1):\n")
for i, name in enumerate(["A", "x0", "B"]):
    print(f"{name} = {popt_no_PTFE_5N_1[i]:.2f} +- {np.sqrt(np.diag(pcov_no_PTFE_5N_1))[i]:.2f}")


# Plot ---
group_size = 50

points1, = plt.plot(times_PTFE[ranges_PTFE[0]:ranges_PTFE[1]], forces_PTFE[ranges_PTFE[0]:ranges_PTFE[1]],
                    'o',
                    color=(0,0,1,0.15),
                    markersize=2,
                    markeredgewidth=0.0,
                    zorder=3,
                    label="with PTFE (raw)")
points2, = plt.plot(group_mean(times_PTFE, group_size), group_mean(forces_PTFE, group_size),
                    'bo',
                    markersize=4,
                    markeredgecolor='k',
                    markeredgewidth=0.4,
                    zorder=4,
                    label="with PTFE (smoothed)")
points3, = plt.plot(times_no_PTFE[ranges_no_PTFE[0]:ranges_no_PTFE[1]], forces_no_PTFE[ranges_no_PTFE[0]:ranges_no_PTFE[1]],
                    'o',
                    color=(1,0,0,0.15),
                    markersize=2,
                    markeredgewidth=0.0,
                    zorder=3,
                    label="without PTFE - run 1 (raw)")
points4, = plt.plot(group_mean(times_no_PTFE, group_size), group_mean(forces_no_PTFE, group_size),
                    'ro',
                    markersize=4,
                    markeredgecolor='k',
                    markeredgewidth=0.4,
                    zorder=4,
                    label="without PTFE - run 1 (smoothed)")
points5, = plt.plot(times_no_PTFE_2[ranges_no_PTFE_2[0]:ranges_no_PTFE_2[1]], forces_no_PTFE_2[ranges_no_PTFE_2[0]:ranges_no_PTFE_2[1]],
                    'o',
                    color=(0,0.7,0,0.15),
                    markersize=2,
                    markeredgewidth=0.0,
                    zorder=3,
                    label="without PTFE - run 2 (raw)")
points6, = plt.plot(group_mean(times_no_PTFE_2, group_size), group_mean(forces_no_PTFE_2, group_size),
                    'go',
                    markersize=4,
                    markeredgecolor='k',
                    markeredgewidth=0.4,
                    zorder=4,
                    label="without PTFE - run 2 (smoothed)")
points7, = plt.plot(times_no_PTFE_long[ranges_no_PTFE_long[0]:ranges_no_PTFE_long[1]], forces_no_PTFE_long[ranges_no_PTFE_long[0]:ranges_no_PTFE_long[1]],
                    'o',
                    color=(1,0,1,0.15),
                    markersize=2,
                    markeredgewidth=0.0,
                    zorder=3,
                    label="without PTFE - run 3 (raw)")
points8, = plt.plot(group_mean(times_no_PTFE_long, group_size), group_mean(forces_no_PTFE_long, group_size),
                    'o',
                    color=(1,0,1),
                    markersize=4,
                    markeredgecolor='k',
                    markeredgewidth=0.4,
                    zorder=4,
                    label="without PTFE - run 3 (smoothed)")
points9, = plt.plot(times_no_PTFE_3[ranges_no_PTFE_3[0]:ranges_no_PTFE_3[1]], forces_no_PTFE_3[ranges_no_PTFE_3[0]:ranges_no_PTFE_3[1]],
                    'o',
                    color=(1,0.7,0,0.15),
                    markersize=2,
                    markeredgewidth=0.0,
                    zorder=3,
                    label="without PTFE - run 4 (raw)")
points10, = plt.plot(group_mean(times_no_PTFE_3, group_size), group_mean(forces_no_PTFE_3, group_size),
                    'o',
                    color=(1,0.7,0),
                    markersize=4,
                    markeredgecolor='k',
                    markeredgewidth=0.4,
                    zorder=4,
                    label="without PTFE - run 4 (smoothed)")


# plt.plot(times_PTFE, log_decay(times_PTFE, np.float64(0.38), np.float64(55), np.float64(5), np.float64(25)), 'k')

plt.plot(times_PTFE, log_decay(times_PTFE, *popt_PTFE), 'b', zorder=3.5)
plt.plot(times_no_PTFE, log_decay(times_no_PTFE, *popt_no_PTFE), 'r', zorder=3.5)
plt.plot(times_no_PTFE_2, log_decay(times_no_PTFE_2, *popt_no_PTFE_2), 'g', zorder=3.5)
plt.plot(times_no_PTFE_3, log_decay(times_no_PTFE_3, *popt_no_PTFE_3), color=(1,0.7,0), zorder=3.5)
plt.plot(times_no_PTFE_long[720:], log_decay(times_no_PTFE_long[720:], *popt_PTFE), 'b', linestyle='dashed', zorder=3.5)
plt.plot(times_no_PTFE_long[1200:], log_decay(times_no_PTFE_long[1200:], *popt_no_PTFE), 'r', linestyle='dashed', zorder=3.5)
plt.plot(times_no_PTFE_long[1200:], log_decay(times_no_PTFE_long[1200:], *popt_no_PTFE_2), 'g', linestyle='dashed', zorder=3.5)
plt.plot(times_no_PTFE_long[1440:], log_decay(times_no_PTFE_long[1440:], *popt_no_PTFE_3), color=(1,0.7,0), linestyle='dashed', zorder=3.5)
line1, = plt.plot(times_no_PTFE_long, log_decay(times_no_PTFE_long, *popt_no_PTFE_long), color=(1,0,1), zorder=3.5, label="20 hour fit")
line2, = plt.plot(times_no_PTFE_long, log_decay(times_no_PTFE_long, *popt_no_PTFE_long_full), linestyle='dashdot', color=(0.6,0,0.6), zorder=3.5, label="72 hour fit")

plt.grid(zorder=-5)
plt.title("Force measured at set distance")
plt.xlabel("Time (hours)")
plt.ylabel("Force (N)")

leg = plt.legend(handles=[points2, points4, points6, points8, points10], prop={'size': 7}, loc='upper right')
# ax = plt.gca().add_artist(leg)
# plt.legend(handles=[line1, line2], bbox_to_anchor=(0.6, 1), prop={'size': 7})

plt.ylim([21.4, 25.3])
# plt.savefig("/home/max/phd/fibre-measurements/figures/stretching/steel-wire-25N-20hrs.pdf", bbox_inches='tight')
plt.show()


points11, = plt.plot(times_no_PTFE_5N_1[ranges_no_PTFE_5N_1[0]:ranges_no_PTFE_5N_1[1]], forces_no_PTFE_5N_1[ranges_no_PTFE_5N_1[0]:ranges_no_PTFE_5N_1[1]],
                    'bo',
                    markersize=2,
                    markeredgewidth=0.0,
                    zorder=3,
                    label="without PTFE - run 1 (raw)")
points12, = plt.plot(group_mean(times_no_PTFE_5N_1, group_size), group_mean(forces_no_PTFE_5N_1, group_size),
                    'bo',
                    markersize=4,
                    markeredgecolor='k',
                    markeredgewidth=0.4,
                    zorder=4,
                    label="without PTFE - run 1 (smoothed)")

plt.plot(times_no_PTFE_5N_1, log_decay(times_no_PTFE_5N_1, *popt_no_PTFE_5N_1), 'b', zorder=3.5)

plt.grid(zorder=-5)
plt.title("Force measured at set distance")
plt.xlabel("Time (hours)")
plt.ylabel("Force (N)")

leg = plt.legend(handles=[points12], prop={'size': 7}, loc='upper right')
# ax = plt.gca().add_artist(leg)
# plt.legend(handles=[line1, line2], bbox_to_anchor=(0.6, 1), prop={'size': 7})

# plt.ylim([21.4, 25.3])
# plt.savefig("/home/max/phd/fibre-measurements/figures/stretching/steel-wire-25N-20hrs.pdf", bbox_inches='tight')
plt.show()
