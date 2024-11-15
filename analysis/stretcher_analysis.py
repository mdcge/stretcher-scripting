import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import stats
import numpy as np

import read_stretcher_output as rs

# Get data ---
forces_PTFE, weights_PTFE, displacements_PTFE = rs.read_stretcher_file("/home/max/phd/fibre-measurements/data/stretching/stretcher_steel_with_PTFE_12hrs_25N.csv")
forces_no_PTFE, weights_no_PTFE, displacements_no_PTFE = rs.read_stretcher_file("/home/max/phd/fibre-measurements/data/stretching/stretcher_steel_without_PTFE_20hrs_25N.csv")
times_PTFE = np.arange(len(forces_PTFE))/60
times_no_PTFE = np.arange(len(forces_no_PTFE))/60

def log_decay(x, A, a, B):
    return -A * np.log(x + a) + B

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


# Fit log decay ---
popt_PTFE, pcov_PTFE = curve_fit(log_decay, times_PTFE, forces_PTFE)
popt_no_PTFE, pcov_no_PTFE = curve_fit(log_decay, times_no_PTFE, forces_no_PTFE)

print("With PTFE:\n")
for i, name in enumerate(["A", "a", "B"]):
    print(f"{name} = {popt_PTFE[i]:.2f} +- {np.sqrt(np.diag(pcov_PTFE))[i]:.2f}")
print()
print("Without PTFE:\n")
for i, name in enumerate(["A", "a", "B"]):
    print(f"{name} = {popt_no_PTFE[i]:.2f} +- {np.sqrt(np.diag(pcov_no_PTFE))[i]:.2f}")


# Plot ---
plt.plot(times_PTFE[ranges_PTFE[0]:ranges_PTFE[1]], forces_PTFE[ranges_PTFE[0]:ranges_PTFE[1]],
         'o',
         color=(0,0,1,0.3),
         markersize=3,
         markeredgewidth=0.0,
         zorder=3,
         label="with PTFE (raw)")
plt.plot(group_mean(times_PTFE, 15), group_adaptive(forces_PTFE, 15),
         'bo',
         markersize=4,
         markeredgecolor='k',
         markeredgewidth=0.6,
         zorder=3,
         label="with PTFE (smoothed)")
plt.plot(times_no_PTFE[ranges_no_PTFE[0]:ranges_no_PTFE[1]], forces_no_PTFE[ranges_PTFE[0]:ranges_PTFE[1]],
         'o',
         color=(1,0,0,0.3),
         markersize=3,
         markeredgewidth=0.0,
         zorder=3,
         label="without PTFE (raw)")
plt.plot(group_mean(times_no_PTFE, 15), group_adaptive(forces_no_PTFE, 15, ratio=0.45),
         'ro',
         markersize=4,
         markeredgecolor='k',
         markeredgewidth=0.6,
         zorder=3,
         label="without PTFE (smoothed)")

# plt.plot(times_PTFE, log_decay(times_PTFE, np.float64(0.38), np.float64(55), np.float64(5), np.float64(25)), 'k')

plt.plot(times_PTFE, log_decay(times_PTFE, *popt_PTFE), 'b', zorder=2.5)
plt.plot(times_no_PTFE, log_decay(times_no_PTFE, *popt_no_PTFE), 'r', zorder=2.5)

plt.grid(zorder=-5)
plt.title("Force measured at set distance")
plt.xlabel("Time (hours)")
plt.ylabel("Force (N)")
plt.legend()
# plt.savefig("/home/max/phd/fibre-measurements/figures/stretching/steel-wire-25N.pdf", bbox_inches='tight')
plt.show()
