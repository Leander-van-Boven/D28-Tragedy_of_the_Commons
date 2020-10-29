import random as rnd

import numpy as np
import scipy.stats as ss


class Agent:
    # Attributes
    age = 0
    energy = 0
    child_count = 0

    # Restricted Energy Function attributes
    restriction_active = False
    cur_cooldown = 0


    # variable = Agent(params);
    def __init__(self, params, **kwargs):
        """Initialises the agent with the provided parameters.

        If a parameter is not specified, its default value (set above)
        is used.

        Parameters
        ----------
        params : `dict`,
            Dictionary containing the parameters for this agent.
        """
        
        self.metabolism = params['metabolism']
        self.consumption = params['metabolism'] * params['consumption_factor']
        self.procreate_cost = params['metabolism'] \
                              * params['procreate_cost_factor']
        self.procreate_req_factor = params['procreate_req_factor']
        self.energy = params['metabolism'] * params['start_energy_factor']
        self.maximum_age = params['maximum_age']

        #self.behaviour = eval(params['behaviour'] + '(sim)')
        self.behaviour = params['behaviour']

        if 'svo' in kwargs:
            self.social_value_orientation = kwargs['svo']
        else:
            self.social_value_orientation = .5

        # Base energy function parameters
        self.scarcity = params['scarcity']
        self.greed = params['greed']

        # Restricted energy function parameters
        self.res_limit_factor = params['res_limit_factor']
        self.res_unlimit_factor = params['res_unlimit_factor']
        self.caught_chance = params['caught_chance']
        self.caught_cooldown = params['caught_cooldown_factor'] \
                                * params['maximum_age']
        

    @property
    def procreate_req(self):
        return self.procreate_cost * self.procreate_req_factor

    @classmethod
    def from_svo_distribution(cls, dist_params, n, agent_params=dict()):
        """Generate a list of agent with their SVOs drawn from a 
        multimodal distribution.

        Parameters
        ----------
        #TODO update docstring dist_params -> dict...
        dist_params : `list[list[float]]`
            The collection of normal distribution parameters. Sould be
            formatted as follows: dist_params[i][0] denotes the mean and
            dist_params[i][1] the variance of the i'th distribution, for 
            any i >= 0.
        n : `int/float`
            The desired number of agents.
        agent_params : `dict`, optional
            The parameter dictionary that will be passed on to each
            agent, by default dict().

        Returns
        -------
        list[csp_simulation.Agent]
            The list of Agents.
        """

        if not dist_params:
            dist_params = {
                "d1" : {
                    "m" : 0.25,
                    "s" : .125
                },
                "d2" : {
                    "m" : 0.75,
                    "s" : .125
                }
            }
               
        dist_params = [list(d.values()) for d in dist_params.values()]
        # We'll use numpy-specific functions, so we convert to np.array
        dist_params = np.array(dist_params)
        
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
        return [Agent(agent_params, svo=svo) for svo in agent_svos]
   
    def act(self, sim):
        """This is the act function of the agent.
        It updates the status of the agent depending on multiple factors.

        Parameters
        ----------
        sim : `Simulation`,
            Reference to the simulation
        """

        # Life cycle
        # TODO Metabolism increases as agent gets older
        # * (1 + exp(self.age - self.max_age/2))
        self.energy -= self.metabolism  
        self.age += 1
        # Execute behaviour to compensate lost energy from metabolism
        eval('self.' + self.behaviour)(sim)


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
            Reference to the simulation
        """

        # Prosocial Behaviour
        if self.social_value_orientation >= .5:
            self.energy += sim.get_resource().consume_resource(self.consumption)
        # Proself Behaviour
        else:
            fish = sim.get_resource().get_amount()
            population = sim.get_agent_count()
            if fish / population < self.scarcity:
                self.energy += sim.get_resource().consume_resource(
                    self.consumption * self.greed)
            else:
                self.energy += sim.get_resource().consume_resource(
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
            Reference to the simulation
        """

        def act_restricted():
            # If agent would die this epoch it is allowed to fish the
            # amount of fish to get at 1 energy at the end of the epoch.
            if self.energy <= 0:
                #print('\t\tself.energy<=0:', self.energy)
                # self.energy += sim.get_resource().consume_resource(
                #     abs(self.energy) + 1)
                self.energy += sim.get_resource().consume_resource(
                    self.consumption + 1)
                #print('\t\tfished, energy:', self.energy)
            # Otherwise, determine based on SVO whether agent violates
            # the fishing rule.
            elif rnd.random() > self.social_value_orientation:
                #print('\t\tviolated restriction...')
                # Check if agent is caught violating the rule.
                if rnd.random() < self.caught_chance:
                    #print('\t\tgot caught! setting cooldown to', self.caught_cooldown, ', energy:', self.energy)
                    self.cur_cooldown = self.caught_cooldown
                else:
                    self.energy += sim.get_resource().consume_resource(
                        self.consumption)
                    #print('\t\tfished violatetly, energy:', self.energy)
            # else:
            #     print('\t\tdid not fish today, energy:', self.energy)

        # Check if agent is not allowed to fish this epoch.
        if self.cur_cooldown > 0:
            #print('\tcur_cooldown > 0:', self.cur_cooldown, ', energy:', self.energy)
            self.cur_cooldown -= 1
            return

        # Check whether the resources dropped below restriction limit.
        if sim.get_resource().get_amount() > \
            sim.get_agent_count()*self.res_unlimit_factor*self.consumption:
            #print('\trestriction has become inactive')
            self.restriction_active = False
        elif sim.get_resource().get_amount() < \
            sim.get_agent_count()*self.res_limit_factor*self.consumption:
            #print('\trestriction has become active')
            self.restriction_active = True

        if self.restriction_active:
            #print('\tacting restricted')
            act_restricted()
        else:
            #print('\tacting unrestricted')
            self.energy += sim.get_resource().consume_resource(self.consumption)

    @classmethod
    def procreate(cls, sim, parents):
        """This is the procreate function of the agent.
        It allows the agents to procreate.

        Parameters
        ----------
        sim : `Simulation`,
            Reference to the simulation
        parents : [],
            An array of agents with energy > procreate_req
        """

        rnd.shuffle(parents)
        while len(parents) > 1:
            # Select parent 1, update its attributes
            parent1 = parents.pop()       
            parent1.child_count += 1

            # Select parent 2, update its attributes
            parent2 = parents.pop()           
            parent2.child_count += 1

            child = Agent(sim.agent_params)
            child.energy = parent1.procreate_cost #+ parent2.procreate_cost
            svo_mean = \
                (parent1.social_value_orientation*parent1.energy \
                + parent2.social_value_orientation*parent2.energy) \
                / (parent1.energy+parent2.energy)
            base_svo_std = min(abs(svo_mean-parent1.social_value_orientation), 
                               abs(svo_mean-parent2.social_value_orientation))
            svo_std = base_svo_std * sim.svo_mutation_factor
            child.social_value_orientation = \
                max(min(rnd.gauss(svo_mean, svo_std), 1), 0)
            
            sim.add_agent(child)

            parent1.energy -= parent1.procreate_cost
            parent2.energy -= parent2.procreate_cost
