import numpy as np

# def read_stretcher_file(filename):
#     with open(filename, 'r') as f:
#         data = f.readlines()
#     stripped_data = list(map(lambda x: x.strip(), data))
#     extracted_values = list(map(lambda x: np.array([float(x[3:7]), float(x[10:14]), float(x[17:21])]), stripped_data))
#     return np.array(extracted_values)[:,0], np.array(extracted_values)[:,1], np.array(extracted_values)[:,2]

def read_stretcher_file(filename):
    with open(filename, 'r') as f:
        data = f.readlines()
    stripped_data = list(map(lambda x: x.strip(), data))
    values = []
    for s in stripped_data:
        v = ""
        for char in s:
            if char.isalpha():
                values.append(v)
                v = ""
            else:
                v += char
    values = list(map(float, list(filter(None, values))))
    packed_values = np.array([values[i:i+3] for i in range(0, len(values), 3)])
    return packed_values[:,0], packed_values[:,1], packed_values[:,2]

def read_temperature_file(filename):
    with open(filename, 'r', encoding="windows-1252") as f:
        data = f.readlines()
    just_data = list(map(lambda x: x.strip().split('\t'), data[29:]))
    clean_data = np.array(list(filter(lambda x: len(x) == 4, just_data)))
    return np.int32(clean_data[:,0]), clean_data[:,1], np.float64(clean_data[:,2]), np.float64(clean_data[:,3])
