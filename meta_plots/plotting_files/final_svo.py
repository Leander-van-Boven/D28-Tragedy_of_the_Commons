

import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


"""
- This file operates on a CSV file containing multiple batches of multiple experiments.  
- Community runs do not need to be of the same length.
- Outputs a SINGLE multi-line plot of five 20% SVO segmentations 
- Select experiment with plot_batch and plot_exp below
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
plot_batch = 0
plot_exp = 1


# Loops through all 12 batches
# Loops through all ten experiments in each batch
# Counts length of each experiment
# Plots multiline agent counts for 5 SVO ranges
# Only plots selected experiment
# 12 Plots total, with autosave option
# Note for bimodal and trimodal plots, the amount of experiments needs to be changed to 54 for bimodal and 2160 for trimodal (not recommended)
for w in range(12):

	exp_end = 0

	for i in range(10):
		exp0 = 0
		for j in df['Exp Num'][batch_start:batch_start+batch_count[w]]:

			if j == i + df['Exp Num'][batch_start]:
				exp0 += 1

		if w == plot_batch and i == plot_exp:
			plt.rcParams["figure.figsize"] = [10, 7]
			pal = sns.color_palette("Set1")

			A = 7
			for z in range(5):
				A += z
				print(df.columns[A])
				plt.plot(df['Epoch'][exp_end+batch_start : exp_end+exp0+batch_start], df[df.columns[A]][exp_end+batch_start : exp_end+exp0+batch_start], label=str(round(z*.20,2)) + " - " + str(round((z+1)*.20,2))) 


		exp_end += exp0
		

	if w == plot_batch:
		plt.legend(loc='upper right')
		plt.legend(title='SVO')
		plt.title('SVO Segmentation Batch ' + str(w+1) + ': Mean = '+ str(df[df.columns[2]][exp_end+batch_start]) + " and STD = " + str(round(df[df.columns[3]][exp_end+batch_start],2)))
		plt.xlim(0, 1000)
		plt.ylim(0, 20)
		plt.xlabel('Epoch')
		plt.ylabel('Agent Count')

		plt.show()

	batch_start += batch_count[w]



