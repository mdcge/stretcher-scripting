import numpy as np

def read_stretcher_file(filename):
    with open(filename, 'r') as f:
        data = f.readlines()
    stripped_data = list(map(lambda x: x.strip(), data))
    extracted_values = list(map(lambda x: np.array([float(x[3:7]), float(x[10:14]), float(x[17:21])]), stripped_data))
    return np.array(extracted_values)[:,0], np.array(extracted_values)[:,1], np.array(extracted_values)[:,2]
