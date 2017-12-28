from __future__ import division
import pandas as pd

file1 = "./Data/run.csv"
file2 = "./Data/experiment.csv"

d2 = open(file2, 'r')
c2 = d2.readlines()

dict2 = {}
for i, line in enumerate(c2):
    if i != 0:
        id, name = line.strip().split(',')
        dict2[id] = name

d1 = open(file1, 'r')
c1 = d1.readlines()

dict1 = {}
lines = []
for i, line in enumerate(c1):
    temp = line.strip().split(',')
    if i != 0:
        temp[1] = dict2[temp[1]]
    lines.append(temp)

import csv

with open("./Processed/transform1.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(lines)



