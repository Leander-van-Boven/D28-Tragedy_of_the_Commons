

import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('SingleCSV')

m, n = df.shape


median = df['Median'].to_numpy()
above = (df['Above'].to_numpy())
below = (df['Below'].to_numpy())


plt.plot(df['Epoch'], median)
plt.fill_between(df['Epoch'], (below), (above), alpha=.3)
plt.xlim(0, m)
plt.title('Median SVO ± 25th percentile')
plt.xlabel('Epoch')
plt.ylabel('SVO')
plt.show()
