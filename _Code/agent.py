

class Agent:

    # Default parameters
    metabolism = 2
    procreate_req = 16
    procreate_cost = 10
    maximum_age = 100

    init_consumption = 3
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





    def energy_function(self, epoch=1):
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