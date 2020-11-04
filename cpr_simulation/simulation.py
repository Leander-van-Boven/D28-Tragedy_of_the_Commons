import time

import numpy as np

from .agent import Agent
from .resource import Resource
from .util import do_nothing


class Simulator:
    """Main class that manages the agents and resource.

    Refer to the documentation
    (https://leander-van-boven.github.io/D28-Tragedy_of_the_Commons/
        pages/architecture/#simulator)
    for a thorough explanation of this class.
    """

    v_print = do_nothing
    v1_print = do_nothing
    v2_print = do_nothing

    def __init__(self, param_dict, printer=None, logger=None, row_head=[],
                 verbose=True):
        """Initializes the simulation with the provided parameter dict."""

        self.epoch = 0
        self.agents = []
        self.result = ""
        self.resource = None

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

        self.resource_limit_factor = \
            self.params['res_limit_factor'] * \
            self.agent_params['consumption_factor'] * \
            self.agent_params['metabolism']

        self.resource_unlimit_factor = \
            self.params['res_unlimit_factor'] * \
            self.agent_params['consumption_factor'] * \
            self.agent_params['metabolism']

        self.restriction_mode = \
            self.agent_params['behaviour'] == "restricted_energy_function"
        self.restriction_active = \
            None if not self.restriction_mode else False

        if verbose > 0:
            self.v_print = print
            if verbose == 1:
                self.v1_print = print
            elif verbose == 2:
                self.v2_print = print

        Agent.print = self.v2_print
        Agent.svo_inheritance_function = \
            param_dict['agent']['svo_inheritance_function']
        Agent.svo_convergence_factor = \
            (param_dict['agent']['svo_convergence_factor']
                       [param_dict['agent']['svo_inheritance_function']]) / 3

        Resource.print = self.v2_print

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

        Parameters
        ----------
            agent : `Agent`,
                The agent to remove.
        """

        self.agents.remove(agent)

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
        if self.logger:
            self.log_results()
        self.epoch = 1

        # Run the simulations for max_epoch amounts
        while self.epoch < self.max_epoch:
            self.v2_print('\n---    EPOCH %s    ---\n' % self.epoch)
            self.v2_print(f"Agent count: {len(self.agents)}")
            self.v2_print("Available resource: " +
                          f"{self.resource.amount:.2f}")
            self.v2_print(f"Restriction: ", end='')

            parents = []
            eol = []

            if self.restriction_mode:
                if self.resource.amount > \
                        len(self.agents) * self.resource_unlimit_factor:
                    self.restriction_active = False
                if self.resource.amount < \
                        len(self.agents) * self.resource_limit_factor:
                    self.restriction_active = True

            if self.restriction_active:
                self.v2_print(f"ACTIVE")
            else:
                self.v2_print(f"INACTIVE")

            # Update the agents
            for num, agent in enumerate(self.agents):
                self.v2_print(f"{num:3.0f}\tid={agent.id}\t" +
                              f"svo={agent.social_value_orientation:3.2f}\t" +
                              f"pre={agent.energy:3.2f}", end='')
                agent.act(self)
                self.v2_print(f'\tpost={agent.energy:.2f}', end='')
                # Check impact of actions
                if agent.energy <= 0:
                    self.v2_print('\tSTARVED')
                    eol.append(agent)
                elif agent.age > agent.maximum_age:
                    self.v2_print('\tEND OF LIFE')
                    eol.append(agent)
                elif agent.energy >= agent.procreate_req:
                    self.v2_print('\tPROCREATE')
                    parents.append(agent)
                else:
                    self.v2_print('\tLIVE')

            self.v2_print("\nEOL: %s (tot %s)" % (
                ', '.join([str(a.id) for a in eol]),
                len(eol)))

            for agent in eol:
                self.agents.remove(agent)

            self.v2_print('Post act agent count: %s' %
                          len(self.agents))
            self.v2_print('\nProcreate: %s (tot %s)' % (
                ', '.join([str(a.id) for a in parents]),
                len(parents)))

            Agent.procreate(self, parents)
            self.v2_print('Post procreate agent count: %s\n'
                          % len(self.agents))
            # Update the resource and epoch
            self.resource.grow_resource()
            np.random.shuffle(self.agents)

            time.sleep(self.params['sleep'])

            # Print the current stats of the simulation
            if self.verbose and self.epoch % self.print_interval == 0:
                self.print_results()
            if self.printer and self.epoch % self.plot_interval == 0:
                yield self.plot_results()
            if self.logger and self.epoch % self.log_interval == 0:
                self.log_results()

            if self.verbose == 2:
                input("Press enter to continue...")

            # Check whether there are still agents alive
            if len(self.agents) <= 1:
                break

            self.epoch += 1

        # While loop finished, maximum epoch reached
        self.v_print()
        # Some agents stayed alive
        if len(self.agents) > 1:
            self.result = ("Maximum epoch reached, you managed to keep " +
                           str(len(self.agents)) +
                           " agents alive!")
        elif len(self.agents) == 1:
            self.result = ("Only one lonely agent managed to survive.\n" +
                           "He will stay on this forgotten island forever.")
        else:
            self.result = ("All agents are dead :(\n" +
                           "There is no hope left for the village, " +
                           "just darkness.")

        if self.printer:
            self.printer.save_fig('.lastplot.png')
        self.v_print(self.result)

    def plot_results(self):
        """Creates a tuple of the current stats of the simulation.
        This tuple then needs to be yielded to get plotted.
        """

        return (self.epoch,
                len(self.agents),
                [agent.social_value_orientation for agent in self.agents],
                self.resource.amount,
                len(self.agents) * self.resource_limit_factor,
                len(self.agents) * self.resource_unlimit_factor)

    def print_results(self):
        """Prints the current stats of the simulation."""
        self.cur_stats = ''
        if self.restriction_mode:
            self.cur_stats += f"restriction: "
            self.cur_stats += \
                "ACTIVE,   " if self.restriction_active else "INACTIVE, "
        self.cur_stats += f"epoch: {self.epoch}, " + \
                          f"agent count: {len(self.agents)}, " + \
                          f"resource: {self.resource.amount:.2f}"

        # for dist_name in self.agent_distributions:
        #     dist = self.agent_distributions[dist_name]
        #     self.cur_stats += (
        #         f"{dist_name}: " +
        #         str(self.get_agent_count(dist['min_social_value'],
        #                                  dist['max_social_value'])) +
        #         ", ")
        # self.cur_stats += f"res: {self.resource.amount:.2f}"
        self.v1_print(self.cur_stats, end="\r", flush=True)

    def log_results(self):
        """Adds a new row to the log."""

        row = self.log_row_head + [self.epoch, self.resource.amount]
        # for dist_name in self.agent_distributions:
        #    dist = self.agent_distributions[dist_name]
        #    row.append(self.get_agent_count(dist['min_social_value'],
        #                                    dist['max_social_value']))

        a = 0
        b = 0
        c = 0
        d = 0
        e = 0

        agents_now = []
        for agent in self.agents:
            svo = agent.social_value_orientation
            agents_now.append(svo)
            if svo <= .2:
                a += 1
            elif .2 < svo <= .4:
                b += 1
            elif .4 < svo <= .6:
                c += 1
            elif .6 < svo <= .8:
                d += 1
            elif .8 < svo <= 1:
                e += 1

        row.append(len(self.agents))
        row.append(a)
        row.append(b)
        row.append(c)
        row.append(d)
        row.append(e)

        if len(agents_now) > 0:
            row.append(np.median(agents_now))
            row.append(np.percentile(agents_now, 40))
            row.append(np.percentile(agents_now, 60))
            row.append(np.mean(agents_now))
            row.append(np.std(agents_now))
            row.append(len(self.agents) * self.resource_limit_factor)
            row.append(len(self.agents) * self.resource_unlimit_factor)
        else:
            row.append(0)
            row.append(0)
            row.append(0)
            row.append(0)
            row.append(0)
            row.append(0)
            row.append(0)

        self.logger.add_row(row)
