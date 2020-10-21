import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import animation

class ResultsPlotter:
    def __init__(self, max_agent, svo_bar_count, max_resource):        
        """Sets up the real-time plot.

        Parameters
        ----------
        agent_distributions : `list`,
            A list containing the different agent groups.

        max_resource : `int`,
            The maximum amount of resource there can be,
                used to set the y-axis range appropiately.
        """

        self.max_agent = max_agent
        #self.svo_bar_count = svo_bar_count
        self.max_resource = max_resource
        self.xdata, self.yagent, self.yresource = [], [], []

        # Create figure
        self.fig, (self.ax_agent, self.ax_svo, self.ax_resource) = plt.subplots(
            nrows=3, figsize=(16,8))
        self.fig.tight_layout(h_pad=3, pad=4)

        # Setup agent subplot
        self.agent_line, = self.ax_agent.plot([], [], lw=2, color='blue')
        self.ax_agent.set_title('Real time plot of agent count')
        self.ax_agent.set_ylabel('agent count')
        self.ax_agent.set_xlabel('epochs')
        #self.ax_agent.legend()
        self.ax_agent.grid()

        # Setup svo subplot
        _, ticks, self.svo_bars = self.ax_svo.hist(
            [], bins=svo_bar_count, range=(0,1), color='blue')
        self.ax_svo.set_title('Real time SVO distribution')
        self.ax_svo.set_ylabel('agent count')
        self.ax_svo.set_xlabel('SVO')
        self.ax_svo.set_xticks(ticks)
        #self.ax_svo.grid()
        
        # Setup resource subplot
        self.resource_line, = self.ax_resource.plot([], [], lw=2, color='green')
        self.ax_resource.set_title('Real time plot of resource supply')
        self.ax_resource.set_ylabel('resource supply')
        self.ax_resource.set_xlabel('epochs')        
        self.ax_resource.grid()


    def init_plot(self):
        '''Final initialisation of the plots'''

        # Set axis ranges
        self.ax_agent.set_ylim(-.1, self.max_agent + 1)
        self.ax_agent.set_xlim(0, 10)
        self.ax_svo.set_ylim(0, 1)
        self.ax_svo.set_xlim(0, 1)
        self.ax_resource.set_ylim(-.1, self.max_resource + 1)
        self.ax_resource.set_xlim(0, 10)

        # Reset all data
        del self.xdata[:]
        del self.yagent[:]
        del self.yresource[:]
        self.zero_flag = 0
   
        self.agent_line.set_data(self.xdata, self.yagent)     
        self.resource_line.set_data(self.xdata, self.yresource)

        initialised = [self.agent_line, self.resource_line]
        [initialised.append(bar) for bar in self.svo_bars]
        return initialised


    def update(self, data):
        """Updates the plot
        This method is called each time the data generator yields data.

        Parameters
        ----------
        data : `tuple`,
            Tuple containing the current epoch, 
                the current amount of agents per agent distribution
                and the current amount of the common resource.
        """

        # Append the data to the correct lists
        t, a, s, r = data
        # print('===')
        # print('t', t)
        # print('a', a)
        # print('s', s)
        # print('r', r)
        self.xdata.append(t)
        self.yagent.append(a)
        counts, _ = np.histogram(s, bins=len(self.svo_bars), range=(0,1))
        total = sum(counts)
        counts = [count/total for count in counts]
        self.yresource.append(r)

        # Resize window if current epoch exceeds x_max        
        xmin, xmax = self.ax_agent.get_xlim()
        if t >= xmax:
            self.ax_agent.set_xlim(xmin, 2*xmax)
            self.ax_resource.set_xlim(xmin, 2*xmax)
            self.ax_agent.figure.canvas.draw()
            self.ax_resource.figure.canvas.draw()
        ymin, ymax = self.ax_agent.get_ylim()
        # Increase y axis limit if current value exceeds y_max
        if a > ymax:
            self.ax_agent.set_ylim(ymin, 2*ymax)
            self.ax_agent.figure.canvas.draw()
        ymin, ymax = self.ax_resource.get_ylim()
        if r > ymax:
            self.ax_resource.set_ylim(ymin, 2*ymax)
            self.ax_resource.figure.canvas.draw()

        # Update the actual lines
        self.agent_line.set_data(self.xdata, self.yagent)
        for i, bar in enumerate(self.svo_bars):
            bar.set_height(counts[i])
        self.resource_line.set_data(self.xdata, self.yresource)
        #self.save_fig('.lastplot.pdf')
        updated = [self.agent_line, self.resource_line]
        [updated.append(bar) for bar in self.svo_bars]
        return updated


    def start_printer(self, data_gen):
        """Creates the real-time plot and shows it, waiting for data.

        Parameters
        ----------
        data_gen : `function`
            The function that yields the data to plot.
        """

        self.animation = animation.FuncAnimation(
            self.fig, self.update, data_gen, 
            blit=True, interval=1, repeat=False, 
            init_func=self.init_plot)
        plt.show()
        

    def save_fig(self, path):
        """Saves the plot to the specified path.

        Parameters
        ----------
        path : `str`,
            The path to save the plot to.
        """

        plt.savefig(path)