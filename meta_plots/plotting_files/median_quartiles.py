import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

"""
FILE PATHS ARE RELATIVE TO THIS FILE,
THEREFORE THIS FILE SHOULD BE RUN FROM THE DIRECTORY THIS FILE IS IN!

- Takes a CSV that includes one experimental run
- Plots median SVO ± 1 decile
"""

df = pd.read_csv('../csv/SingleCSV.csv')
m, n = df.shape

median = df['Median'].to_numpy()
above = (df['Above'].to_numpy())
below = (df['Below'].to_numpy())

plt.plot(df['Epoch'], median)
plt.fill_between(df['Epoch'], below, above, alpha=.3)
plt.xlim(0, m)
plt.title('Median SVO ± 10th percentile')
plt.xlabel('Epoch')
plt.ylabel('SVO')
plt.show()
