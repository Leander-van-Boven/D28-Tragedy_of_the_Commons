import numpy as np
import time
from .agent import Agent
from .resource import Resource

class Simulator:
    """Main class that manages the agents and resource.

    ...

    Attributes
    ----------
    epoch : `int`,
        The current epoch the simulation is on.

    agents : `list`,
        A list containing all (alive) agents currently in the simulation.
    
    result : `str`,
        Set when the simulation is done, denoting the outcome of the sim.
    
    resource : `Resource`,
        A resource object representing the common resource.

    Methods
    -------
    getters and setters for each attribute

    `get_agent_count(min_social_value=0, max_social_value=1)`

    `add_agent(agent)`

    `remove_agent(agent)`

    `generate_simulation()`
    """

    epoch = 0
    agents = []
    result = ""
    resource = None


    def __init__(self, param_dict, printer=None, logger=None, row_head=[],
                 verbose=True):
        '''Initializes the simulation with the provided parameter dict.'''

        self.printer = printer
        self.logger = logger
        self.log_row_head = row_head
        self.verbose = verbose

        self.params = param_dict['simulation']
        self.max_epoch = self.params['max_epoch']
        self.plot_interval = self.params['plot_interval']
        self.print_interval = self.params['print_interval']
        self.log_interval = self.params['log_interval']

        self.resource_params = param_dict['resource']
        self.svo_distributions = param_dict['svo_dist']
        self.n_agents = param_dict['agent']['count']
        self.agent_params = param_dict['agent']['params']

        self.svo_mutation_factor = \
            param_dict['agent']['svo_convergence_factor'] / 3


    def get_agent_count(self, min_social_value=0, max_social_value=1):
        """Returns the amount of all agents if no params are specified.
        
        This function returns the amount of agents that have a social
        value orientation between the two parameters (inclusive).

        Parameters
        ----------
        min_social_value : `float`,
            The lower limit of the SVO of the agent (inclusive).
        max_social_value : `float`,
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
        """Adds an agent to the list of agents.

        Parameters
        ----------
        agent : `Agent`
            The agent to add.
        """

        self.agents.append(agent)


    def remove_agent(self, agent):
        """Removes the agent from the simulation.

        #TODO determine what to do with the energy of the agent
            when the agent dies from for example age or punishment.

        Parameters
        ----------
            agent : `Agent`,
                The agent to remove.
        """

        self.agents.remove(agent)


    def get_resource(self):
        return self.resource
        
    
    def get_result(self):
        return self.result


    def get_epoch(self):
        return self.epoch


    def generate_simulation(self):
        """Generates the simulation.
        
        This function runs sets up the simulation as a Generator
        Every iteration, tt makes an agent act, causes resource to 
        replenish and collects data to plot and/or log.

        Yields
        ------
        data : `tuple`,
            Tuple containing the current epoch, 
                the current amount of agents per agent distribution
                and the current amount of the common resource.
        """

        # Generate agents
        self.agents = Agent.from_svo_distribution(
            self.svo_distributions, self.n_agents, self.agent_params)

        # # Initialise the agents
        # for dist_name in self.agent_distributions:
        #     dist = self.agent_distributions[dist_name]
        #     for _ in range(dist.get('agent_count',0)):
        #         self.add_agent(Agent(dist))

        # Initialise the resource
        self.resource = Resource(self.resource_params)

        # Initialise runtime variables
        self.epoch = 0
        self.cur_stats = ''

        # Plot starting situation
        if self.printer:
            yield self.plot_results()
        if self.verbose:
            self.print_results()

        #TODO We might want to add self.epoch = 1 here.
        # Run the simulations for max_epoch amounts
        while (self.epoch < self.max_epoch):
            print('\n---    EPOCH %s    ---\n' % self.epoch)
            print(f"Agent count: {len(self.agents)}, available resource: {self.resource.get_amount():.2f}")

            parents = []
            eol = []

            # Update the agents
            for num, agent in enumerate(self.agents):
                #print(f'\t\t{num}. {agent}.act()')
                print(f"{num:3.0f}\tid={agent.id}\tsvo={agent.social_value_orientation:3.2f}\tpre={agent.energy:3.2f}",
                    end='')
                agent.act(self)
                print(f'\tpost={agent.energy:.2f}', end='')
                # Check impact of actions
                if agent.energy <= 0:
                    print('\tSTARVED')
                    eol.append(agent)
                elif agent.age > agent.maximum_age:
                    print('\tEOL')
                    eol.append(agent)                              
                elif agent.energy >= agent.procreate_req:
                    print('\tPROCEATE')
                    parents.append(agent)
                else:
                    print('\tLIVE')

            for agent in eol:
                self.agents.remove(agent)

            print('\nPost act agent count: %s' % self.get_agent_count())
            print('Procreate: %s (tot %s)' % (
                ', '.join([str(a.id) for a in parents]),
                len(parents)
            ))
            Agent.procreate(self, parents)
            print('Post-proc agent count: %s\n' % len(self.agents))
            # Update the resource and epoch
            self.resource.grow_resource() 
            np.random.shuffle(self.agents)
            self.epoch += 1

            time.sleep(self.params['sleep'])

            # Print the current stats of the simulation
            if self.verbose and self.epoch%self.print_interval == 0:
                self.print_results()
            if self.printer and self.epoch%self.plot_interval == 0:
                yield self.plot_results()
            if self.logger and self.epoch%self.log_interval == 0:
                self.log_results()

            input("Press enter to continue...")

            # Check whether there are still agents alive
            if self.get_agent_count() <= 1:
                pass#break
        
        # While loop finished, maximum epoch reached
        if self.verbose:
            print()
        # Some agents stayed alive
        if self.get_agent_count() > 1:
            self.result = ("Maximum epoch reached, you managed to keep " +
                           str(self.get_agent_count()) +
                           " agents alive!")
        elif self.get_agent_count() == 1:
            self.result = ("Only one lonely agent managed to survive\n" +
                           "He will stay on this forgotten island forever.")
        else:
            self.result = ("All agents are dead :( " + 
                           "there is no hope left for the village, " + 
                           "just darkness.")

        if self.printer:
            self.printer.save_fig('.lastplot.pdf')
        if self.verbose:
            print(self.result)

    
    def plot_results(self):
        """Creates a tuple of the current stats of the simulation.
        This tuple then needs to be yielded to get plotted.
        """

        return (self.epoch,
                len(self.agents),
                [agent.social_value_orientation for agent in self.agents],
                self.resource.get_amount())


    def print_results(self):
        '''Prints the current stats of the simulation.'''

        self.cur_stats = f"epoch: {self.epoch}, " + \
                         f"agent count: {self.get_agent_count()}, " + \
                         f"resource: {self.get_resource().get_amount():.2f}"
        # for dist_name in self.agent_distributions:
        #     dist = self.agent_distributions[dist_name]
        #     self.cur_stats += (
        #         f"{dist_name}: " + 
        #         str(self.get_agent_count(dist['min_social_value'], 
        #                                  dist['max_social_value'])) + 
        #         ", ")
        #self.cur_stats += f"res: {self.resource.get_amount():.2f}"
        print(self.cur_stats, end = "\r", flush = True)

    def log_results(self):
        '''Adds a new row to the log.'''
        
        row = self.log_row_head + [self.epoch, self.resource.get_amount()]
        #for dist_name in self.agent_distributions:
        #    dist = self.agent_distributions[dist_name]
        #    row.append(self.get_agent_count(dist['min_social_value'],
        #                                    dist['max_social_value']))
        
        
        a = 0
        b = 0
        c = 0
        d = 0
        e = 0
        
        agents_now = []
        agent_svo_rounded = []

        for agent in self.agents:
            svo = agent.social_value_orientation
            agents_now.append(svo)
            #agent_svo_rounded.append(np.round(svo,2))
            if svo <= .2:
                a += 1
            if (svo > .2 and svo <= .4) :
                b += 1
            if (svo > .4 and svo <= .6) :
                c += 1
            if (svo > .6 and svo <= .8) :
                d += 1
            if (svo > .8 and svo <= 1):
                e += 1

        #agent_svo_rounded = np.round(agents_now, 2)

        median = np.median(agents_now)

        below = []
        above = []

        for agent in self.agents:
            svo = agent.social_value_orientation
            if svo < median:
                below.append(svo)
            if svo > median:
                above.append(svo)


        row.append(a)
        row.append(b)
        row.append(c)
        row.append(d)
        row.append(e)
        row.append(median)
        row.append(np.percentile(agents_now,40))
        row.append(np.percentile(agents_now,60))
        row.append(np.mean(agents_now))
        row.append(np.std(agents_now))

        self.logger.add_row(row)