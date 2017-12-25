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


# Convenience functions
def cloud_arms(data_file):
    content = pd.read_csv(data_file)
    vm_types = sorted([c for c in content.columns if '.' in c])  # to make sure we get the same instance order
    arms = []
    for vm_type in vm_types:
        arms.append(CloudArm(content[vm_type].values.tolist()))
    return arms, vm_types

data_folder = "./data/"
datas = [data_folder + d for d in os.listdir(data_folder) if '.csv' in d]

for data in datas:
    arms, vm_types = cloud_arms(data)
    n_arms = len(arms)
    algo1 = EpsilonGreedy( 0.1, [], [])
    algo2 = Softmax( 1.0, [], [])
    algo3 = UCB1( [], [])
    # algo4 = Exp3( 0.2, [])

    algos = [algo1, algo2, algo3]

    for algo in algos:
      algo.initialize(n_arms)

    for t in range(40):
      for algo in algos:
        chosen_arm = algo.select_arm()
        reward = arms[chosen_arm].draw()
        algo.update(chosen_arm, reward)

    print data
    print "Epsilon Greedy"
    for v, cn in zip(vm_types, algo1.counts):
        print v[:5], cn, "| ",
    print

    print "Softmax"
    for v, cn in zip(vm_types, algo2.counts):
        print v[:5], cn, "| ",
    print

    print "UCB1"
    for v, cn in zip(vm_types, algo3.counts):
        print v[:5], cn, "| ",
    print

    raw_input()


"""
num_sims = 1000
horizon = 10
results = test_algorithm(algo1, arms, num_sims, horizon)
"""