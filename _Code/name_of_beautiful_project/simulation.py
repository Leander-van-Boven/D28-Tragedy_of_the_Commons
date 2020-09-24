import numpy as np
from agent import Agent
from resource import Resource

class Simulation:
    epoch = 0

    initial_agent_count = 100
    agent_count = 0
    agents = []

    resource = None

    def __init__(self, param_dict, logger=None):
        self.params = param_dict['simulation']
        self.initial_agent_count = params['initial_agents_count']
        self.agent_params = param_dict['agent']
        self.resource_params = param_dict['resource']
        super().__init__()

    #--- Getters & Setters
    def get_initial_agent_count(self):
        return self.initial_agent_count

    def set_initial_agent_count(self, count):
        self.initial_agent_count = count

    def get_agent_count(self):
        return len(self.agents)

    def set_agent(self, agent):
        self.agents.append(agent)

    def get_initial_agent_count(self):
        return self.initial_agent_count

    def set_initial_agent_count(self, count):
        self.initial_agent_count = count

    def remove_agent(self, agent):
        self.agents.remove(agent)


    #--- Main methods
    def run_simulation(self, agent_dict, resource_dict, max_epoch = 1000000):
        self.agent_count = self.initial_agent_count
        self.epoch = 0
        agents_alive = 0
        resource_left = 0

        # Initialise the agents
        for i in range(self.agent_count):    
            agent = Agent(self.agent_params)
            set_agent(agent)

        # Initialise the resource
        resource = Resource(self.resource_params)
        
        # Run the simulations for max_epoch amounts
        while (self.epoch < max_epoch):
            # Update the agents
            for agent in self.agents:
                agent.do_cycle(self.resource)
                if agent.get_life() <= 0:
                    remove_agent(agent) # Agent is dead, do we remove now/later/before?

            # Update the resource
            Resource.growth_func(0) # 0: r = r * coeff, 1: r += r, # 2: r += sqrt(max - current) 

            # Get the information about the simulation
            agents_alive = get_agent_count()
            resource_left = Resource.get_amount()

            # Ending the epoch, return values/end
            if self.epoch % 100 == 0:
                yield self.epoch, agents_alive # = data = (time, agents, resource, ....)
            
            if agents_alive <= 0:
                return "All agents are dead :( there is no hope left for the village, just darkness."
            if resource_dict <= 0:
                return "Y'all gonna starve HAHAHAHA."

            self.epoch += 1       