from __future__ import division

f1 = "./Data/configuration.csv"
d1 = open(f1)
c1 = d1.readlines()

f2 = "./Processed/transform2.csv"
d2 = open(f2)
c2 = d2.readlines()

dict2 = {}
for i,line in enumerate(c2):
    if i != 0:
        temp = line.strip().split(',')
        assert(len(temp) == 11), "Something is wrong"
        id = temp[0]
        rest = temp[1:]
        dict2[id] = rest

lines = []
for i, line in enumerate(c1):
    if i == 0:
        temp = []
        temp.append(c1[0].strip().split(',')[0])
        temp.append(c1[0].strip().split(',')[1])
        temp.append(c1[0].strip().split(',')[2])
        temp.extend(c2[0].strip().split(',')[1:])
        lines.append(temp)
    else:
        temp = []
        temp.extend(line.strip().split(','))
        temp.extend(dict2[line.strip().split(',')[2]])
        lines.append(temp)

import csv

with open("./Processed/transform3.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(lines)