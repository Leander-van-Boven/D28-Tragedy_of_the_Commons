import math

from functools import partial
from .util import do_nothing


class Resource:
    """This class represents the common resource, or fish in our case.

    Refer to the documentation
    (https://leander-van-boven.github.io/D28-Tragedy_of_the_Commons/ 
        pages/architecture/#resource) 
    for a thorough explanation of this class.
    """

    print = do_nothing

    def __init__(self, params):
        """Resource class constructor

        Parameters
        ----------
        params : `dict`,
            The parameter dictionary
        """

        self.start_amount = params.get('start_amount', 100)
        self.max_amount = params.get('max_amount', -1)
        self.min_amount = params.get('min_amount', 1)
        self.cooldown = params.get('cooldown', 10)
        self.growth_rate = params.get('growth_rate', 0.2)
        self.in_cooldown = False

        self.growth = eval(f"self.growth_{params['growth_function']}")
        self.growth = partial(
            self.growth, **params['gf_params'][params['growth_function']])

        self.amount = self.start_amount

    def growth_exponential(self, val, rate):
        """An exponential growth function.

        Parameters
        ----------
        val : `float`,
            The previous resource value
        rate : `float`,
            The exponential rate

        Returns
        -------
        `float`
            The new resource value
        """
        return val + (val * rate)

    def growth_logarithmic(self, val, a, t, s):
        """A growth function based on a log10.

        Parameters
        ----------
        val : `float`
            The previous resource value
        a : `float`
            Scaling factor
        t : `float`,
            Translation factor
        s : `float`,
            Jump scaling factor

        Returns
        -------
        `float`
            The new resource value
        """
        return val * ((a / (math.log10(val) + (a / (s - t)))) + t)

    def growth_nroot(self, val, a, tx, ty, n):
        """A growth function based on the nth root.

        Parameters
        ----------
        val : `float`,
            The previous resource value
        a : `float`,
            Scaling factor
        tx : `float`,
            Translation factor over x axis
        ty : `float`,
            Translation factor over y axis
        n : `float`,
            Root base

        Returns
        -------
        `float`
            The new resource value
        """
        return val + max(a * (1 / ((val - (tx / a)) ** (1 / n)) - ty / a), 0)

    def grow_resource(self):
        """Regrows the resource with `self.growth_rate`

        If the current amount of resources reaches 0 or lower, the
        cooldown is triggered. When the cooldown is past, resource
        amount will be reset to self.min_amount.
        """

        if self.amount < self.min_amount:
            self.amount = self.min_amount

        growth = self.growth(self.amount)
        self.print(
            f"Resource: {self.amount:4.2f},\t growing {growth:.2f},", end='')
        self.amount = growth
        self.print(f"\tnow {self.amount:.2f}")

        if self.max_amount > 0 and self.amount > self.max_amount:
            self.amount = self.max_amount

    def consume_resource(self, amount):
        """Consumes an amount of the resource.
        Can be seen as the agents going out to fish.

        Parameters
        ----------
        amount : `double`,
            The amount of the resource to consume.

        Returns
        -------
        `double`,
            The amount of requested resource if available,
            the remaining amount of the resource otherwise.
        """

        if self.amount - amount < 0:
            self.amount = 0
            return self.amount
        else:
            self.amount -= amount
            return amount