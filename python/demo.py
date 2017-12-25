from __future__ import division
# Need access to random numbers
import random

# Definitions of bandit arms
from arms.adversarial import *
from arms.bernoulli import *
from arms.normal import *
from arms.cloud import *

# Definitions of bandit algorithms
from algorithms.epsilon_greedy.standard import *
from algorithms.epsilon_greedy.annealing import *
from algorithms.softmax.standard import *
from algorithms.softmax.annealing import *
from algorithms.ucb.ucb1 import *
from algorithms.ucb.ucb2 import *
from algorithms.exp3.exp3 import *
from algorithms.hedge.hedge import *

# # Testing framework
from testing_framework.tests import *
import os
import pandas as pd
import matplotlib.pyplot as plt
import os
import collections


def draw_historgram(x, y, name, method):
    plt.figure(figsize=(8, 6))
    plt.bar(range(len(x)), height=x)
    plt.xticks([xx for xx in range(len(x))], y, rotation=90)
    plt.title(name + " " + method)
    plt.ylabel('Count')
    plt.savefig(name.replace('data', 'figures').replace('.csv', '') + "_" + method.replace(' ', '_') + '.png')
    plt.cla()

# Convenience functions
def cloud_arms(data_file):
    content = pd.read_csv(data_file)
    vm_types = sorted([c for c in content.columns if '.' in c])  # to make sure we get the same instance order
    arms = []
    for vm_type in vm_types:
        arms.append(CloudArm(content[vm_type].values.tolist()))
    return arms, vm_types


os.system('rm -f ./figures/*')
data_folder = "./data/"
datas = [data_folder + d for d in os.listdir(data_folder) if '.csv' in d]

# Ground Truth
rot = {
    './data/spark15_time.csv': ['r4.2xlarge', 'm4.2xlarge', 'm3.2xlarge'],
    './data/spark15_cost.csv': ['m4.xlarge', 'm4.large', 'c4.xlarge'],
    './data/hadoop_time.csv': ['r4.2xlarge', 'r3.2xlarge', 'm4.2xlarge'],
    './data/hadoop_cost.csv': ['m4.large', 'c4.large', 'm4.xlarge'],
    './data/spark_time.csv': ['r4.2xlarge', 'm4.2xlarge', 'r3.2xlarge'],
    './data/spark_cost.csv': ['m4.large', 'r4.large', 'm4.xlarge']
}


for data in datas:
    reps = 30
    trials = 50
    collector = {}
    for rep in xrange(reps):
        arms, vm_types = cloud_arms(data)
        n_arms = len(arms)
        algo1 = EpsilonGreedy(0.1, [], [])
        algo2 = Softmax(1.0, [], [])
        algo3 = UCB1([], [])

        algos = [algo1, algo2, algo3]

        for algo in algos:
            algo.initialize(n_arms)

        for t in range(trials):
          for algo in algos:
            chosen_arm = algo.select_arm()
            reward = arms[chosen_arm].draw()
            algo.update(chosen_arm, reward)

        # find the recommend vm_instances
        for algo in algos:
            if algo.name not in collector:
                collector[algo.name] = [vm_types[algo.counts.index(max(algo.counts))]]
            else:
                collector[algo.name].append(vm_types[algo.counts.index(max(algo.counts))])

    print
    print data, rot[data]
    for key in collector.keys():
        print key, collections.Counter(collector[key])

"""
num_sims = 1000
horizon = 10
results = test_algorithm(algo1, arms, num_sims, horizon)
"""