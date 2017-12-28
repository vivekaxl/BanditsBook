from __future__ import division

""" This file is used to condense machine.csv"""

file1 = "./Data/disk_type.csv"
file2 = "./Data/virtual_machine_type.csv"

d1 = open(file1)
d2 = open(file2)

c2 = d2.readlines()

dict2 = {}
for i, line in enumerate(c2):
    if i != 0:
        temp = line.strip().split(',')
        id = temp[0]
        rest = temp[1:]
        dict2[id] = rest


c1 = d1.readlines()

dict1 = {}
for i, line in enumerate(c1):
    if i != 0:
        temp = line.strip().split(',')
        id = temp[0]
        rest = temp[1:]
        dict1[id] = rest

file3 = "./Data/machine.csv"
d3 = open(file3)

c3 = d3.readlines()

dict3 = {}
lines = []
for i, line in enumerate(c3):
    if i == 0:
        lines.append((line.strip().split(',')[0] + ',' + ','.join(c1[0].strip().split(',')[1:]) + ',' + ','.join(
            c2[0].strip().split(',')[1:])).split(','))
    else:
        t = line.strip().split(',')
        temp = [t[0]]
        temp.extend(dict1[t[1]])
        temp.extend(dict2[t[2]])
        lines.append(temp)


import csv

with open("./Processed/transform2.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(lines)