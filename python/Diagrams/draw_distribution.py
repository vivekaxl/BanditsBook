import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')
import seaborn as sns
sns.set(color_codes=True)
import pandas as pd
import os
import numpy as np

data_folder = "../Data/"
data_files = [data_folder + f for f in os.listdir(data_folder) if '.csv' in f]
for i,data_file in enumerate(data_files):
    content = pd.read_csv(data_file)
    # vm_types = sorted([c for c in content.columns if '.' in c])  # to make sure we get the same instance order
    vm_types = [ 'c3.large', 'c3.xlarge', 'c3.2xlarge',
                 'c4.large', 'c4.xlarge', 'c4.2xlarge',
                 'm3.large', 'm3.xlarge', 'm3.2xlarge',
                 'm4.large', 'm4.xlarge', 'm4.2xlarge',
                 'r3.large', 'r3.xlarge', 'r3.2xlarge',
                 'r4.large', 'r4.xlarge', 'r4.2xlarge']

    x = []
    y = []
    for vm_type in vm_types:
        x.append(vm_type)
        y.append(np.mean(content[vm_type]))
    # sns.axes_style('white')
    sns.set_style('white')

    colors = []
    for _x, _y in zip(x, y):
        if _y in sorted(y)[:3]:
            print _y, sorted(y)[:3]
            colors.append('red')
        elif 'c' in _x:
            colors.append('#002500')
        elif 'r3.' in _x or 'r4.' in _x:
            colors.append('#929982')
        elif 'm3.' in _x or 'm4.' in _x:
            colors.append('#EDCBB1')


    ax = sns.barplot(x, y, palette=colors)

    for n, (label, _y) in enumerate(zip(x, y)):
        ax.annotate(
            s='{:.1f}'.format(abs(_y)),
            xy=(n, _y),
            ha='center', va='center',
            xytext=(0, 10),
            textcoords='offset points',
            weight='bold'
        )

        # ax.annotate(
        #     s=label,
        #     xy=(n, 0),
        #     ha='center', va='center',
        #     xytext=(0, 10),
        #     textcoords='offset points',
        # )
        # axes formatting
    # ax.set_yticks([])
    # ax.set_xticks([])
    plt.xticks(rotation=90)
    sns.despine(ax=ax, bottom=True, left=True)
    ylabel = 'Normalized ' + ('Operational Cost' if 'cost' in data_file else 'Execution Time') + ' across ' + str(len(content[vm_type])) + ' Workloads'
    plt.ylabel(ylabel)
    plt.tight_layout()
    fig = ax.get_figure()
    fig.savefig("Figures/output_" + data_file.split('/')[-1].replace('.csv', '') + ".png")
    plt.cla()