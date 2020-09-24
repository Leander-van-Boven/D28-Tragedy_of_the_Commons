import numpy as np
import matplotlib
#matplotlib.use('GTKAgg')
from matplotlib import pyplot as plt
from matplotlib import animation

class ResultsPrinter:
    def __init__(self):
        self.fig, (self.ax_agent, self.ax_resource) = plt.subplots(nrows=2, figsize=(16,8))
        self.fig.tight_layout(h_pad=3, pad=4)

        # setup ax_agent
        self.agent_line, = self.ax_agent.plot([], [], lw=1, color='red')
        self.ax_agent.set_title('Real time plot of agent count')
        self.ax_agent.set_ylabel('agent count')
        self.ax_agent.set_xlabel('epochs')
        self.ax_agent.grid()
        
        # setup ax_resource
        self.resource_line, = self.ax_resource.plot([], [], lw=1, color='green')
        self.ax_resource.set_title('Real time plot of resource supply')
        self.ax_resource.set_ylabel('resource supply')
        self.ax_resource.set_xlabel('epochs')        
        self.ax_resource.grid()

        self.xdata, self.yagents, self.yresource = [], [], []


    def init_plot(self):
        self.ax_agent.set_ylim(-1.1, 1.1)
        self.ax_agent.set_xlim(0, 10)
        self.ax_resource.set_ylim(-1.1, 1.1)
        self.ax_resource.set_xlim(0, 10)
        del self.xdata[:]
        del self.yagents[:]
        del self.yresource[:]
        self.agent_line.set_data(self.xdata, self.yagents)
        self.resource_line.set_data(self.xdata, self.yresource)
        return self.agent_line, self.resource_line


    def update(self, data):
        t, a, r = data
        self.xdata.append(t)
        self.yagents.append(a)
        self.yresource.append(r)

        xmin, xmax = self.ax_agent.get_xlim()
        if t >= xmax:
            self.ax_agent.set_xlim(xmin, 2*xmax)
            self.ax_resource.set_xlim(xmin, 2*xmax)
            self.ax_agent.figure.canvas.draw()
            self.ax_resource.figure.canvas.draw()

        self.agent_line.set_data(self.xdata, self.yagents)
        self.resource_line.set_data(self.xdata, self.yresource)
        return self.agent_line, self.resource_line


    def start_printer(self, data_gen):
        ani = animation.FuncAnimation(self.fig, self.update, data_gen, blit=False, interval=1, repeat=False, init_func=self.init_plot)
        plt.show()
