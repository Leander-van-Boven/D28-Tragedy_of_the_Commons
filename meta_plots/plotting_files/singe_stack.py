

import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



"""
- Takes a CSV that includes one experimental run
- Plots agent count over epochs for five 20% SVO segmentations
"""

df = pd.read_csv('SingleCSV')

m, n = df.shape


pal = sns.color_palette("Set1")

plt.stackplot(df['Epoch'], df['A'], df['B'], df['C'], df['D'], df['E'],  labels=['0 - .20','.21 - .40','.40 - .60','.60 - .80','.80 - 1'], alpha=0.4)
pal = ["#9b59b6", "#e74c3c", "#34495e", "#2ecc71", "#34495e", "#2ecc71"]

plt.legend(loc='upper right')
plt.legend(title='SVO')
plt.title('Stack Area Plot')
#plt.xlim(0, 20)
plt.xlim(0, 100)
plt.xlabel('Epoch')
plt.ylabel('Agent Count')

plt.show()