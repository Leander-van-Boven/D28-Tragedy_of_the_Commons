import numpy as np
import time
from .agent import Agent
from .resource import Resource

class Simulation:
    """Main class that manages the agents and resource

    ...

    Attributes
    ----------
    epoch : `int`,
        the current epoch the simulation is on

    agents : `list`,
        a list containing all (alive) agents currently in the simulation
    
    result : `str`,
        set when the simulation is done, denoting the outcome of the sim
    
    resource : `Resource`,
        a resource object representing the common resource

    Methods
    -------
    getters and setters for each attribute

    `get_agent_count(min_social_value=0, max_social_value=1)`

    `add_agent(agent)`

    `remove_agent(agent)`

    `run_simulation()`
    """

    epoch = 0
    agents = []
    result = ""
    resource = None


    def __init__(self, param_dict, logger=None):
        '''Initializes the simulation with the provided parameter dict.'''

        self.params = param_dict['simulation']
        self.max_epoch = self.params['max_epoch']
        self.plot_interval = self.params['plot_interval']
        self.print_interval = self.params['print_interval']

        self.agent_distributions = param_dict['agent_distributions']
        self.resource_params = param_dict['resource']


    def get_agent_count(self, min_social_value=0, max_social_value=1):
        """Returns the amount of all agents if no params are specified.
        
        This function returns the amount of agents that have a social
        value orientation between the two parameters (inclusive).

        Parameters
        ----------
        min_social_value : float
            The lower limit of the SVO of the agent (inclusive).
        max_social_value : flaot
            The upper limit of the SVO of the agent (inclusive).
        """

        return len([agent 
                    for agent in self.agents 
                    if min_social_value 
                        <= agent.social_value_orientation 
                        <= max_social_value])


    def get_agents(self):
        '''Creates a histogram with an agent count for each unique SVO.'''

        classes = {}
        for agent in self.agents:   
          svo = agent.social_value_orientation()
          classes[svo] = classes.get(svo, 0) + 1
        return classes   


    def add_agent(self, agent):
        self.agents.append(agent)


    def remove_agent(self, agent):
        """Removes the agent from the simulation.

        #TODO determine what to do with the energy of the agent
            when the agent dies from for example age or punishment.

        Parameters
        ----------
            agent : `Agent`
                The agent to remove.
        """

        self.agents.remove(agent)


    def get_resource(self):
        return self.resource
        
    
    def get_result(self):
        return self.result


    def get_epoch(self):
        return self.epoch


    def run_simulation(self):
        """Runs the simulation.
        
        This function runs sets up the simulation and runs it.
        It makes an agent act, causes resource to replenish 
        and collects data to plot.

        Yields
        ------
        data : `tuple`,
            Tuple containing the current epoch, 
                the current amount of agents per agent distribution
                and the current amount of the common resource.
        """

        # Initialise the agents
        for dist in self.agent_distributions:
            for i in range(dist['agent_count']):
                self.add_agent(Agent(dist))

        # Initialise the resource
        self.resource = Resource(self.resource_params)

        # Initialise runtime variables
        self.epoch = 0
        self.cur_stats = ''

        # Plot starting situation
        yield self.plot_results()
        self.print_results()

        #TODO We might want to add self.epoch = 1 here.
        
        # Run the simulations for max_epoch amounts
        while (self.epoch < self.max_epoch):
            # Update the agents
            for agent in self.agents:
                agent.act(self)
                # Check whether agent has died from his actions
                if agent.energy <= 0:
                    self.remove_agent(agent)

            # Print the current stats of the simulation
            if self.epoch % self.plot_interval == 0:
                yield self.plot_results()
            if self.epoch % self.print_interval == 0:
                self.print_results()
            #TODO Implement CSV logger

            # Check whether there are still agents alive
            if self.get_agent_count() <= 0:
                self.result = ("All agents are dead :(" + 
                               "there is no hope left for the village," + 
                               "just darkness.\n" +
                               "Last stats: " + self.cur_stats)
                print(self.result)
                return

            # Update the resource and epoch
            self.resource.grow_resource() 
            np.random.shuffle(self.agents)
            self.epoch += 1

            # Uncomment below to slow down the simulation/plotting speed
            #time.sleep(0.5) 
        
        # While loop finished, maximum epoch reached
        # Some agents stayed alive
        self.result = ("Maximum epoch reached, you managed to keep " +
                       self.get_agent_count() +
                       " agents alive!\n" +
                       "Last stats: " + self.cur_stats)

    
    def plot_results(self):
        """Creates a tuple of the current stats of the simulation.
        This tuple then needs to be yielded to get plotted.
        """

        return (self.epoch,
              [self.get_agent_count(dist['min_social_value'],
                                    dist['max_social_value'])
               for dist in self.agent_distributions
              ],
               self.resource.get_amount())


    def print_results(self):
        '''Prints the current stats of the simulation.'''

        self.cur_stats = f"epoch: {self.epoch}, "
        for dist in self.agent_distributions:
            self.cur_stats += (f"{dist['label']}: " + 
                str(self.get_agent_count(dist['min_social_value'], 
                                         dist['max_social_value'])) + 
                ", ")
        self.cur_stats += f"res: {self.resource.get_amount():.2f}"
        print(self.cur_stats, end = "\r", flush = True)