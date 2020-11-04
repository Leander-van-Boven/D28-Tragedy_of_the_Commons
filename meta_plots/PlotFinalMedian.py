

import numpy as np

import csv
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('unimodal.csv')

m, n = df.shape

exp_number = max(df['Exp Num'])


agent_count = df['A'] + df['B'] + df['C'] + df['D'] + df['E']


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

	for i in range(10):
		exp0 = 0
		for j in df['Exp Num'][batch_start:batch_start+batch_count[w]]:

			if j == i + df['Exp Num'][batch_start]:
				exp0 += 1

		#print(exp1+batch_start, exp1+exp0+batch_start)
		plt.rcParams["figure.figsize"] = [10, 7]
		plt.plot(df['Epoch'][exp_end+batch_start : exp_end+exp0+batch_start], df['Median'][exp_end+batch_start : exp_end+exp0+batch_start], label = str(df[df.columns[2]][exp_end+batch_start]) + ",  " + str(round(df[df.columns[3]][exp_end+batch_start],2)) )
		plt.fill_between(df['Epoch'][exp_end+batch_start : exp_end+exp0+batch_start], df['Below'][exp_end+batch_start : exp_end+exp0+batch_start], df['Above'][exp_end+batch_start : exp_end+exp0+batch_start], alpha=.3)

		exp_end += exp0

	plt.rcParams["figure.figsize"] = [10, 7]
	plt.legend(loc='upper right')
	plt.legend(title='Intitial Mean SVO, STD')
	plt.title('SVO Median ± Decile of 10 Unimodal Distributions, Batch ' + str(w+1))
	plt.xlabel('Epoch')
	plt.ylabel('SVO')
	plt.xlim(0, 100)
	plt.ylim(0, 1)
	#plt.savefig('FinalMedian' + str(w+1) + '.png')
	plt.show()
	batch_start += batch_count[w]



