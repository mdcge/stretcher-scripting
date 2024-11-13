import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

import read_stretcher_output as rs

forces, weights, displacements = rs.read_stretcher_file("/home/max/phd/fibre-measurements/data/stretching/stretcher_steel_with_PTFE_12hrs_25N.csv")
times = np.arange(len(forces))

def log_decay(x, A, k, a, B):
    return -A * np.log(k*x + a) + B

popt, pcov = curve_fit(exp_decay, times, forces, p0=[1.36, 50, 1, -0.001, 23])

plt.plot(times, forces, 'o', markersize=3)
plt.plot(times, exp_decay(times, *popt), 'r')
# Fit log decay ---
# popt_PTFE, pcov_PTFE = curve_fit(log_decay, group_adaptive(times_PTFE, 15), group_adaptive(forces_PTFE, 15), p0=[0.4, 35, 10, 26])
popt_PTFE, pcov_PTFE = curve_fit(log_decay, times_PTFE, forces_PTFE, p0=[0.4, 35, 90, 26])
popt_no_PTFE, pcov_no_PTFE = curve_fit(log_decay, times_no_PTFE, forces_no_PTFE)

print("With PTFE:\n")
for i, name in enumerate(["A", "k", "a", "b"]):
    print(f"{name} = {popt_PTFE[i]:.2f} +- {np.sqrt(np.diag(pcov_PTFE))[i]:.2f}")
print()
print("Without PTFE:\n")
for i, name in enumerate(["A", "k", "a", "b"]):
    print(f"{name} = {popt_no_PTFE[i]:.2f} +- {np.sqrt(np.diag(pcov_no_PTFE))[i]:.2f}")
plt.plot(times_PTFE, log_decay(times_PTFE, *popt_PTFE), 'b')
# plt.plot(times_no_PTFE/60, log_decay(times_no_PTFE, *popt_no_PTFE), 'r')
plt.show()
