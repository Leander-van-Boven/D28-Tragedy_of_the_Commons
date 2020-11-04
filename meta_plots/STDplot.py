

import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt



df = pd.read_csv('BatchCSV')

m, n = df.shape

total_batch = df['batch'][m-1]


SVOS = [[df['A'].to_numpy()], [df['B'].to_numpy()], [df['C'].to_numpy()], [df['D'].to_numpy()], [df['E'].to_numpy()]]


for z in range(5):
	x = np.transpose(SVOS[z])
	interval = 0

	B_array = np.array(x)

	B_matrix = np.zeros((total_batch,int(m/total_batch)))

	w = 0
	for i in range(total_batch):
		interval = int((m/total_batch))
		B_row = B_array[w:w+interval]
		B_matrix[i][:] = np.reshape(B_row, (interval))
		w += interval

	B_np_avg = np.mean(B_matrix, axis=0)
	B_np_std = np.std(B_matrix, axis=0)


	plt.plot(df['Epoch'][0:int(m/total_batch)], B_np_avg, label=str((round(z*.2, 1) )) + "-" + str((round((z+1)*.2,1))) )

	plt.fill_between(df['Epoch'][0:int(m/total_batch)], (B_np_avg - .25*B_np_std), (B_np_avg + .25*B_np_std), alpha=.3)


plt.xlim(0, interval)
plt.ylim(0, 200)
plt.legend(loc='upper right')
plt.legend(title='SVO')
plt.title('Mean SVO ± 0.25 * Standard Deviation')
plt.plot(legend=['0 - .20','.21 - .40','.40 - .60','.60 - .80','.80 - 1'])
plt.xlabel('Epoch')
plt.ylabel('Agent Count')
plt.show()
