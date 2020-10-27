

import numpy as np

import csv
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('Batch3CSV')

m, n = df.shape

total_batch = df['batch'][m-1]


median = df['Median'].to_numpy()
above = (df['Above'].to_numpy())
below = (df['Below'].to_numpy())


interval = int(m/total_batch)


for i in range(total_batch):

	plt.plot(df['Epoch'][0:interval], median[interval*i:interval*(i+1)], label = str(i+1))
	plt.fill_between(df['Epoch'][0:interval], (below)[interval*i:interval*(i+1)], (above)[interval*i:interval*(i+1)], alpha=.3)




#plt.fill_between(df['Epoch'], (median - .2), (median + .2), alpha=.3)
plt.legend(loc='upper right')
plt.legend(title='Batch')
plt.xlim(0, interval)
plt.title('Median SVO ± 25th percentile')
plt.xlabel('Epoch')
plt.ylabel('SVO')
plt.show()






#########
