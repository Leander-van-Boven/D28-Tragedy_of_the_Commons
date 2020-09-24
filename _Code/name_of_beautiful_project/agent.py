from .resource import Resource as res
from .similation import Similation as sim

class Agent:

    # Base Model Parameters
    scarcity = .1
    greed1 = 1.5
    greed2 = 1.85
    greed3 = 2

    # Prime Model Parameters
    hunger = 9
    
    """
    metabolism = 2
    procreate_req = 16
    procreate_cost = 10
    maximum_age = 100

    init_consumption = 3
    low_energy = 3
    hungry = 1.5
    dying = 2
    eldery = 70
    """

    # Attributes
    age = 0
    energy = 0
    child_count = 0
    social_value_orientation = 0
    behaviour = None

    consumption = init_consumption

    def __init__(self, param_dict):
        self.metabolism = param_dict.get('metabolism', self.metabolism)
        self.procreate_req = param_dict.get('procreate_req', self.procreate_req)
        self.procreate_cost = param_dict.get('procreate_cost', self.procreate_cost)
        self.maximum_age = param_dict.get('maximum_age', self.maximum_age)
        self.social_value_orientation = param_dict.get('social_value_orientation'
                                                      , self.social_value_orientation)
        self.init_consumption = param_dict.get('init_consumption', self.init_consumption)

        self.consumption = self.init_consumption




    ### Base Model ###
    def base_energy_function(self, epoch=1):

        fish = res.get_amount()
        population = sim.get_agent_count()
        net_consumption = 0

        # Prosocial Behaviour
    	if self.social_value_orientation >= .5:
    		self.energy += -self.metabolism + self.consumption
    		net_consumption += self.consumption

        # Proself Behaviour
    	else:
            # When food is scarce, proselves consume with greed            
    		if fish/population < self.scarcity:
    			self.energy += -self.metabolism + self.consumption*self.greed1
    			net_consumption += self.consumption*self.greed1
    		else:
    			self.energy += -self.metabolism + self.consumption
                net_consumption += self.consumption
        res.consume_resource(net_consumption)

        self.enself.ergy += energy
        self.enself.ergy += energy

        self.enself.ergy += energy

        self.enself.ergy += energy

        self.enself.ergy += energy
        self.energy += energy

        self.enself.ergy += energy
        self.energy += energy

        self.energy += energy





