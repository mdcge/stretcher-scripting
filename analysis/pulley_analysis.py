import matplotlib.pyplot as plt
import numpy as np

import read_stretcher_output as rs

def get_data(filename):
    forces, weights, displacements = rs.read_stretcher_file(filename)
    times = np.arange(len(forces))/60
    return times, forces, weights, displacements

def group_mean(data, g):
    return np.array([np.mean(data[i:i+g]) for i in range(0, len(data), g)])

def plot_data(times, forces, group_size,
              ranges=(0,-1),
              raw_colour=(1,0,0,0.3),
              raw_marker_size=2.5,
              raw_label="raw data",
              smooth_colour=(1,0,0),
              smooth_marker_size=4.0,
              smooth_label="smooth data",
              raw_format='o',
              raw_linewidth=0.2,
              smooth_marker_edge_width=0.4,
    raw_times, raw_forces = times[ranges[0]:ranges[1]], forces[ranges[0]:ranges[-1]]
    smooth_times, smooth_forces = group_mean(times[ranges[0]:ranges[1]], group_size)[ranges[0]//group_size:ranges[1]//group_size], group_mean(forces[ranges[0]:ranges[1]], group_size)[ranges[0]//group_size:ranges[-1]//group_size]
    raw_points, = plt.plot(raw_times, raw_forces,
                           raw_format,
                           color=raw_colour,
                           markersize=raw_marker_size,
                           markeredgewidth=0.0,
                           linewidth=raw_linewidth,
                           zorder=3,
                           label=raw_label)
    smooth_points, = plt.plot(smooth_times, smooth_forces,
                              'o',
                              color=smooth_colour,
                              markersize=smooth_marker_size,
                              markeredgewidth=smooth_marker_edge_width,
                              zorder=4,
                              label=smooth_label)
    return raw_points, smooth_points, None


# Plots ---------
times_5N_1, forces_5N_1, _, _ = get_data("/home/max/phd/fibre-measurements/data/stretching/stretcher_steel_pulley_5N_run_01.csv")
true_force_5N_1 = (497.349 / 1000) * 9.81

plot_data(times_5N_1, forces_5N_1, 50, ranges=(1,-1), true_force=true_force_5N_1)
plt.ylim([4, 5.3])
plt.show()
