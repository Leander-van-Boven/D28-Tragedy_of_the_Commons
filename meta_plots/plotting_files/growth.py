import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

"""
FILE PATHS ARE RELATIVE TO THIS FILE,
THEREFORE THIS FILE SHOULD BE RUN FROM THE DIRECTORY THIS FILE IS IN!

- This file operates on a CSV file containing multiple batches of
    multiple experiments.
- Community runs do not need to be of the same length.
- Outputs plot for a SINGLE experiment, selected with plot_batch and
    plot_exp below
- Plots Resource count over epochs with Resource limitation range
"""

df = pd.read_csv('../csv/unimodal.csv')
m, n = df.shape

exp_number = max(df['Exp Num'])
agent_count = df['Count']

batch1 = 0
for i in df['batch']:
    if i == 1:
        batch1 += 1

batch_count = []
for k in range(12):
    batch_num = 0
    for x in df['batch']:
        if x == k + 1:
            batch_num += 1
    batch_count.append(batch_num)

# Initialize counting variables
batch_start = 0
exp_end = 0

# Select batch and experiment
plot_batch = 11
plot_exp = 106

# Loops through all 12 batches
# Loops through all ten experiments in each batch
# Counts length of each experiment
# Plots resource plot with limitaiton range for selected experiment
# Note for bimodal and trimodal plots, the amount of experiments needs
# to be changed to 54 for bimodal and 2160 for trimodal (not recommended)
for w in range(12):
    exp_end = 0
    for i in range(10):
        exp0 = 0
        for j in df['Exp Num'][batch_start:batch_start+batch_count[w]]:
            if j == i + df['Exp Num'][batch_start]:
                exp0 += 1

        if w == (plot_batch - 1) and i == (plot_exp % 10):
            plt.rcParams["figure.figsize"] = [10, 5]
            plt.plot(
                df['Epoch'][exp_end+batch_start:exp_end+exp0+batch_start],
                df['Resource'][exp_end+batch_start:exp_end+exp0+batch_start],
                "g")
            plt.fill_between(
                df['Epoch'][exp_end+batch_start:exp_end+exp0+batch_start],
                df['Resource Limit']
                  [exp_end+batch_start:exp_end+exp0+batch_start],
                df['Resource Unlimit']
                  [exp_end+batch_start:exp_end+exp0+batch_start],
                color="r", alpha=.2)
            plot_mean = str(round(df[df.columns[2]][exp_end+batch_start], 2))
            plot_std = str(round(df[df.columns[3]][exp_end+batch_start], 2))

        exp_end += exp0

    if w == plot_batch:
        plt.title('Resource Growth with Limit/Unlimit Range, Batch ' +
                  str(plot_batch) + ': Mean = ' + plot_mean + " and STD = " +
                  plot_std)
        plt.xlim(200, 300)
        plt.ylim(0, 1800)
        plt.xlabel('Epoch')
        plt.ylabel('Resource Count')
        plt.savefig('Resource_Growth_b' + str(plot_batch) + '_e' +
                    str(plot_exp) + '.png')
        plt.show()
    exp_end += exp0
    batch_start += batch_count[w]
