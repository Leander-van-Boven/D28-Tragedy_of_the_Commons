import random as rnd
import numpy as np
import scipy.stats as ss

class Agent:
    # Attributes
    age = 0
    energy = 0
    child_count = 0

    # Parameters
    start_energy_multiplier = 3
    social_value_orientation = 0
    metabolism = 3
    consumption = 15
    procreate_req = 20
    procreate_cost = 15
    maximum_age = 100
    mutation_factor = .1

    # Base Model Parameters
    scarcity = 1
    greed1 = 1.5
    greed2 = 1.85
    greed3 = 5

    # Prime Model Parameters
    hunger = 9
    low_energy = 3
    hungry = 1.5
    dying = 2
    eldery = 70

    # Restricted Model Parameters
    res_limit_factor = 2
    caught_chance = .25
    caught_cooldown = 20
    cur_cooldown = 0


    def __init__(self, params, svo=None):
        """Initialises the agent with the provided parameters.

        If a parameter is not specified, its default value (set above)
        is used.

        Parameters
        ----------
        params : `dict`,
            Dictionary containing the parameters for this agent.
        """

        self.metabolism = params.get('metabolism', self.metabolism)
        self.consumption = params.get('consumption', self.consumption)
        self.maximum_age = params.get('maximum_age', self.maximum_age)
        self.mutation_factor = params.get('mutation_factor', 
                                          self.mutation_factor)

        self.procreate_req = params.get('procreate_req', self.procreate_req)
        self.procreate_cost = params.get('procreate_cost', self.procreate_cost)

        # #TODO: Check syntax 
        # self.social_value_orientation = params.get('svo', 
        #     rnd.uniform(params.get('min_social_value',0), 
        #         params.get('max_social_value',1)))

        if svo is not None:
            self.social_value_orientation = svo
        else:
            self.social_value_orientation = rnd.uniform(
                params.get('min_social_value',0), params.get('max_social_value',1))

        self.energy = self.metabolism * params.get('start_energy_multiplier',
                                                   self.start_energy_multiplier)

        # Restricted energy function parameters
        self.res_limit_factor = params.get('res_limit_factor',
                                           self.res_limit_factor)
        self.caught_chance = params.get('caught_chance', self.caught_chance)
        self.caught_cooldown = params.get('caught_cooldown',
                                          self.caught_cooldown)
        

    @classmethod
    def from_svo_distribution(cls, dist_params, n, agent_params=dict()):
        """Generate a list of agent with their SVOs drawn from a 
        multimodal distribution.

        Parameters
        ----------
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
        return [Agent(agent_params, svo) for svo in agent_svos]

   
    def act(self, sim):
        """This is the act function of the agent.
        It updates the status of the agent depending on multiple factors.

        Parameters
        ----------
        sim : `Simulation`,
            Reference to the simulation
        """

        # Life cycle
        #TODO Metabolism increases as agent gets older
        self.energy -= self.metabolism
        self.age += 1
        # Execute behaviour to compensate lost energy from metabolism
        #TODO Change this to execute the behaviour set as parameter
        #TODO Implement more behaviours
        #self.base_energy_function(sim)
        self.restricted_energy_function(sim)
        

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
            if fish/population < self.scarcity:
                self.energy += sim.get_resource().consume_resource(
                    self.consumption*self.greed3)
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

        # Check if agent is not allowed to fish this epoch.
        if self.cur_cooldown > 0:
            self.cur_cooldown -= 1
            return

        # Check whether the resources dropped below restriction limit.
        if (sim.get_resource().get_amount() < 
            sim.get_agent_count()*self.res_limit_factor):
            # If agent would die this epoch it is allowed to fish the
            # amount of fish to get at 1 energy at the end of the epoch.
            if self.energy <= 0:
                # self.energy += sim.get_resource().consume_resource(
                #     abs(self.energy) + 1)
                self.energy += sim.get_resource().consume_resource(
                    self.consumption)
            # Otherwise, determine based on SVO whether agent violates
            # the fishing rule.
            elif rnd.random() > self.social_value_orientation:
                # Check if agent is caught violating the rule.
                if rnd.random() < self.caught_chance:
                    self.cur_cooldown = self.caught_cooldown
                else:
                    self.energy += sim.get_resource().consume_resource(
                        self.consumption)    
        # 'Plenty' of fish
        else:
            self.energy += sim.get_resource().consume_resource(self.consumption)

    def new_energy_function(self, sim):
        # Functions:
        def prosocial(_):
            return self.consumption

        def proself(sim):
            fish = sim.get_resource().get_amount()
            population = sim.get_agent_count()
            if fish/population < self.scarcity:
                return self.consumption*self.greed3
            else:
                return self.consumption

        # Behaviour library:
        behaviours = [
            (0.9, prosocial),
            (0.1, proself),
        ]


    def procreate(self, sim, parents):
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
            # Select parent 1, update its params
            parent1 = parents.pop()
            parent1.energy -= parent1.procreate_req
            parent1.child_count += 1

            # Select parent 2, update its params
            parent2 = parents.pop()
            parent2.energy -= parent2.procreate_req
            parent2.child_count += 1

            # Select the winning parent. 
            # Its genes will be used for the child
            # --------------------------------------------
            # genes = rnd.random([parent1,parent2])
            # genes = parent1 if parent1.age >= parent2.age else parent 2
            genes = parent1 if parent1.energy >= parent2.energy else parent2

            # Create the child with winning genes
            # Added genetic transmission of stronger parent with 
            # randomized coefficient.
            mutation = 0
            child = {
                "min_social_value" : min(parent1.social_value_orientation, 
                                         parent2.social_value_orientation),
                "max_social_value" : max(parent1.social_value_orientation, 
                                         parent2.social_value_orientation),

                "metabolism" : genes.metabolism 
                    #+ genes.metabolism*rnd.gauss(0,self.mutation_factor),
                    ,
                "consumption" : genes.consumption 
                    #+ genes.consumption*rnd.gauss(0,self.mutation_factor),
                    ,
                "maximum_age" : genes.maximum_age 
                    #+ genes.maximum_age*rnd.gauss(0,self.mutation_factor),
                    ,

                "procreate_req" : genes.procreate_req
                    #+ genes.procreate_req*rnd.gauss(0,self.mutation_factor),
                    ,
                "procreate_cost" : genes.procreate_cost
                    #+ genes.procreate_cost*rnd.gauss(0,self.mutation_factor),
                    ,

                # "mutation_factor" : self.mutation_factor
                #     + self.mutation_factor*rnd.gauss(0,self.mutation_factor),
            }
            sim.add_agent(Agent(child))

    #TODO implement more energy functions / behaviours
    # def secondary_energy_function(self, res):
    """
    Built of base model.

    Accounts for deliberation time contraints based on age, hunger,
        and scarcity

    These time contraints inspire increasingly greedy behaviour in 
        proself agents

    Additional greed coefficients are weighted at a diminishing value
    """
    #
    #   self.energy -= self.metabolism
    #   
    #   # Prosocial
    #   if self.social_value_orientation >= .5:
    #       self.energy += res.consume_resource(self.consumption)
    #
    #   # Proself
    #   fish = res.get_amount()
    #   population = self.simulation.get_agent_count()
    #
    #   scarce_bool = fish/population < self.scarcity
    #   age_bool = self.age > self.elderly
    #   hungry_bool = self.energy < self.hungry
    #
    #   if scarce_bool and age_bool and hungry_bool:
    #       self.energy += res.consume_resource(
    #           self.consumption*self.greed1*greed2*greed3)
    #   elif (scarce_bool and age_bool) or 
    #        (scarce_bool and hungry_bool) or 
    #        (age_bool and hungry_bool):
    #       self.energy += res.consume_resource(
    #           self.consumption*self.greed1*greed2)
    #   elif scare_bool or age_bool or hungry_bool:
    #       self.energy += res.consume_resource(
    #           self.consumption*self.greed1)
    #   else:
    #       self.energy += res.consume_resource(self.consumption)
    #
    #   self.age += 1
    #   
    #   ### Addition of Reproduction to the model
    #   reproduce = 0
    #   if self.energy > self.procreate_req:
    #       reproduce += 1
    #   return reproduce

    #TODO
    # implement high-reward high-risk functions 
    #   that have possible punishments:
    #   "An agent is not allowed to go fishing 
    #       when the amount of fish is below x",
    #   Punishment: If caught, the agent is not allowed to fish 
    #       or y amount of days