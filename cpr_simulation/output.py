import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import animation


class ResultsPlotter:
    """Class handling the real-time plotting

    Refer to the documentation
    (https://leander-van-boven.github.io/D28-Tragedy_of_the_Commons/
        pages/architecture/#results-plotter)
    for a brief explanation of this class. 
    And to
    (https://leander-van-boven.github.io/D28-Tragedy_of_the_Commons/
        pages/output/#real-time-plot)
    for a thorough explanation of the output. 
    """

    def __init__(self, start_agent, svo_bar_count, start_resource, fullscreen, 
                 allow_resize):
        """Sets up the real-time plot

        Parameters
        ----------
        start_agent : `int`
            The initial amount of agents, used to set the y-axis limit
            of the agent count plot (1.25*start_agent)
        svo_bar_count : `int`
            The amount of bars to show in the real-time histogram
        start_resource : `float`
            The amount of starting resources, used to set y-axis limit 
            of the resource plot (1.25*start_resource)
        fullscreen : `bool`
            Whether to run the plot in maximized window 
            (if backend supports it)
        allow_resize : `bool`
            Whether to enable resizing without resetting the plot
        """

        # Set parameters to use during initialisation
        self.start_agent = start_agent
        self.xdata, self.yagent = [], []
        self.yresource, self.limitresource, self.unlimitresource = [], [], []
        self.start_resource = start_resource
        self.blit = not allow_resize

        # Create figure
        self.fig = plt.figure(figsize=(10, 7))
        self.ax_agent = plt.subplot(222)
        self.ax_resource = plt.subplot(224)
        self.ax_svo = plt.subplot(121)
        self.fig.tight_layout(h_pad=3, w_pad=2, pad=2)

        # Maximize plot if required and backend supports it
        if fullscreen:
            backend = matplotlib.get_backend().lower()
            if backend == 'tkagg':
                mng = plt.get_current_fig_manager()
                mng.window.state('zoomed')
            elif backend == 'qt5agg' or backend == 'qt4agg':
                self.fig.canvas.manager.window.showMaximized()
            elif backend == 'wxagg': # Not tested
                print('WARNING: ' +
                      'maximize plot has not been tested yet on this backend.')
                try:
                    mng = plt.get_current_fig_manager()
                    mng.frame.Maximize(True)
                except:
                    print('Failed to maximize plot')

        # Setup agent subplot
        self.agent_line, = self.ax_agent.plot([], [], lw=2, color='blue', 
                                              label='Agent Count')
        self.ax_agent.set_title('Real time plot of agent count')
        self.ax_agent.set_ylabel('agent count')
        self.ax_agent.set_xlabel('epochs')
        self.ax_agent.legend()
        self.ax_agent.grid()

        # Setup svo subplot
        _, _, self.svo_bars = self.ax_svo.hist(
            [], bins=svo_bar_count, range=(0, 1), color='blue')
        self.ax_svo.set_title('Real time SVO distribution')
        self.ax_svo.set_ylabel('fraction of agent count')
        self.ax_svo.set_xlabel('SVO')
        self.ax_svo.set_xticks(np.arange(0, 1, step=1 / (svo_bar_count / 4)))

        # Setup resource subplot
        self.resource_line, = self.ax_resource.plot(
            [], [], lw=2, color='green', label='Resource Count')
        self.res_limit_line, = self.ax_resource.plot(
            [], [], lw=1, color='red', linestyle='--', label='Resource Limit')
        self.res_unlimit_line, = self.ax_resource.plot(
            [], [], lw=1, color='purple', linestyle='--', 
            label='Resource Unlimit')
        self.ax_resource.set_title('Real time plot of resource supply')
        self.ax_resource.set_ylabel('resource supply')
        self.ax_resource.set_xlabel('epochs')
        self.ax_resource.legend()
        self.ax_resource.grid()

    def init_plot(self):
        """Final initialisation of the plots"""

        # Set axis ranges
        self.ax_agent.set_ylim(-.1, self.start_agent * 1.25)
        self.ax_agent.set_xlim(0, 10)
        self.ax_svo.set_ylim(0, 1)
        self.ax_svo.set_xlim(0, 1)
        self.ax_resource.set_ylim(-.1, self.start_resource * 1.25)
        self.ax_resource.set_xlim(0, 10)

        # Reset all data
        del self.xdata[:]
        del self.yagent[:]
        del self.yresource[:]
        del self.limitresource[:]
        del self.unlimitresource[:]

        # Setup all lines
        self.agent_line.set_data(self.xdata, self.yagent)
        self.resource_line.set_data(self.xdata, self.yresource)
        self.res_limit_line.set_data(self.xdata, self.limitresource)
        self.res_unlimit_line.set_data(self.xdata, self.unlimitresource)

        # Return updated actors
        initialised = [self.agent_line, self.resource_line, self.res_limit_line, 
                       self.res_unlimit_line]
        for bar in self.svo_bars:
            initialised.append(bar)
        return initialised

    def update(self, data):
        """Updates the plot
        This method is called each time the data generator yields data.

        Parameters
        ----------
        data : `tuple`,
            Tuple containing the current epoch, 
                the current amount of agents alive,
                a list of all SVO's of the currently alive agents,
                the current amount of resources,
                the current resource limit value,
                the current resource unlimit value.
        """

        # Append the data to the correct lists
        t, a, s, r, l, u = data
        self.xdata.append(t)
        self.yagent.append(a)
        counts, _ = np.histogram(s, bins=len(self.svo_bars), range=(0, 1))
        total = sum(counts)
        counts = [c / total for c in counts] if total > 0 else len(counts) * [0]
        self.yresource.append(r)
        self.limitresource.append(l)
        self.unlimitresource.append(u)

        # Resize window of all plots if current epoch exceeds x_max        
        xmin, xmax = self.ax_agent.get_xlim()
        if t >= xmax:
            self.ax_agent.set_xlim(xmin, 2 * xmax)
            self.ax_resource.set_xlim(xmin, 2 * xmax)
            self.ax_agent.figure.canvas.draw()
            self.ax_resource.figure.canvas.draw()
        ymin, ymax = self.ax_agent.get_ylim()
        # Increase y-axis limit of agent plot if current exceeds y_max
        if a > ymax:
            self.ax_agent.set_ylim(ymin, 2 * ymax)
            self.ax_agent.figure.canvas.draw()
        ymin, ymax = self.ax_resource.get_ylim()
        # Increase y axis limit
        if r > ymax:
            self.ax_resource.set_ylim(ymin, 2 * ymax)
            self.ax_resource.figure.canvas.draw()

        # Update the actual lines
        self.agent_line.set_data(self.xdata, self.yagent)
        for i, bar in enumerate(self.svo_bars):
            bar.set_height(counts[i])
        self.resource_line.set_data(self.xdata, self.yresource)
        self.res_limit_line.set_data(self.xdata, self.limitresource)
        self.res_unlimit_line.set_data(self.xdata, self.unlimitresource)
        updated = [self.agent_line, self.resource_line, self.res_limit_line, 
                   self.res_unlimit_line]
        for bar in self.svo_bars:
            updated.append(bar)
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
            blit=self.blit, interval=1, repeat=False,
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