def plot_mab_opportunity(df, optimization_target, framework=None, experiment_dir='Figures'):
    records = {}
    records_optimal = {}
    #if optimization_target == 'time':
    #    if framework == 'all':
    #        df = df_landscape_time_normalized
    #    else:
    #        df = df_landscape_time_normalized.loc[(framework, slice(None), slice(None))]
    #elif optimization_target == 'cost':
    #    if framework == 'all':
    #        df = df_landscape_cost_normalized
    #    else:
    #        df = df_landscape_cost_normalized.loc[(framework, slice(None), slice(None))]
            
    for instance_type in df.columns:
        records[instance_type] = 0
        records_optimal[instance_type] = 0
    for w in df.index:
        dfx = df.ix[w, :]
        for instance_type in dfx[dfx <= 1.3].index:
            records[instance_type] += 1
        for instance_type in dfx[dfx == 1].index:
            records_optimal[instance_type] += 1
    s = pd.Series(records).sort(inplace=False, ascending=False) / len(df)
    s1 = pd.Series(records_optimal).sort(inplace=False, ascending=False) / len(df)
    s2 = df.ix[:, s.index].quantile(0.25)

    
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ['r' if index == s1.idxmax() else 'g' if s[index] >= 0.4 else 'b' for index in s.index]
    s.plot(ax=ax, kind='bar', color=colors)
    ax.set_ylabel('Workload Percentage'.format(optimization_target), fontsize=16)
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(16) 
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(16)
    ax.set_ylim(0, 1)
    output_name = 'motivation_{}_{}_percentage.pdf'.format(optimization_target, framework)
    output = os.path.join(experiment_dir, output_name)
    fig.savefig(output, bbox_inches='tight', transparent=True, dpi=300)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    #ax2 = ax.twinx()
    colors = ['b' if s2[index] > 1.3 else 'r' if index == s1.idxmax() else 'g' for index in s2.index]
    s2.plot(ax=ax, kind='bar', color=colors)
    ax.set_ylabel('Median Normalized {}'.format(optimization_target), fontsize=16)
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(16) 
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(16)
    ax.set_ylim(0, 2)
    output_name = 'motivation_{}_{}_performance.pdf'.format(optimization_target, framework)
    output = os.path.join(experiment_dir, output_name)
    fig.savefig(output, bbox_inches='tight', transparent=True, dpi=300)


if __name__ == '__main__':
    plot_mab_opportunity(df_landscape_cost_normalized, 'cost', 'all')
    plot_mab_opportunity(df_landscape_cost_normalized.loc[('hadoop', slice(None), slice(None))], 'cost', 'hadoop')
    plot_mab_opportunity(df_landscape_cost_normalized.loc[('spark', slice(None), slice(None))], 'cost', 'spark')
    plot_mab_opportunity(df_landscape_cost_normalized.loc[('spark1.5', slice(None), slice(None))], 'cost', 'spark1.5')
