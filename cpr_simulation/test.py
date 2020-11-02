# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
# import random as rnd
# from datetime import datetime

# fig, (ax, ax2) = plt.subplots(nrows=2)
# xdata, ydata = [], []

# values = []
# for j in range(50):
#     val = rnd.gauss(.5, .1)
#     if val < 0:
#         val = 0
#     elif val > 1:
#         val = 1
#     values.append(val)
# height, x = np.histogram(values, bins=10, range=(0,1))
# bars = ax.bar(x[:-1], height, color='blue', align='edge', width=.1)

# line, = ax2.plot([],[],color='orange')


# def init():
#     ax.set_xlim(0,1)
#     ax2.set_xlim(0,500)
#     ax2.set_ylim(0,60)

#     changed = []
#     for bar in bars:
#         changed.append(bar)
#     changed.append(line)   
#     return changed


# def update(frame):
#     values = []
#     for j in range(50):
#         val = rnd.gauss(.5, .1)
#         if val < 0:
#             val = 0
#         elif val > 1:
#             val = 1
#         values.append(val)
#     height, x = np.histogram(values, bins=10, range=(0,1))
#     for i in range(len(bars)):
#         bars[i].set_height(height[i])

#     now = datetime.now()
#     xdata.append(now.second)
#     ydata.append(now.second)

#     line.set_data(xdata, ydata)
#     changed = []
#     for bar in bars:
#         changed.append(bar)
#     changed.append(line)
#     return changed

# ani = FuncAnimation(fig, update,
#                     interval=100,
#                     init_func=init, blit=True)
# plt.show()
