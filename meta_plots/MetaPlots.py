
import numpy as np

import csv
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('NewCSVTest')
print(df.shape)

m, n = df.shape



pal = sns.color_palette("Set1")

plt.stackplot(df['Epoch'], df['A'], df['B'], df['C'], df['D'], df['E'],  labels=['0 - .20','.21 - .40','.40 - .60','.60 - .80','.80 - 1'], colors=pal, alpha=0.4)

pal = ["#9b59b6", "#e74c3c", "#34495e", "#2ecc71", "#34495e", "#2ecc71"]

plt.legend(loc='upper right')

plt.legend(title='SVO')

plt.title('Fantastic Plot')

plt.xlim(0, 20)

plt.xlabel('Epoch')

plt.ylabel('Agent Count')

#plt.set_title('style: {!r}'.format(sty), color='C0')


#plt.plot(df['Epoch'][1000:1050], df['proself'][1000:1050])
#plt.plot(df['Epoch'][2000:2050], df['proself'][2000:2050])
#plt.plot(df['Epoch'][2000:2050], avg_proself)


plt.show()