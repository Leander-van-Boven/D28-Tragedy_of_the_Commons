import matplotlib.pyplot as plt
import pandas as pd

"""
FILE PATHS ARE RELATIVE TO THIS FILE,
THEREFORE THIS FILE SHOULD BE RUN FROM THE DIRECTORY THIS FILE IS IN!

- This file operates on a CSV file containing multiple batches of
    multiple experiments.
- Community runs do not need to be of the same length.
- Outputs multi-line plots of Mean SVO (with STD range) for each batch,
    containing all experimental runs in that batch.
"""

df = pd.read_csv('../csv/unimodal.csv')
m, n = df.shape

exp_number = max(df['Exp Num'])
Mean = df['Mean']

# Appending the length of each batch to a list
batch_count = []
for k in range(12):
    batch_num = 0
    for x in df['batch']:
        if x == k + 1:
            batch_num += 1
    batch_count.append(batch_num)

# Initializing counting variables
batch_start = 0
exp_end = 0

# Loops through all 12 batches
# Loops through all ten experiments in each batch
# Counts length of each experiment
# Plots median each experiment of a batch onto one plot
# Includes fill between ± 1 Decile
# 12 Plots total, with autosave option
# Note for bimodal and trimodal plots, the amount of experiments needs to
# 	be changed to 54 for bimodal and 2160 for trimodal (not recommended)
for w in range(12):
    print(batch_start, batch_start+batch_count[w])
    exp_end = 0

    for i in range(10):
        exp0 = 0
        for j in df['Exp Num'][batch_start:batch_start+batch_count[w]]:
            if j == i + df['Exp Num'][batch_start]:
                exp0 += 1

        plt.rcParams["figure.figsize"] = [10, 7]
        plt.plot(
            df['Epoch'][exp_end+batch_start:exp_end+exp0+batch_start],
            Mean[exp_end+batch_start:exp_end+exp0+batch_start],
            label=str(df.columns[2]) + " = " +
            str(df[df.columns[2]][exp_end+batch_start]) +
            " and " + df.columns[3] + " = " +
            str(round(df[df.columns[3]][exp_end+batch_start], 2)))
        plt.fill_between(
            df['Epoch'][exp_end+batch_start:exp_end+exp0+batch_start],
            Mean[exp_end+batch_start:exp_end+exp0+batch_start]
            - df['STD'][exp_end+batch_start:exp_end+exp0+batch_start],
            Mean[exp_end+batch_start:exp_end+exp0+batch_start]
            + df['STD'][exp_end+batch_start:exp_end+exp0+batch_start],
            alpha=.3)
        exp_end += exp0

    plt.rcParams["figure.figsize"] = [10, 7]
    plt.legend(loc='upper right')
    plt.legend(title='Distribution')
    plt.title('Mean SVO of 10 Unimodal Distributions, Batch ' + str(w+1))
    plt.xlabel('Epoch')
    plt.ylabel('SVO')
    plt.xlim(0, 100)
    plt.ylim(0, 1)
    plt.savefig('FinalMean' + str(w+1) + '.png')
    plt.show()
    batch_start += batch_count[w]
