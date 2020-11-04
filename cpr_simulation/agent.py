import random as rnd

import numpy as np
import scipy.stats as ss

from .util import do_nothing


class Agent:
    """Class representing the main actors of the model

    Refer to the documentation
    > https://leander-van-boven.github.io/D28-Tragedy_of_the_Commons/
        pages/architecture/#agent
    for a thorough explanation of this class.
    """

    # Static attributes
    svo_convergence_factor = 0
    svo_inheritance_function = 'svo_either_parent'
    print = do_nothing

    def __init__(self, params, **kwargs):
        """Initialises the agent with the provided parameters.

        If a parameter is not specified, its default value (set above)
        is used.

        Parameters
        ----------
        params : `dict`,
            Dictionary containing the parameters for this agent.
        **kwargs : `dict`, optional,
            If desired, you can add 'id' key for a unique agent
            identifier and 'svo' key to override the svo value.
        """

        # Independent parameters
        self.age = 0
        self.energy = 0
        self.child_count = 0
        self.penalty_cooldown = 0

        # General parameters
        self.metabolism = params['metabolism']
        self.consumption = params['metabolism'] * params['consumption_factor']
        self.procreate_cost = \
            params['metabolism'] * params['procreate_cost_factor']
        self.procreate_req = \
            self.procreate_cost * params['procreate_req_factor']
        self.energy = params['metabolism'] * params['start_energy_factor']
        self.maximum_age = max(0, int(round(rnd.gauss(
            params['maximum_age'],
            params['maximum_age'] * params['maximum_age_std_factor']))))
        self.behaviour = params['behaviour']
        # Override SVO value
        self.social_value_orientation = kwargs.get('svo', .5)
        # Unique agent identifier
        self.id = kwargs.get('id', -1)

        # Base energy function parameters
        self.scarcity = params['scarcity']
        self.greed = params['greed']

        # Restricted energy function parameters
        self.caught_chance = params['caught_chance']
        self.caught_cooldown = \
            params['caught_cooldown_factor'] * params['maximum_age']

    @classmethod
    def from_svo_distribution(cls, dist_params, n, agent_params=dict()):
        """Generate a list of agent with their SVOs drawn from a
        multimodal distribution.

        Parameters
        ----------
        dist_params : `dict[str, dict[str, float]]`,
            A dictionary of normal distribution dicionaries. Each normal
            distribution should have a key 'm' denoting the mean, and a
            key 's' denoting the standard deviation.
        n : `float` or `int`
            The desired number of agents. Will be rounded down.
        agent_params : `dict`, optional
            The parameter dictionary that will be passed on to each
            agent, by default dict().

        Returns
        -------
        list[csp_simulation.Agent]
            The list of Agents.
        """

        # If dist_param is an empty dictionary, use default
        if not dist_params:
            dist_params = {
                "d1": {
                    "m": 0.25,
                    "s": .125
                },
                "d2": {
                    "m": 0.75,
                    "s": .125
                }
            }

        # Convert the dictionary structure to a list structure sorted
        # by index instead of key
        dist_params = \
            np.array([list(d.values()) for d in dist_params.values()])

        # The shape of dist_params should be (x,2) with x>0
        assert dist_params.shape[0] > 0
        assert dist_params.shape[1] == 2

        # It is possible that type(n)=float. We thus need to cast to int
        n = int(n)
        n_dist = dist_params.shape[0]

        # For now, each distribution is weighed equally to get an
        # unbiased gaussian mixture.
        weights = np.ones(n_dist, dtype=np.float64) / float(n_dist)

        # Sample for each agent, the index of the distribution its SVO
        # will be drawn from.
        agent_dist_index = np.random.choice(len(weights), size=n, replace=True,
                                            p=weights)

        # For each agent, draw its SVO from the right normal distribution
        agent_svos = np.fromiter(
            (ss.norm.rvs(*(dist_params[i])) for i in agent_dist_index),
            dtype=np.float64)

        # Clip the SVOs to values between 0 and 1
        np.clip(agent_svos, 0, 1, out=agent_svos)

        # Return the list of Agent with the right SVOs
        return [Agent(agent_params, svo=svo, id=id) for (id, svo) in
                enumerate(agent_svos)]

    def act(self, sim):
        """This is the act function of the agent. This function updates
        the status of the agent depending on its behaviour function.

        Parameters
        ----------
        sim : `Simulation`,
            The current simulation
        """

        # Metabolise some energy
        self.energy -= self.metabolism
        # Grow older
        self.age += 1
        self.print(f'\t-met={self.energy:.2f}', end='')
        # Execute behaviour to compensate lost energy from metabolism
        eval('self.' + self.behaviour)(sim)
        self.print(f'\t+beh={self.energy:.2f}', end='')

    def base_energy_function(self, sim):
        """This is the base model energy function for our agent.

        Implements the basic behaviour of the agents.

        - Pro-social agents will always fish
            at the predefined consumption rate.
        - Pro-self agents, will fish with an extra greed coefficient
            when fish population is low relative to human population.

        Parameters
        ----------
        sim : `Simulation`,
            The current simulation
        """

        # Prosocial Behaviour
        if self.social_value_orientation >= .5:
            self.energy += sim.resource.consume_resource(self.consumption)
        # Proself Behaviour
        else:
            fish = sim.resource.amount
            population = sim.get_agent_count()
            if fish / population < self.scarcity:
                self.energy += sim.resource.consume_resource(
                    self.consumption * self.greed)
            else:
                self.energy += sim.resource.consume_resource(
                    self.consumption)

    def restricted_energy_function(self, sim):
        """Agent behaviour based on restrictions on the common resource.

        This behaviour allows agents to fish their consumption when
        the resource amount is above the set restriction limit.
        This limit is determined in terms of currently alive agents and
        a certain factor.

        The following happens when resources drop below set limit:
        - Prosocial agents will only consume enough fish to be left
            with 1 energy; enough to just survive another day.
            Thus if they already have >=1 energy they will not fish.
        - Proself agents with >=1 energy have a chance to violate the
            fishing restriction and fish anyways. If they do, there is a
            chance they get caught and are not allowed to fish for a
            certain amount of days.

        Parameters
        ----------
        sim : `Simulation`,
            The current simulation
        """

        # Check if agent is not allowed to fish this epoch.
        if self.penalty_cooldown > 0:
            self.penalty_cooldown -= 1
            self.print('\tCOOLDOWN', end='')
            return

        assert sim.restriction_active is not None

        if sim.restriction_active:
            # If the agent is restricted
            self.print('\tRESTRICTED', end='')
            # If agent would die this epoch it is allowed to fish the
            # amount of fish to get at 1 energy at the end of the epoch.
            if self.energy <= 0:
                self.energy += sim.resource.consume_resource(
                    self.consumption + 1)
            # Otherwise, determine based on SVO whether agent violates
            # the fishing rule.
            elif rnd.random() > self.social_value_orientation:
                # Check if agent is caught violating the rule.
                if rnd.random() < self.caught_chance:
                    self.penalty_cooldown = self.caught_cooldown
                else:
                    self.energy += sim.resource.consume_resource(
                        self.consumption)
        else:
            # If the agent is not restricted, just consume the desired
            # amount of resource.
            self.print('\tUNRESTRICTED', end='')
            self.energy += sim.resource.consume_resource(self.consumption)

    @classmethod
    def procreate(cls, sim, parents):
        """This is the procreate function of the agent.
        It allows the agents to procreate.

        Parameters
        ----------
        sim : `Simulation`,
            Reference to the simulation
        parents : `list[Agent]`,
            An array of agents with energy > procreate_req
        """

        def svo_either_parent():
            if rnd.random() < parent1.energy / (parent1.energy+parent2.energy):
                svo = rnd.gauss(parent1.social_value_orientation,
                                Agent.svo_convergence_factor)
            else:
                svo = rnd.gauss(parent2.social_value_orientation,
                                Agent.svo_convergence_factor)
            return max(min(svo, 1), 0)

        def svo_between_parents():
            svo_mean = \
                (parent1.social_value_orientation*parent1.energy
                 + parent2.social_value_orientation*parent2.energy) \
                / (parent1.energy+parent2.energy)
            base_svo_std = min(abs(svo_mean-parent1.social_value_orientation),
                               abs(svo_mean-parent2.social_value_orientation))
            svo_std = base_svo_std * Agent.svo_convergence_factor
            return max(min(rnd.gauss(svo_mean, svo_std), 1), 0)

        if parents:
            # Detrmine the start point for unique agent identifier
            s_id = max([a.id for a in parents]) + 1

        rnd.shuffle(parents)
        while len(parents) > 1:
            # Select parent 1, update its attributes
            parent1 = parents.pop()
            parent1.child_count += 1

            # Select parent 2, update its attributes
            parent2 = parents.pop()
            parent2.child_count += 1

            svo = eval(Agent.svo_inheritance_function)()

            child = Agent(sim.agent_params, id=s_id, svo=svo)
            child.energy = (parent1.procreate_cost +
                            parent2.procreate_cost) / 2

            sim.add_agent(child)

            parent1.energy -= parent1.procreate_cost
            parent2.energy -= parent2.procreate_cost

            s_id += 1
