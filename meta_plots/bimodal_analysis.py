

import numpy as np

import csv
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


df = pd.read_csv('_1.csv')

m, n = df.shape
"""
exp_number = max(df['Exp Num'])


agent_count = df['Count']


batch1 = 0
for i in df['batch']:
	if i == 1:
		batch1 += 1

#print (batch1)


batch_count = []
for k in range(12):
	batch_num = 0
	for x in df['batch']:
		if x == k + 1:
			batch_num += 1
	batch_count.append(batch_num)

print(batch_count, np.sum(batch_count))

batch_start = 0
exp_end = 0

for w in range(12):
	print(batch_start, batch_start+batch_count[w])
	exp_end = 0

	for i in range(54):
		exp0 = 0
		for j in df['Exp Num'][batch_start:batch_start+batch_count[w]]:

			if j == i + df['Exp Num'][batch_start]:
				exp0 += 1

		#print(exp1+batch_start, exp1+exp0+batch_start)
		plt.rcParams["figure.figsize"] = [10, 7]
		plt.plot(df['Epoch'][exp_end+batch_start : exp_end+exp0+batch_start], agent_count[exp_end+batch_start : exp_end+exp0+batch_start], label = str(df.columns[2]) + " = " + str(df[df.columns[2]][exp_end+batch_start]) + " and " + df.columns[3] + " = " + str(round(df[df.columns[3]][exp_end+batch_start],2)) )

		exp_end += exp0

	plt.rcParams["figure.figsize"] = [10, 7]
	#plt.legend(loc='upper right')
	#plt.legend(title='Distribution')
	plt.title('Agent Count of 10 Unimodal Distributions, Batch ' + str(w+1))
	plt.xlabel('Epoch')
	plt.ylabel('Agent Count')
	plt.xlim(0, 1000)
	plt.ylim(0, 140)
	plt.savefig('FinalCount' + str(w+1) + '.png')
	plt.show()
	batch_start += batch_count[w]

"""

complete = df[df["Epoch"] == 999]

survive = complete[['svo_dist.d1.m', 'svo_dist.d1.s','svo_dist.d2.m','svo_dist.d2.s','svo_dist.d3.m','svo_dist.d3.s']]

survive.to_csv("survive.csv")








