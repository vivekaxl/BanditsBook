import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

algorithms = [ 'Epsilon_Greedy_0.1', 'Epsilon_Greedy_0.2', 'Epsilon_Greedy_0.3', 'Epsilon_Greedy_0.4',
               'SoftMax_0.1', 'SoftMax_0.2', 'SoftMax_0.4',   'SoftMax_0.8', 'SoftMax_1.0',
               'UCB1',]

data = pickle.load(open('all_results.p'))
seeds = data.keys()
for algorithm in algorithms:
    print algorithm
    store = {}
    for seed in seeds:
        store[seed] = {}
        trails = data[seed].keys()
        print seed, algorithm,
        store[seed]['x'] = [seed*18 + 20 + i for i in xrange(len(trails))]
        store[seed]['y'] = []
        for trail in trails:
            store[seed]['y'].append(data[seed][trail][algorithm]['Present'])

    fig, ax = plt.subplots(sharex=True, sharey=True)
    sns.set_style("white")

    df = pd.DataFrame([store[0]['x'], store[0]['y']]).transpose()
    df.columns = ['x', 'y']
    g = sns.regplot(x='x', y='y', data=df, ax=ax, fit_reg=True, truncate=True, label='Seed 0',  ci=0, line_kws={'lw':3}, scatter_kws={"color":"b","alpha":0.33, 's':45}, marker='^')
    g.set(ylim=(0, 33))


    df = pd.DataFrame([store[1]['x'], store[1]['y']]).transpose()
    df.columns = ['x', 'y']
    g = sns.regplot(x='x', y='y', data=df, ax=ax, fit_reg=True, truncate=True, label='Seed 1', ci=0, line_kws={'lw':3}, scatter_kws={"color":"g","alpha":0.33, 's':45}, marker='o')
    g.set(ylim=(0, 33))

    # ax3 = ax.twinx()
    df = pd.DataFrame([store[2]['x'], store[2]['y']]).transpose()
    df.columns = ['x', 'y']
    g = sns.regplot(x='x', y='y', data=df, ax=ax, fit_reg=True, truncate=True, label='Seed 2', ci=0, line_kws={'lw':3}, scatter_kws={"color":"r","alpha":0.33, 's':45}, marker='*')
    g.set(ylim=(0, 33))

    plt.legend(bbox_to_anchor=(0.9, 1.1),  ncol=3, fontsize = 15)
    plt.ylim(0, 33)
    plt.xlim(0, 100)
    plt.xlabel('Number of Measurements', fontsize = 15)
    plt.ylabel('Stability', fontsize = 15)
    # plt.title('Algorithm = ' + algorithm)
    # sns.despine()
    plt.savefig('./Diagram/' + algorithm + '.png')
    plt.cla()