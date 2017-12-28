from __future__ import division
import pandas as pd

filename = "./Processed/run_ex.csv"

content = pd.read_csv(filename)
lines = []
workloads = content.exp_id.unique().tolist()
instances = content.config_id.unique().tolist()
for workload in workloads:
    measurements = [-1 for _ in xrange(len(instances))]
    subset = content[content.exp_id==workload]
    w_instances = subset.config_id.tolist()
    for w_instance in w_instances:
        # measurements[w_instance-1] = round(float(subset[subset.config_id==w_instance].cost), 3)
        measurements[w_instance-1] = round(float(subset[subset.config_id==w_instance].time), 3)
    lines.append([workload] + measurements)

import csv
# with open("./Processed/cost_raw.csv", "wb") as f:
with open("./Processed/time_raw.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(lines)
