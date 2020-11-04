import matplotlib.pyplot as plt
import pandas as pd

"""
FILE PATHS ARE RELATIVE TO THIS FILE,
THEREFORE THIS FILE SHOULD BE RUN FROM THE DIRECTORY THIS FILE IS IN!

This file reads a CSV file containing multiple community runs of
the same length and plots the median SVO value over epochs,
with a filled range of ± 1 decile.
"""

df = pd.read_csv('../csv/Batch3CSV.csv')
m, n = df.shape

# How many batches in the file
total_batch = df['batch'][m-1]

# Pull necessary data that was logged directly in the CSV during
# the simulation.
median = df['Median'].to_numpy()
above = df['Above'].to_numpy()
below = df['Below'].to_numpy()

# The length of each batch
interval = int(m / total_batch)
# Plot each batch
for i in range(total_batch):
    plt.plot(df['Epoch'][0:interval], median[interval * i:interval * (i+1)],
             label=str(i+1))
    plt.fill_between(df['Epoch'][0:interval],
                     below[interval * i:interval * (i+1)],
                     above[interval * i:interval * (i+1)], alpha=.3)

plt.legend(loc='upper right')
plt.legend(title='Batch')
plt.xlim(0, interval)
plt.title('Median SVO ± 25th percentile')
plt.xlabel('Epoch')
plt.ylabel('SVO')
plt.show()
