

import numpy as np

import csv
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('Batch3CSV')

m, n = df.shape



total_batch = df['batch'][m-1]

"""
SVOS = [[df['A'].to_numpy()], [df['B'].to_numpy()], [df['C'].to_numpy()], [df['D'].to_numpy()], [df['E'].to_numpy()]]


B_sum = np.zeros((m, 1))
B_matrix = np.zeros((5, m))

for z in range(5):
	x = np.transpose(SVOS[z])
	interval = 0

	B_array = np.array(x)
	print(B_array.shape)

	B_sum += B_array

	B_matrix[z][:] = np.reshape(B_array, 150)

#	w = 0
#	for i in range(total_batch):
#		interval = int((m/total_batch))
#		B_row = B_array[w:w+interval]
#		B_matrix[i][:] = np.reshape(B_row, (interval))
#		w += interval


B_np_std = .25*np.reshape(np.std(B_matrix, axis=0), (150))

B_array = np.reshape(B_array, (150))
"""
bl = int(m/total_batch) # batch length

B_mean = df['Mean'].to_numpy()
B_std = .25*df['STD'].to_numpy()



plt.plot(df['Epoch'][0:bl], B_mean[0*bl:1*bl], label='Batch1')
plt.plot(df['Epoch'][0:bl], B_mean[1*bl:2*bl], label='Batch2')
plt.plot(df['Epoch'][0:bl], B_mean[2*bl:3*bl], label='Batch3')

plt.fill_between(df['Epoch'][0:bl], B_mean[0*bl:1*bl] - B_std[0*bl:1*bl], B_mean[0*bl:1*bl] + B_std[0*bl:1*bl], alpha=.3)
plt.fill_between(df['Epoch'][0:bl], B_mean[1*bl:2*bl] - B_std[1*bl:2*bl], B_mean[1*bl:2*bl] + B_std[1*bl:2*bl], alpha=.3)
plt.fill_between(df['Epoch'][0:bl], B_mean[2*bl:3*bl] - B_std[2*bl:3*bl], B_mean[2*bl:3*bl] + B_std[2*bl:3*bl], alpha=.3)

plt.title('Agent Count ± .25*STD')
plt.legend(loc='upper right')
plt.legend(title='SVO')
plt.plot(legend=['Batch1','Batch2','Batch3'])
plt.xlim(0, bl)

#plt.fill_between(df['Epoch'][0:int(m/total_batch)], (B_array[int(0*m/total_batch):int(1*m/total_batch)] - B_np_std[int(0*m/total_batch):int(1*m/total_batch)]), (B_array[int(0*m/total_batch):int(1*m/total_batch)] + B_np_std[int(0*m/total_batch):int(1*m/total_batch)]),  alpha=.3)

#plt.plot(df['Epoch'][0:int(m/total_batch)], B_np_std[int(0*m/total_batch):int(1*m/total_batch)], label="hello")
#plt.plot(df['Epoch'][0:int(m/total_batch)], B_np_std[int(1*m/total_batch):int(2*m/total_batch)], label="hello")
#plt.plot(df['Epoch'][0:int(m/total_batch)], B_np_std[int(2*m/total_batch):int(3*m/total_batch)], label="hello")

plt.show()

"""
for z in range(5):
	x = np.transpose(SVOS[z])
	interval = 0

	B_array = np.array(x)

	B_matrix = np.zeros((total_batch,int(m/total_batch)))

	w = 0
	for i in range(10):
		interval = int((m/total_batch))
		B_row = B_array[w:w+interval]
		B_matrix[i][:] = np.reshape(B_row, (interval))
		w += interval

	B_np_avg = np.median(B_matrix, axis=0)
	B_np_std = np.std(B_matrix, axis=0)
	B_np_quartile = .166*B_np_avg

	plt.plot(df['Epoch'][0:int(m/total_batch)], B_np_avg, label=str(z+1))

	plt.fill_between(df['Epoch'][0:int(m/total_batch)], (B_np_avg - B_np_quartile), (B_np_avg + B_np_quartile), alpha=.3)


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