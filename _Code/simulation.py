

class Simulation:
    initial_agent_count = 100
    
    epoch = 0

    agents = []
    resource = None

    def __init__(self, param_dict):
        self.initial_agent_count = param_dict['initial_agents_count']
        super().__init__()

    #--- Getters & Setters
    def get_initial_agent_count(self):
        return self.initial_agent_count

    def set_initial_agent_count(self, count):
        self.initial_agent_count = count

    def get_agent_count(self):
        return len(self.agents)

    def set_agent(self, agents):
        self.agents = agents

    def get_initial_agent_count(self):
        return self.initial_agent_count

    def set_initial_agent_count(self, count):
        self.initial_agent_count = count


    #--- Main methods
    def run_simulation(self, max_epoch = 1000000):
        self.agent_count = self.initial_agent_count
        self.epoch = 0

        while (self.epoch < max_epoch):
            for agent in self.agents:
                agent.do_cycle(self.resource)
            self.epoch += 1
            