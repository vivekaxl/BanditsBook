import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')
import seaborn as sns
sns.set(color_codes=True)
import pandas as pd
sns.set_style('white')

data = [['System', 'Method', 'Operational Cost', 'Measurement Cost'],
                ['Hadoop','Brute\nForce', 1.0,55],
                ['Hadoop', 'Bayesian\nOptimization', 1.1,12],
                ['Hadoop', 'Micky', 1.2,1],
                ['Spark','Brute\nForce',1.0,55],
                ['Spark','Bayesian\nOptimization', 1.1,12],
                ['Spark', 'Micky',1.21,1],
                ['Spark-1.5','Brute\nForce',1,53],
                ['Spark-1.5','Bayesian\nOptimization', 1,15],
                ['Spark-1.5', 'Micky',1.3,1],
                ['All','Brute\nForce', 1.0,67],
                ['All','Bayesian\nOptimization', 1.2,19],
                ['All', 'Micky',1.2,1],
                 ]

colors = ['#383F4C', '#FFB219', '#9FA9B2']

# fig, ax = plt.subplots()
headers = data.pop(0)
df = pd.DataFrame(data)
df.transpose()
df.columns = headers

s = sns.factorplot(x='System', y='Operational Cost', hue='Method', data=df, kind='bar', legend_out=False, palette=colors)


plt.ylabel('Operational Cost (normalized wrt. Brute Force)')
plt.legend(bbox_to_anchor=(1.05, 1.15),  ncol=3)
s.despine(ax=s, bottom=True, left=True)
s.savefig("Figures/motivation_1"  + ".png")
plt.cla()

s = sns.factorplot(x='System', y='Operational Cost', hue='Method', data=df, kind='bar', legend_out=False, palette=colors)
plt.ylabel('Execution Time (normalized wrt. Brute Force)')
plt.legend(bbox_to_anchor=(1.05, 1.15),  ncol=3)
s.despine(ax=s, bottom=True, left=True)
s.savefig("Figures/motivation_3"  + ".png")
plt.cla()

s = sns.factorplot(x='System', y='Measurement Cost', hue='Method', data=df, kind='bar', legend_out=False, palette=colors)
plt.ylabel('Operational Cost (normalized wrt. Micky)')
plt.legend(bbox_to_anchor=(1.05, 1.15),  ncol=3)
s.despine(ax=s, bottom=True, left=True)
s.savefig("Figures/motivation_2"  + ".png")
plt.cla()