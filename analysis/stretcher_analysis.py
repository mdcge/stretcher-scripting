import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

import read_stretcher_output as rs

forces, weights, displacements = rs.read_stretcher_file("/home/max/phd/fibre-measurements/data/stretching/stretcher_steel_with_PTFE_12hrs_25N.csv")
times = np.arange(len(forces))

def exp_decay(x, A, tau, t0, m, b):
    return A * np.exp((x-t0)/(-tau)) + m*x + b

popt, pcov = curve_fit(exp_decay, times, forces, p0=[1.36, 50, 1, -0.001, 23])

plt.plot(times, forces, 'o', markersize=3)
plt.plot(times, exp_decay(times, *popt), 'r')
plt.show()
