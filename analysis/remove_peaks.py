import matplotlib.pyplot as plt
import numpy as np

import read_stretcher_output as rs

forces_no_PTFE_25N, weights_no_PTFE_25N, displacements_no_PTFE_25N = rs.read_stretcher_file("/home/max/phd/fibre-measurements/data/stretching/stretcher_steel_without_PTFE_20hrs_25N.csv")
forces_no_PTFE_5N, weights_no_PTFE_5N, displacements_no_PTFE_5N = rs.read_stretcher_file("/home/max/phd/fibre-measurements/data/stretching/stretcher_steel_without_PTFE_20hrs_5N.csv")
times_no_PTFE_25N = np.arange(len(forces_no_PTFE_25N)) / 60
times_no_PTFE_5N = np.arange(len(forces_no_PTFE_5N[0:1020])) / 60

# FT ---
yf_25N = np.fft.fft(forces_no_PTFE_25N)
xf_25N = np.fft.fftfreq(len(forces_no_PTFE_25N), d=1)
yf_5N = np.fft.fft(forces_no_PTFE_5N[0:1020])
xf_5N = np.fft.fftfreq(len(forces_no_PTFE_5N[0:1020]), d=1)

# IFT ---
y_25N = np.fft.ifft(yf_25N)
y_5N = np.fft.ifft(yf_5N)

# Plot ---
plt.stairs(yf_25N[:len(xf_25N)//2-1], xf_25N[:len(xf_25N)//2], fill=True, linewidth=1, edgecolor=(1,0,0,1), facecolor=(1,0,0,0.4), label="25N")
plt.stairs(yf_5N[len(xf_5N)//2:-1], xf_5N[len(xf_5N)//2:], fill=True, linewidth=1, edgecolor=(0,0,1,1), facecolor=(0,0,1,0.4), label="5N")

plt.yscale('log')
plt.legend()
plt.xlim([-0.15, 0.15])
plt.title("Fourier transformed data")
plt.xlabel("Frequency (min$^{-1}$)")
plt.ylabel("Amplitude (a.u.)")
# plt.savefig("/home/max/phd/fibre-measurements/figures/stretching/steel-wire-ft.pdf", bbox_inches='tight')
plt.show()