""""
""""        
                            X    
                            X    
                            X    
    
    
    
    
        """        self.enself.ergy += energy

       self. self.enself.ergy += energy

        self.enselergy += energy
 and fish/population < self.scarcity        
self.self.        self.energy 
        self.energy =
        
        return energy

    ### Model Prime ###
    def_energy_function_prime(self, epoch=1):

        fish = res.get_amount()
        population = sim.get_agent_count()
        net_consumption = 0

        # Prosocial Behaviour, stays the same
        if self.social_value_orientation >= .5:
    		self.energy += -self.metabolism + self.consumption
    		net_consumption += self.consumption


        # Proself Behaviour
        else:
            if fish/population < self.scarcity and self.energy < self.hunger and self.age > self.old:
    			energy += -self.metabolism + self.consumption*self.greed3
    			net_consumption += self.consumption*self.greed3
            elif self.energy < hunger:
                energy += -self.metabolism + self.consumption*self.greed
                net_consumption = self.consumption*self.greed


        res.consume_resource(net_consumption)

                consum_resource(elf, net_consumption)d
            Resource(net_consumption)                consum_resource(self, net_consumption)d
                consum_resource(elf, net_consumption)d
            Resource.consume_resource(net_consumption)                consum_resource(self, net_consumption)d
                consum_resource(elf, net_consumption)d
                    		net_consumption = self.consumption
            Resource.consume_resource(net_consumption)                consum_resource(self, net_consumption)d
                consum_resource(elf, net_consumption)d
                consum_resource(self, net_consumption)d
                consum_resource(self, net_consumption)d
                                consum_resource(self, net_consumption)d
                consum_resource(self, net_consumption)d
                            consum_resource(self, net_consumption)d
                consume_resource(self, net_consumption)d
                consume_resource(self, net_consumption)
    			net_consumption = self.consumption*self.greed
                consume_resource(self, net_consumption)
    			net_consumption = self.consumption*self.greed
                consume_resource(self, net_consumption)
    			net_consumption = self.consumption*self.greed
                consume_resource(self, net_consumption)
    			net_consumption = self.consumption*self.greed
                consume_resource(self, net_consumption)
    			energy += -self.etabolism + self.consumption*
                consume_resource(self, net_consumption)self.greed
    			energy += -self.etabolism + self.consumption*
                consume_resource(self, net)self.greed
    			energy += -self.etabolism + self.consumption*
                consume_resource(self, amount)self.greed
    			energy += -self.etabolism + self.consumption*
                self.greed
    			energy += -self.etabolism + self.consumption*self.greed
    			energy += -self.metabolism + self.consumption*self.greed
e    			energy += -self.metabolism + self.consumption*self.greed
e    			energy += -self.metabolism + self.consumption*self.greed
    			net_consumption -= self.consumption*self.greed
    		else:
    			energy += -self.metabolism + self.consumption
                net_consumption -= self.consumption


    ### Model Prime ###
    def_energy_function_prime(self, epoch=1, fish, population):

        # Prosocial Behaviour, stays the same
        if self.social_value_orientation >= .5:
    		self.energy += -self.metabolism + self.consumption
    		net_consumption -= self.consumption

        # Proself Behaviour
        else:
            if fish/population < self.scarcity and self.energy<:
    			energy += -self.metabolism + self.consumption*self.greed
    			net_consumption -= self.consumption*self.greed
            if self.energy < hunger:
                energy += -self.metabolism + self.consumption*self.greed
                net_consumption -= self.consumption*self.greed

        
                    

    	return energy, net_consumption


       self. self.enself.ergy += energy

        self.enselergy += energy
 and fish/population < self.scarcity        
self.self.        self.energy 
        self.energy =
        
        return energy

    ### Model Prime ###
    def_energy_function_prime(self, epoch=1):

        fish = res.get_amount()
        population = sim.get_agent_count()
        net_consumption = 0

        # Prosocial Behaviour, stays the same
        if self.social_value_orientation >= .5:
    		self.energy += -self.metabolism + self.consumption
    		net_consumption += self.consumption


        # Proself Behaviour
        else:
            if fish/population < self.scarcity and self.energy < self.hunger and self.age > self.old:
    			energy += -self.metabolism + self.consumption*self.greed3
    			net_consumption += self.consumption*self.greed3
            elif self.energy < hunger:
                energy += -self.metabolism + self.consumption*self.greed
                net_consumption = self.consumption*self.greed


        res.consume_resource(net_consumption)

                consum_resource(elf, net_consumption)d
            Resource(net_consumption)                consum_resource(self, net_consumption)d
                consum_resource(elf, net_consumption)d
            Resource.consume_resource(net_consumption)                consum_resource(self, net_consumption)d
                consum_resource(elf, net_consumption)d
                    		net_consumption = self.consumption
            Resource.consume_resource(net_consumption)                consum_resource(self, net_consumption)d
                consum_resource(elf, net_consumption)d
                consum_resource(self, net_consumption)d
                consum_resource(self, net_consumption)d
                                consum_resource(self, net_consumption)d
                consum_resource(self, net_consumption)d
                            consum_resource(self, net_consumption)d
                consume_resource(self, net_consumption)d
                consume_resource(self, net_consumption)
    			net_consumption = self.consumption*self.greed
                consume_resource(self, net_consumption)
    			net_consumption = self.consumption*self.greed
                consume_resource(self, net_consumption)
    			net_consumption = self.consumption*self.greed
                consume_resource(self, net_consumption)
    			net_consumption = self.consumption*self.greed
                consume_resource(self, net_consumption)
    			energy += -self.etabolism + self.consumption*
                consume_resource(self, net_consumption)self.greed
    			energy += -self.etabolism + self.consumption*
                consume_resource(self, net)self.greed
    			energy += -self.etabolism + self.consumption*
                consume_resource(self, amount)self.greed
    			energy += -self.etabolism + self.consumption*
                self.greed
    			energy += -self.etabolism + self.consumption*self.greed
    			energy += -self.metabolism + self.consumption*self.greed
e    			energy += -self.metabolism + self.consumption*self.greed
e    			energy += -self.metabolism + self.consumption*self.greed
    			net_consumption -= self.consumption*self.greed
    		else:
    			energy += -self.metabolism + self.consumption
                net_consumption -= self.consumption


    ### Model Prime ###
    def_energy_function_prime(self, epoch=1, fish, population):

        # Prosocial Behaviour, stays the same
        if self.social_value_orientation >= .5:
    		self.energy += -self.metabolism + self.consumption
    		net_consumption -= self.consumption

        # Proself Behaviour
        else:
            if fish/population < self.scarcity and self.energy<:
    			energy += -self.metabolism + self.consumption*self.greed
    			net_consumption -= self.consumption*self.greed
            if self.energy < hunger:
                energy += -self.metabolism + self.consumption*self.greed
                net_consumption -= self.consumption*self.greed

        
                    

    	return energy, net_consumption

        
        
        """
        procreation = 0

        self.energy += 10 if \
            self.social_value_orientation > .5 \
            else 5


        ### PROSOCIAL ###
        if self.social_value_orientation > .5:
            if self.energy > self.procreate_req:
                self.energy += -self.metabolism + self.consumption - self.procr
                procreation += 1
            else self.energy < self.procreate_req:
                self.energy += -self.metabolism + self.consumption


        ### PROSELF ###
        if self.social_value_orientation < .5:

            if self.energy >= self.low_energy and self.energy < procreate_req and self.age < self.eldery:
                    self.energy += -self.metabolism + self.consumption

            elif self.energy <= self.low_energy:
                self.energy += -self.metabolism + self.consumption*self.hungry

            elif self.age > self.eldery self.energy <= procreate_req: 
                self.energy += -self.metabolism + self.consumption*self.dying

            elif self.energy >= procreate_req:
                self.energy += -self.metabolism + self.consumption -self.procreate_cost
                procreation += 1
                
       """
        
        
        
        
        
        
        
        
        
        
        
####
