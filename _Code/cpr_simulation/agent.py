import random as rnd

class Agent:
    # Attributes
    age = 0
    energy = 0
    child_count = 0

    # Parameters
    behaviour = None
    social_value_orientation = 0
    metabolism = 2
    consumption = 1
    procreate_req = 16
    procreate_cost = 10
    maximum_age = 100

    # Base Model Parameters
    scarcity = 1
    greed1 = 1.5
    greed2 = 1.85
    greed3 = 5
    start_energy_multiplier = 3

    # Prime Model Parameters
    hunger = 9
    low_energy = 3
    hungry = 1.5
    dying = 2
    eldery = 70

    # Restricted Model Parameters
    res_limit_factor = 1
    violation_chance = .25
    caught_chance = .10
    cooldown = 5
    cur_cooldown = 0


    def __init__(self, params):
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
        self.procreate_req = params.get('procreate_req', self.procreate_req)
        self.procreate_cost = params.get('procreate_cost', self.procreate_cost)
        self.maximum_age = params.get('maximum_age', self.maximum_age)

        self.social_value_orientation = rnd.uniform(
            params["min_social_value"], params["max_social_value"])

        self.energy = self.metabolism * params.get('start_energy_multiplier',
                                                   self.start_energy_multiplier)
        
   
    def act(self, sim):
        """This is the act function of the agent.
        It updates the status of the agent depending on multiple factors.

        Parameters
        ----------
        sim : `Simulation`,
            Reference to the simulation
        """

        # Life cycle
        self.energy -= self.metabolism

        # Execute behaviour to compensate lost energy from metabolism
        #TODO Change this to execute the behaviour set as parameter.
        #self.base_energy_function(sim)
        self.restricted_energy_function(sim)

        #TODO Implement more behaviours
        #self.procreate(sim.get_epoch())
        #self.change_VO()


    def base_energy_function(self, sim):
        """This is the base model energy function for our agent.
        
        Implements the basic behaviour of the agents
        
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
                #print('')
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
            # Prosocial Behaviour
            if self.social_value_orientation >= .5:
                # Agent only fishes enough to survive another day.
                if self.energy <= 0:
                    self.energy += sim.get_resource().consume_resource(
                        abs(self.energy) + 1)
            # Proself Behaviour
            else:
                # Determine if proself agent violates restriction rule.
                if self.energy>0 and rnd.random()<self.violation_chance:
                    self.energy = sim.get_resource().consume_resource(
                        self.consumption)
                    # Check whether agent is caught fishing.
                    #TODO Determine whether to take away fished resources 
                        # this epoch as extra punishment.
                    if rnd.random() < self.caught_chance:
                        self.cur_cooldown = self.cooldown
                # Comply to restriction rule; 
                # only fish to survive another day.
                else:
                    self.energy += sim.get_resource().consume_resource(
                        abs(self.energy) + 1)
        
        # 'Plenty' of fish
        else:
            self.energy += sim.get_resource().consume_resource(self.consumption)

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

            # Select the winning parent. Its genes will be used for the child
            # genes = rnd.random([parent1,parent2])
            # genes = parent1 if parent1.age >= parent2.age else parent 2
            genes = parent1 if parent1.energy >= parent2.energy else parent2

            # Create the child with winning genes
            child = {
                "label": "blerg",
                "line_style": ':',
                "agent_count": 1,
                "min_social_value": genes.social_value_orientation,
                "max_social_value": genes.social_value_orientation,

                "standard_param_deviation": .1,
                "start_energy_multiplier": 3,
                "metabolism": genes.metabolism,
                "consumption": genes.consumption,
                "maximum_age": genes.maximum_age,

                "procreate_req": genes.procreate_req,
                "procreate_cost": genes.procreate_cost,
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