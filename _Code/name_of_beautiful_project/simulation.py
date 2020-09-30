import numpy as np
import time
from .agent import Agent
from .resource import Resource

class Simulation:
    """Main class that manages the agents and resource

    ...

    Attributes
    ----------
    epoch : `int`\\
        The current epoch the simulation is on

    agents : `list`\\
        A list containing all (alive) agents currently in the simulation
    
    result : `str`\\
        Set when the simulation is done, denoting the outcome of the sim
    
    resource : `Resource`\\
        A resource object representing the common resource

    Methods
    -------
    - getters and setters for each attribute

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

        self.agent_params = param_dict['agent']
        self.resource_params = param_dict['resource']


    #--- Getters & Setters
    def get_agent_count(self, min_social_value=0, max_social_value=1):
        """Returns the amount of all agents if no params are specified
        
        This function returns the amount of agents that have a social
        value orientation between the two parameters (inclusive).

        Parameters
        ----------
        min_social_value : float
            the lower limit of the SVO of the agent (inclusive)
        max_social_value : flaot
            the upper limit of the SVO of the agent (inclusive)
        """

        return len([agent 
                    for agent in self.agents 
                    if min_social_value 
                        <= agent.social_value_orientation 
                        <= max_social_value])


    def get_agents(self):
        '''Creates a histogram with an agent count for each unique SVO'''

        classes = {}
        for agent in self.agents:   
          svo = agent.social_value_orientation()
          classes[svo] = classes.get(svo, 0) + 1
        return classes   


    def add_agent(self, agent):
        self.agents.append(agent)


    def remove_agent(self, agent):
        self.agents.remove(agent)

    
    def get_result(self):
        return self.result


    def get_epoch(self):
        return self.epoch


    #--- Main methods
    def run_simulation(self):
        """Run the simulation
        
        This function runs sets up the simulation and runs it.
        It makes an agent act, causes resource to replenish 
        and collects data to plot.

        Yields
        ------
        data : tuple
            a tuple containing the current epoch, 
            current amount of agents for each agent distribution,
            current amount of the common resource
        """

        self.epoch = 0

        # Initialise the agents
        for dist in self.params['agent_distributions']:
            for i in range(dist['agent_count']):
                self.add_agent(Agent(self.agent_params, dist))

        # Initialise the resource
        self.resource = Resource(self.resource_params)
        
        # Run the simulations for max_epoch amounts
        while (self.epoch < self.max_epoch):
            # Print the current stats of the simulation
            # Yield results for the plot
            if self.epoch % self.plot_interval == 0:
                yield (self.epoch,
                      [self.get_agent_count(dist['min_social_value'],
                                            dist['max_social_value'])
                        for dist in self.params['agent_distributions']
                      ],
                      self.resource.get_amount())
            # Print results in console
            if self.epoch % self.print_interval == 0:
                print((f"epoch: {self.epoch}, " +
                       f"res: {self.resource.get_amount():.2f}, " + 
                       f"self: {self.get_agent_count(.5, False)}, " + 
                       f"social: {self.get_agent_count(.5, True)}"), 
                      end = "\r", flush = True)

            # Update the agents
            for agent in self.agents:
                agent.act(self, self.resource)
                # Check whether agent has died from his actions
                if agent.energy <= 0:
                    self.remove_agent(agent)
                
            # Check whether there are still agents alive
            if self.get_agent_count() <= 0:
                self.result = ("All agents are dead :(" + 
                              "there is no hope left for the village," + 
                              "just darkness.")
                print(self.result)
                return

            # Update the resource and epoch
            self.resource.growth_func(0) 
            self.epoch += 1

            # Uncomment below to slow down the simulation/plotting speed
            #time.sleep(0.5) 
        
        self.result = ("Maximum epoch reached, you managed to keep " +
                       self.get_agent_count() +
                       " agents alive!")