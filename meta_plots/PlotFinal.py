

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


batch_count = []
for k in range(12):
	batch_num = 0
	for x in df['batch']:
		if x == k + 1:
			batch_num += 1
	batch_count.append(batch_num)

batch_start = 0
exp_end = 0

for w in range(12):

	exp_end = 0

	for i in range(10):
		exp0 = 0
		for j in df['Exp Num'][batch_start:batch_start+batch_count[w]]:

			if j == i + df['Exp Num'][batch_start]:
				exp0 += 1

		#print(exp1+batch_start, exp1+exp0+batch_start)
		plt.rcParams["figure.figsize"] = [10, 5]
		plt.plot(df['Epoch'][exp_end+batch_start : exp_end+exp0+batch_start], agent_count[exp_end+batch_start : exp_end+exp0+batch_start], label = "Mean = " + str(df[df.columns[2]][exp_end+batch_start]) + " and STD = " + str(round(df[df.columns[3]][exp_end+batch_start],2)) )

		exp_end += exp0

	plt.rcParams["figure.figsize"] = [10, 5]
	plt.legend(loc='upper right')
	plt.legend(title='Unimodal Distribution')
	plt.title('Agent Count of 10 Unimodal Distributions, Batch ' + str(w+1))
	plt.xlabel('Epoch')
	plt.ylabel('Agent Count')
	plt.xlim(0, 1000)
	plt.ylim(0, 100)
	plt.savefig('FinalCount' + str(w+1) + '.png')
	plt.show()
	batch_start += batch_count[w]




"""
color_map = [
"#57bb8a",
"#63b682",
"#73b87e",
"#84bb7b",
"#94bd77",
"#a4c073",
"#b0be6e",
"#c4c56d",
"#d4c86a",
"#e2c965",
"#f5ce62",
"#f3c563",
"#e9b861",
"#e6ad61",
"#ecac67",
"#e9a268",
"#e79a69",
"#e5026b",
"#e2886c",
"#e0816d",
"#dd776e"
]
"""

