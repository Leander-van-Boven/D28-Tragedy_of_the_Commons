

import numpy as np

import csv
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('SingleCSV')

m, n = df.shape


median = df['Median'].to_numpy()
above = (df['Above'].to_numpy())
below = (df['Below'].to_numpy())

tile = .1


plt.plot(df['Epoch'], median)
plt.fill_between(df['Epoch'], (below), (above), alpha=.3)
#plt.fill_between(df['Epoch'], (median - .2), (median + .2), alpha=.3)
plt.xlim(0, m)
plt.title('Median SVO ± 25th percentile')
plt.xlabel('Epoch')
plt.ylabel('SVO')
plt.show()


"""
total_batch = df['batch'][m-1]

SVOS = [[df['A'].to_numpy()], [df['B'].to_numpy()], [df['C'].to_numpy()], [df['D'].to_numpy()], [df['E'].to_numpy()]]


for z in range(5):
	x = np.transpose(SVOS[z])
	interval = 0
	print(x.shape)
	B_array = np.array(x)

	B_matrix = np.zeros((total_batch,int(m/total_batch)))

	w = 0
	for i in range(total_batch):
		interval = int((m/total_batch))
		B_row = B_array[w:w+interval]
		B_matrix[i][:] = np.reshape(B_row, (interval))
		w += interval

	B_np_avg = np.median(B_matrix, axis=0)
	B_np_std = np.std(B_matrix, axis=0)
	B_np_quartile = .166*B_np_avg

	#plt.plot(df['Epoch'][0:int(m/total_batch)], B_np_avg, label=str(z+1))

	#plt.fill_between(df['Epoch'][0:int(m/total_batch)], (B_np_avg - B_np_quartile), (B_np_avg + B_np_quartile), alpha=.3)


print(B_matrix.shape)
"""
"""
plt.xlim(0, 20)
plt.ylim(0, 250)
plt.legend(loc='upper right')
plt.legend(title='SVO')
plt.title('Median SVO ± Sextile (Real Science Term)')
plt.plot(legend=['0 - .20','.21 - .40','.40 - .60','.60 - .80','.80 - 1'])
plt.xlabel('Epoch')
plt.ylabel('Agent Count')
plt.show()
"""