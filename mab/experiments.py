import numpy as np
import pandas as pd

from mab.algorithms import *


def load_db(data_path, shuffled=True):
    db = pd.read_csv(data_path)
    db = db.set_index(['framework', 'workload', 'datasize'])
    db = 1 / db
    if shuffled:
        db = db.sample(frac=1, axis=0).sample(frac=1, axis=1)
    return db


def export_result(algo):
    result = {}
    best_config = algo.reward.mean().idxmax()
    for workload in algo.reward.index:
        workload_rewards = algo.reward.ix[workload, :]
        workload_rewards = workload_rewards[workload_rewards > 0]
        # print(workload_rewards)
        if len(workload_rewards) > 0:
            #print('1)', workload_rewards.index.tolist())
            #print('#', 1.0 / workload_rewards.max())
            #print('@', workload_rewards.idxmax())
            result[workload] = {
                'steps': workload_rewards.index.tolist(),
                'selected_performance': 1.0 / workload_rewards.max(),
                'selected_config': workload_rewards.idxmax(),
            }
        else:
            #print('2)', best_config)
            #print('#', 1.0 / algo.db.ix[workload, best_config])
            #print('@', best_config)
            result[workload] = {
                'steps': [],
                'selected_performance': 1.0 / algo.db.ix[workload, best_config],
                'selected_config': best_config,
            }

    return result


def run_parallel(db, method_class, method_parameters, num_trials, num_init_iterations, mode='quick', num_repetitions=10, statistics_method='mean'):
    df_records_performance = []
    df_records_steps = []

    for i in range(num_repetitions):
        if method_parameters:
            method = method_class(db, method_parameters)
        else:
            method = method_class(db)
        func = run_quick_explore if mode == 'quick' else run_full_search
        result = func(method, num_trials, num_init_iterations)
        df = pd.DataFrame({k: {'selected_performance': result[k]['selected_performance'], 'steps': len(result[k]['steps'])} for k in result.keys()}).T
        df_records_performance.append(df['selected_performance'])
        df_records_steps.append(df['steps'])
    if statistics_method == 'median':
        df_record = pd.concat([pd.concat(df_records_performance, axis=1).median(axis=1), pd.concat(df_records_steps, axis=1).median(axis=1)], keys=['selected_performance', 'steps'], axis=1)
    elif statistics_method == 'mean':
        df_record = pd.concat([pd.concat(df_records_performance, axis=1).mean(axis=1), pd.concat(df_records_steps, axis=1).mean(axis=1)], keys=['selected_performance', 'steps'], axis=1)

    return df_record


def run_quick_explore(algo, num_trials, num_init_iterations):
    print('trials:', num_trials)
    print('iterate:', num_init_iterations)

    # Step 1: try every arm in each iteration
    for _ in range(num_init_iterations):
        algo.init()
    print('init:', algo.count.sum().sum())
    display(algo.count.sum().sort(inplace=False))
    display(algo.reward.mean().sort(inplace=False))
    display(algo.count.sum(axis=1))

    # Step 2: run the algorithm
    for _ in range(num_trials):
        algo.smart_pull()
    print('pull:', algo.count.sum().sum())
    display(algo.count.sum().sort(inplace=False))
    display(algo.reward.mean().sort(inplace=False))
    display(algo.count.sum(axis=1))

    try:
        result = export_result(algo)
        return result
    except Exception as e:
        print(e)
        return algo.count


def run_full_search(algo, num_trials, num_init_iterations):
    print('trials:', num_trials)
    print('iterate:', num_init_iterations)

    # Step 1: try every arm in each iteration
    for _ in range(num_init_iterations):
        algo.init()
    print('init:', algo.count.sum().sum())

    # Step 2: run the algorithm
    # @TODO: the number calculation might be wrong
    num_workloads = len(algo.db)
    num_actual_trials = num_trials - num_workloads
    for t in range(num_actual_trials):
        algo.smart_pull()
    print('pull round 1:', algo.count.sum().sum())

    # Step 3: pull arm for each workload
    for trial_id, workload in zip(range(num_workloads), algo.reward.index):
        algo.select_pull(workload)
    print('pull round 2:', algo.count.sum().sum())

    try:
        result = export_result(algo)
        return result
    except Exception as e:
        print(e)
        return algo.count


def run_random_search(method, num_trials):
    for t in range(num_trials):
        method.pull()

    try:
        result = export_result(method)
        return result
    except Exception as e:
        print(e)
        return algo.count
