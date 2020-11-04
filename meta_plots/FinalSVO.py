

import numpy as np

import csv
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('unimodal.csv')

m, n = df.shape

exp_number = max(df['Exp Num'])


agent_count = df['Count']


batch1 = 0
for i in df['batch']:
	if i == 1:
		batch1 += 1

print (df.columns)


batch_count = []
for k in range(12):
	batch_num = 0
	for x in df['batch']:
		if x == k + 1:
			batch_num += 1
	batch_count.append(batch_num)


batch_start = 0
exp_end = 0

plot_batch = 0
plot_exp = 1

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



