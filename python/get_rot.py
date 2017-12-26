import pandas as pd
import os

data_folder = "./data/"
files = [data_folder + f for f in os.listdir(data_folder) if '.csv' in f]

contain = {}
for f in files:
    content = pd.read_csv(f)
    columns = [c for c in content.columns if '.' in c]
    temp = []
    for column in columns:
        temp.append([column, sum(content[column].values.tolist())])
    contain[f] = [t[0] for t in sorted(temp, key=lambda x:x[1])[:3]]


import pdb
pdb.set_trace()