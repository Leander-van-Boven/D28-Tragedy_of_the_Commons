#TODO add docstring

import math

class Resource:
    start_amount = 100
    energy_per_unit = 1
    growth_rate = 1.0
    max_amount = 100
    min_amount = 0
    amount = 100


    def __init__(self, values):
        self.start_amount = values["start_amount"]
        self.energy_per_unit =  values["energy_per_unit"]
        self.growth_rate = values["growth_rate"]
        self.max_amount = values["max_amount"]
        self.min_amount = values["min_amount"]
        self.amount = self.start_amount


    def growth_func(self, fx):
        '''
        Parameters:
            0: r = r * coeff, 

            1: r += r,

            2: r += sqrt(max - current) 

        '''
        if (self.amount <= self.min_amount): 
            self.amount = self.min_amount

        if fx == 0:
            self.amount = self.amount * self.growth_rate
        elif fx == 1:
            self.amount += self.amount
        elif fx == 2:
            self.amount += math.sqrt(self.max_amount - self.amount) 

        if (self.amount > self.max_amount):
            self.amount = self.max_amount


    def consume_resource(self, amount):
        if self.amount - amount < 0:
            self.amount = 0
            return self.amount * self.energy_per_unit
        else:
            self.amount -= amount
            return amount * self.energy_per_unit


    def get_amount(self):
        return self.amount


    def get_energy_per_unit(self):
        return self.energy_per_unit


    def set_energy_per_unit(self, energy_per_unit):
        self.energy_per_unit = energy_per_unit


    def get_growth_rate(self):
        return self.growth_rate


    def set_set_growth_rate(self, growth_rate):
        self.set_growth_rate = growth_rate


    def get_max_amount(self):
        return self.max_amount
    

    def set_max_amount(self, max_amount):
        self.max_amount = max_amount
     

    def get_min_amount(self):
        return self.min_amount


    def set_min_amount(self, min_amount):
        self.min_amount = min_amount
