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
datas = [data_folder + d for d in sorted(os.listdir(data_folder)) if '.csv' in d] #

# Ground Truth
rot = {
    './data/all_time.csv': ['c3.large', 'r4.2xlarge', 'm4.2xlarge'],
    './data/spark15_time.csv': ['r4.2xlarge', 'm4.2xlarge', 'm3.2xlarge'],
    './data/spark15_cost.csv': ['m4.xlarge', 'm4.large', 'c4.xlarge'],
    './data/hadoop_time.csv': ['r4.2xlarge', 'r3.2xlarge', 'm4.2xlarge'],
    './data/all_cost.csv': ['c3.large', 'm4.large', 'm4.xlarge'],
    './data/hadoop_cost.csv': ['m4.large', 'c4.large', 'm4.xlarge'],
    './data/spark_time.csv': ['r4.2xlarge', 'm4.2xlarge', 'r3.2xlarge'],
    './data/spark_cost.csv': ['m4.large', 'r4.large', 'm4.xlarge']
}


def run(iterate, trials, reps=30):
    for data in datas:
        collector = {}
        for rep in xrange(reps):
            arms, vm_types = cloud_arms(data)
            n_arms = len(arms)
            algo1 = EpsilonGreedy(0.1, [], [])
            algo2 = Softmax(1.0, [], [])
            algo3 = UCB1([], [])
            algo4 = EpsilonGreedy(0.2, [], [])
            algo5 = EpsilonGreedy(0.3, [], [])
            algo6 = EpsilonGreedy(0.4, [], [])
            algo7 = Softmax(0.1, [], [])
            algo8 = Softmax(0.2, [], [])
            algo9 = Softmax(0.4, [], [])
            algo10 = Softmax(0.8, [], [])

            algos = [algo1, algo2, algo3, algo4, algo5, algo6, algo7, algo8, algo9, algo10]

            for algo in algos:
                algo.initialize(n_arms)
                for iter in xrange(iterate):
                    for arm in xrange(n_arms):
                        reward = arms[arm].draw()
                        algo.update(arm, reward)

            for t in range(trials):
              for algo in algos:
                chosen_arm = algo.select_arm()
                reward = arms[chosen_arm].draw()
                algo.update(chosen_arm, reward)

            # find the recommend vm_instances
            for algo in algos:
                if algo.name not in collector:
                    collector[algo.name] = {'Present': 0, 'Absent': 0}

                if vm_types[algo.counts.index(max(algo.counts))] in rot[data]:
                    collector[algo.name]['Present'] += 1
                else:
                    collector[algo.name]['Absent'] += 1

        return collector

# print data,"|",
# for k in sorted(collector.keys()):
#     print k+'_p','|', k+'_a', '|',
# print


all_iterates = [0, 1, 2]
all_trials = [20+i for i in xrange(1, 40)]

all_results = {}
for iterate in all_iterates:
    all_results[iterate] = {}
    for trail in all_trials:
        print '. ',
        ret = run(iterate, trail)
        all_results[iterate][trail] = ret
    print

import pickle
pickle.dump(all_results, open('./PickleFolder/all_results.p', 'w'))