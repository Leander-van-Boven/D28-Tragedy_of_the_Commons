import matplotlib.pyplot as plt
import pandas as pd

"""
FILE PATHS ARE RELATIVE TO THIS FILE,
THEREFORE THIS FILE SHOULD BE RUN FROM THE DIRECTORY THIS FILE IS IN!

- Takes a CSV that includes one experimental run
- Plots agent count over epochs for five 20% SVO segmentations
"""

df = pd.read_csv('../csv/SingleCSV.csv')
m, n = df.shape

plt.stackplot(
    df['Epoch'], df['A'], df['B'], df['C'], df['D'], df['E'],
    labels=['0 - .20', '.21 - .40', '.40 - .60', '.60 - .80', '.80 - 1'],
    alpha=0.4)

plt.legend(loc='upper right')
plt.legend(title='SVO')
plt.title('Stack Area Plot')
plt.xlim(0, 100)
plt.xlabel('Epoch')
plt.ylabel('Agent Count')
plt.show()
