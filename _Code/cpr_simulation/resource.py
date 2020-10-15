import math

class Resource:
    """This class represents the common resource, or fish in our case.

    All attributes are explained in `parameters.py`
    ...

    Methods
    -------
    getters and setters for each attribute

    `grow_resource()`

    `consume_resource(amount : double)`
    """

    start_amount = 100
    max_amount = 100
    min_amount = 0
    growth_rate = 1.0
    cooldown = 10
    cur_cooldown = 0
    in_cooldown = False


    def __init__(self, values):
        self.start_amount = values.get('start_amount', self.start_amount)
        self.max_amount = values.get('max_amount', self.max_amount)
        self.min_amount = values.get('min_amount', self.min_amount)
        self.cooldown = values.get('cooldown', self.cooldown)
        self.growth_rate = values.get('growth_rate', self.growth_rate)

        self.amount = self.start_amount


    def grow_resource(self):
        """Regrows the resource with `self.growth_rate`

        If the current amount of resources reaches 0 or lower, the
        cooldown is triggered. When the cooldown is past, resource
        amount will be reset to self.min_amount.
        """
        
        if self.in_cooldown:
            self.cur_cooldown -= 1
            if self.cur_cooldown <= 0:
                self.in_cooldown = False
                self.amount = self.min_amount
            return

        if self.amount <= 0:
            self.cur_cooldown = self.cooldown
            self.in_cooldown = True
            return

        self.amount += self.amount * self.growth_rate

        if (self.amount > self.max_amount):
            self.amount = self.max_amount


    def consume_resource(self, amount):
        """Consumes an amount of the resource.
        Can be seen as the agents going out to fish.

        Parameters
        ----------
        amount : `double`
            The amount of the resource to consume.

        Returns
        -------
        `double`
            The amount of requested resource if available,
            the remaining amount of the resource otherwise.
        """

        if self.amount - amount < 0:
            self.amount = 0
            return self.amount
        else:
            self.amount -= amount
            return amount


    def get_amount(self):
        return self.amount


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