import random as rnd

class Agent:
    # Base Model Parameters
    scarcity = .5
    greed1 = 1.5
    greed2 = 1.85
    greed3 = 5
    start_energy_multiplier = 3
    metabolism = 2
    consumption = 1

    # Prime Model Parameters
    hunger = 9
    age = 0
    procreate_req = 16
    procreate_cost = 10
    maximum_age = 100

    low_energy = 3
    hungry = 1.5
    dying = 2
    eldery = 70

    # Attributes
    age = 0
    energy = 0
    child_count = 0
    social_value_orientation = 0
    behaviour = None


    def __init__(self, params):
        self.metabolism = params.get('metabolism', self.metabolism)
        self.consumption = params.get('consumption', self.consumption)
        self.procreate_req = params.get('procreate_req', self.procreate_req)
        self.procreate_cost = params.get('procreate_cost', self.procreate_cost)
        self.maximum_age = params.get('maximum_age', self.maximum_age)

        self.social_value_orientation = rnd.uniform(
            params["min_social_value"], params["max_social_value"])

        self.energy = self.metabolism * params.get('start_energy_multiplier',
                                                   self.start_energy_multiplier)
        
   
    def act(self, sim, res):
        """
        This is the act function of the agent.
        It is does everything relevant to an agent.
        """

        self.base_energy_function(sim, res)
        # These are just future methods that an agent could do
        #self.procreate(sim.get_epoch())
        #self.change_VO()


    def base_energy_function(self, sim, res):
        """This is the base model energy function for our agent.
        
        Implements the basic behaviour of the agents
        
        - Pro-social agents will always fish 
            at the predefined consumption rate.
        - Pro-self agents, will fish with an extra greed coefficient 
            when fish population is low relative to human population.
        
        """
        
        self.energy -= self.metabolism

        # Prosocial Behaviour
        if self.social_value_orientation >= .5:
            self.energy += res.consume_resource(self.consumption)

        # Proself Behaviour
        else:
            fish = res.get_amount()
            population = sim.get_agent_count()
            if fish/population < self.scarcity:
                self.energy += res.consume_resource(
                    self.consumption*self.greed3)
            else:
                self.energy += res.consume_resource(self.consumption)


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
    #       self.energy += res.consume_resource(self.consumption*self.greed1*greed2*greed3)
    #   elif (scarce_bool and age_bool) or (scarce_bool and hungry_bool) or (age_bool and hungry_bool):
    #       self.energy += res.consume_resource(self.consumption*self.greed1*greed2)
    #   elif scare_bool or age_bool or hungry_bool:
    #       self.energy += res.consume_resource(self.consumption*self.greed1)
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