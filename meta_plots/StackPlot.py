

import numpy as np

import csv
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('RyanCSV')

m, n = df.shape


"""
plt.plot(df['Epoch'], df['A']) #, df['B'], df['C'], df['D'], df['E'])
plt.plot(df['Epoch'], df['B']) 
plt.plot(df['Epoch'], df['C'])
plt.plot(df['Epoch'], df['D']) 
plt.plot(df['Epoch'], df['E'])  
plt.xlim(0, 170)
plt.ylim(0, 600)
plt.plot(legend=['0 - .20','.21 - .40','.40 - .60','.60 - .80','.80 - 1'])
plt.show()
"""
pal = sns.color_palette("Set1")

plt.stackplot(df['Epoch'], df['A'], df['B'], df['C'], df['D'], df['E'],  labels=['0 - .20','.21 - .40','.40 - .60','.60 - .80','.80 - 1'], colors=pal, alpha=0.4)
pal = ["#9b59b6", "#e74c3c", "#34495e", "#2ecc71", "#34495e", "#2ecc71"]

plt.legend(loc='upper right')
plt.legend(title='SVO')
plt.title('Fantastic Plot')
plt.xlim(0, 20)
plt.xlabel('Epoch')
plt.ylabel('Agent Count')

plt.show()