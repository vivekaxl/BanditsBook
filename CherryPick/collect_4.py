from __future__ import division
""" This script is used to add cost to run.csv"""
file1 = "./Data/experiment.csv"
file2 = "./Processed/transform3.csv"
file3 = "./Data/run.csv"

c1 = open(file1).readlines()
c2 = open(file2).readlines()
c3 = open(file3).readlines()

dict1 = {}
for i,line in enumerate(c1):
    if i != 0:
        id, name = line.strip().split(',')
        dict1[id] = name

dict2 = {}
for i, line in enumerate(c2):
    if i != 0:
        t = line.strip().split(',')
        dict2[t[0]] = t[1:]

lines = []
lines.append((c3[0].strip() + ',cost').split(','))

for i, line in enumerate(c3):
    if i != 0:
        t = line.strip().split(',')
        id = t[0]
        exp_id = t[1]
        config_id = t[2]
        time = t[3]

        temp = []
        temp.append(id)
        temp.append(dict1[exp_id])
        temp.extend(dict2[config_id])
        temp.append(time)

        cost = (float(temp[2]) * (float(temp[7]) + float(temp[13]))) * (float(temp[14])/3600)
        temp.append(str(cost))
        temp = line.strip().split(',') + [cost]

        lines.append(temp)

import csv
with open("./Processed/run_ex.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(lines)
