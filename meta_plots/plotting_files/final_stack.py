

import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


"""
- This file operates on a CSV file containing multiple batches of multiple experiments.  
- Community runs do not need to be of the same length.
- Outputs plot for a SINGLE experiment
- Select experiment with plot_batch and plot_exp below
- Outputs a stack plot agent count for five 20% SVO ranges
"""



df = pd.read_csv('unimodal.csv')

m, n = df.shape

exp_number = max(df['Exp Num'])


agent_count = df['Count']


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

# Set desired batch and experiment for plotting
plot_batch = 11
plot_exp = 106


# Loops through all 12 batches
# Loops through all ten experiments in each batch
# Counts length of each experiment
# Plots stack plot of selected experiment
# Note for bimodal and trimodal plots, the amount of experiments needs to be changed to 54 for bimodal and 2160 for trimodal (not recommended)
for w in range(12):

	exp_end = 0

	for i in range(10):
		exp0 = 0
		for j in df['Exp Num'][batch_start:batch_start+batch_count[w]]:

			if j == i + df['Exp Num'][batch_start]:
				exp0 += 1

		if w == (plot_batch - 1) and i == (plot_exp%10):
			plt.rcParams["figure.figsize"] = [10, 5]
			pal = sns.color_palette("Set1")


			plt.stackplot(df['Epoch'][exp_end+batch_start : exp_end+exp0+batch_start], df['A'][exp_end+batch_start : exp_end+exp0+batch_start], df['B'][exp_end+batch_start : exp_end+exp0+batch_start], df['C'][exp_end+batch_start : exp_end+exp0+batch_start], df['D'][exp_end+batch_start : exp_end+exp0+batch_start], df['E'][exp_end+batch_start : exp_end+exp0+batch_start],  labels=['0 - .20','.21 - .40','.40 - .60','.60 - .80','.80 - 1'], colors=pal, alpha=0.4)

			plot_mean = str(round(df[df.columns[2]][exp_end+batch_start],2)) 
			plot_std = str(round(df[df.columns[3]][exp_end+batch_start],2))

		exp_end += exp0
		
	if w == plot_batch:
		plt.legend(loc='upper right')
		plt.legend(title='SVO')
		plt.title('Stack Area Plot Batch ' + str(plot_batch) + ': Mean = '+ plot_mean + " and STD = " + plot_std)
		plt.xlim(0, 1000)
		plt.ylim(0, 100)
		plt.xlabel('Epoch')
		plt.ylabel('Agent Count')
		plt.savefig('Stack_b' + str(plot_batch) + '_e' + str(plot_exp) + '.png')
		plt.show()
	exp_end += exp0
	batch_start += batch_count[w]



