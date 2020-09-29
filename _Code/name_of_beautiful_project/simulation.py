import numpy as np
import time
from .agent import Agent
from .resource import Resource

class Simulation:
    epoch = 0
    initial_agent_count = 100
    agents = []
    result = ""
    resource = None


    def __init__(self, param_dict, logger=None):
        self.params = param_dict['simulation']
        self.initial_agent_count = self.params['initial_agents_count']
        self.max_epoch = self.params['max_epoch']

        self.agent_params = param_dict['agent']
        self.resource_params = param_dict['resource']


    #--- Getters & Setters
    def get_initial_agent_count(self):
        return self.initial_agent_count


    def set_initial_agent_count(self, count):
        self.initial_agent_count = count


    # def get_agent_count(self):
    #    return len(self.agents)
  
    def get_agent_count(self, social_value = 1, greater = False):
        if greater:
            return len([agent for agent in self.agents if agent.social_value_orientation > social_value])
        else:
            return len([agent for agent in self.agents if agent.social_value_orientation <= social_value])


    def get_agents(self):
        pass
        # classes = {}
        # i = 0
        # for agent in self.agents:
        #   svo = agent.social_value_orientation()
        #   if classes.get(svo) is none:
        #       classes[svo] = 0
        # for agent in self.agents:   
        #   svo = agent.social_value_orientation()
        #   classes[svo] = classes.get(svo, 0) + 1
        # return classes   


    def set_agent(self, agent):
        self.agents.append(agent)


    def get_initial_agent_count(self):
        return self.initial_agent_count


    def set_initial_agent_count(self, count):
        self.initial_agent_count = count


    def remove_agent(self, agent):
        self.agents.remove(agent)

    
    def get_result(self):
        return self.result


    #--- Main methods
    def run_simulation(self):
        """
        The function that runs the simulation for the amount of epochs given.
        It makes an agent act, causes resource to replenish, and collects data to plot.
        """
        self.epoch = 0

        # Initialise the agents
        for i in range(self.initial_agent_count):    
            agent = Agent(self.agent_params, self)
            self.set_agent(agent)

        # Initialise the resource
        self.resource = Resource(self.resource_params)
        
        # Run the simulations for max_epoch amounts
        while (self.epoch < self.max_epoch):
            # Print the current stats of the simulation
            if self.epoch % 2 == 0:
                #print(self.epoch , self, self.resource)
                yield self.epoch, [self.get_agent_count(.5, False), self.get_agent_count(.5, True)], self.resource.get_amount() 
                # = data = (time, agents, resource, ....)
            if self.epoch % 1 == 0:
                print(f"epoch:{self.epoch}, res: {self.resource.get_amount():.2f}, self: {self.get_agent_count(.5, False)}, social: {self.get_agent_count(.5, True)}", end = "\r", flush = True)

            # Update the agents
            for agent in self.agents:
                agent.act(self.resource, self.epoch)
                if agent.energy <= 0:
                    self.remove_agent(agent) # Agent is dead, do we remove now/later/before?
            
            if self.get_agent_count() <= 0:
                self.result = "All agents are dead :( there is no hope left for the village, just darkness."
                print(self.result)
                return

            # Update the resource
            self.resource.growth_func(0) # 0: r = r * coeff, 1: r += r, # 2: r += sqrt(max - current) 

            self.epoch += 1
            #time.sleep(0.5) # Uncomment to slow down the simulation / plotting speed