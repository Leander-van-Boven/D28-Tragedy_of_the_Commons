

import numpy as np

import csv
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('unimodal.csv')

m, n = df.shape

exp_number = max(df['Exp Num'])


"""
for i in range(15):
	LINE = 0
	LINE = df['A'][i*interval:(i+1)*interval] + df['B'][i*interval:(i+1)*interval] + df['C'][i*interval:(i+1)*interval] + df['D'][i*interval:(i+1)*interval] + df['E'][i*interval:(i+1)*interval]

	plt.plot(df['Epoch'][0:1000], LINE)


plt.legend(loc='upper right')
plt.title('Agent Count Plot for 15 SVO Distributions')
#plt.xlim(0, 20)
plt.xlim(0, 1000)
plt.xlabel('Epoch')
plt.ylabel('Agent Count')

plt.show()

"""