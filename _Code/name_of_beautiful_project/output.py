import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import animation

class ResultsPrinter:
    def __init__(self, agent_distributions: [], max_resource):        
        """Initializes the real-time plot

        Parameters
        ----------
        agent_distributions : `list`,
            A list containing the different agent groups

        max_resource : `int`,
            [description]
        """

        # Initialize self properties
        self.max_agent = sum(dist['agent_count'] 
                             for dist in agent_distributions)
        self.max_resource = max_resource
        self.xdata, self.yagents, self.yresource = [], [[]], []

        # Create figure
        self.fig, (self.ax_agent, self.ax_resource) = plt.subplots(
            nrows=2, figsize=(16,8))
        self.fig.tight_layout(h_pad=3, pad=4)

        # Setup agent subplot
        styles = ['--', ':', ',']
        self.agent_lines = []
        for dist in agent_distributions:
            self.agent_lines.append(
                self.ax_agent.plot([], [], 
                                   lw=2, label=dist['label'], 
                                   linestyle=dist['line_style'])[0])
        self.ax_agent.set_title('Real time plot of agent count')
        self.ax_agent.set_ylabel('agent count')
        self.ax_agent.set_xlabel('epochs')
        self.ax_agent.legend()
        self.ax_agent.grid()
        
        # Setup resource subplot
        self.resource_line, = self.ax_resource.plot([], [], lw=3, color='green')
        self.ax_resource.set_title('Real time plot of resource supply')
        self.ax_resource.set_ylabel('resource supply')
        self.ax_resource.set_xlabel('epochs')        
        self.ax_resource.grid()


    def init_plot(self):
        self.ax_agent.set_ylim(-.1, self.max_agent + 1)
        self.ax_agent.set_xlim(0, 10)
        self.ax_resource.set_ylim(-.1, self.max_resource + 1)
        self.ax_resource.set_xlim(0, 10)

        del self.xdata[:]
        self.yagents = [[] for i in range(len(self.agent_lines))]
        del self.yresource[:]
        self.zero_flags = np.repeat(0, len(self.agent_lines))

        for agent_line in self.agent_lines:
            agent_line.set_data(self.xdata, [])           
        self.resource_line.set_data(self.xdata, self.yresource)

        return self.agent_lines, self.resource_line


    def update(self, data):
        """[summary]

        Arguments:
            data {[type]} -- [description]

        Returns:
            [type] -- [description]
        """

        t, a, r = data
        self.xdata.append(t)
        for i in range(len(a)):
            if a[i] == 0 and self.zero_flags[i] == 0:
                self.zero_flags[i] = 1
                self.ax_agent.axvline(x=t, c=self.agent_lines[i].get_c())
            self.yagents[i].append(a[i]) 
        self.yresource.append(r)

        xmin, xmax = self.ax_agent.get_xlim()
        if t >= xmax:
            self.ax_agent.set_xlim(xmin, 2*xmax)
            self.ax_resource.set_xlim(xmin, 2*xmax)
            self.ax_agent.figure.canvas.draw()
            self.ax_resource.figure.canvas.draw()

        #self.agent_line.set_data(self.xdata, self.yagents)
        for i in range(len(self.yagents)):
            self.agent_lines[i].set_data(self.xdata, self.yagents[i])
        self.resource_line.set_data(self.xdata, self.yresource)

        return self.agent_lines, self.resource_line


    def start_printer(self, data_gen):
        """[summary]

        Args:
            data_gen ([type]): [description]
        """

        ani = animation.FuncAnimation(self.fig, self.update, data_gen, 
                                      blit=False, interval=1, repeat=False, 
                                      init_func=self.init_plot)
        plt.show()
