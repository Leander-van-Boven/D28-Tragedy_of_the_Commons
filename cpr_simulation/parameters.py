"""This module contains the dictionary with the default parameters.

Explanation of parameters
-------------------------

agent : `dict`,
    agent_count : `int`,
        The amount of agents in the group.

    min_social_value : `float`,
        The lower limit of the SVO for agents in this group.

    max_social_value : `float`, 
        The upper limit of the SVO for agents in this group.

    metabolism : `double`,
        The cost of staying alive (in energy / epoch)

    consumption : `double`,
        The amount of fish per epoch an agent catches.

    maximum_age : `int`,
        The maximum age for the agent (in epochs).

    mutation_factor : `float`,
        This factor is used as standard deviation in a gaussian
        distribution for calculating a modification value for above
        mentioned parameters (metabolism, consumption, max_age).
        This will cause more variation within the group of agents.

    procreate_req : `double`,
        How much energy an agent needs before it may procreate.

    procreate_cost : `double`,
        Cost of energy to procreate.

    # Restricted Energy Function Parameters
    res_limit_factor : `double`,
        This factor is multiplied by the amount of agents alive at that
        point. If the resource amount is below the calculated value, 
        the resources are assumed as 'scarce' and the restriction rule
        is activated.
    caught_chance : `float`,
        If an agent violates the restriction rule, this parameter
        determines the chance the agent gets caught.
    caught_cooldown : `int`,
        If an agent is caught violating the restriction rule, this
        parameter determines the amount of epochs the agent is prohibited
        from fishing.


resource : `dict`,
    Contains the parameters for the common resource (fish in our case).

    start_amount : `double`,
        The starting amount for the common resource.

    max_amount : `double`,
        The maximum amount for the common resource.
        If the amount of resource exceeds this limit, 
            the amount of resource gets reset to this limit.

    min_amount : `double`,
        The minimum amount for the common resource.
        If the amount of resource gets lower than this limit,
            the amount of resource gets reset to this limit.

    cooldown : `int`,
        Determines the amount of epochs that the resource will be at 0.
        When cooldown amount of epochs are past the resource will be set
        at min_amount.

    growth_rate : `double`,
        Determines the percentage with which the resource growths /epoch.
        0 means no regrowth, 1 means a doubling of the resource, etc.


simulation : `dict`,
    Contains the parameters for the simulation.

    max_epoch : `int`,
        The maximum amount of epochs for the simulation.

    plot_interval : `int`,
        How many every epoch the plot should be updated,
        only used when real-time plot is enabled.

    print_interval : `int`,
        How many every epoch the console should be updated.


logger_params : `dict`,
    Contains parameters for the CSV logger.
    
    separator : `str`,
        The separator the separate each item in a datarow with.

    separator_replacement : `str`,
        The value to replace the separator with 
        if it occurs in a value.


run : `int`,
    Determines the amount of times the simulation is run, 
    with the specified parameters.
"""

default_params = {
    "agent": {
        "count": 100,

        "svo_inheritance_function": "svo_either_parent",
        # Possible values:          "svo_either_parent"
        #                           "svo_between_parents"
        "svo_convergence_factor": {
            "svo_either_parent": 0.15,
            "svo_between_parents": 3
        },

        "params": {
            "metabolism": 5,
            "maximum_age": 30,
            "maximum_age_std_factor": 0.05,

            "consumption_factor": 1.8,
            "procreate_cost_factor": 3.9,
            "procreate_req_factor": 1.2,
            "start_energy_factor": 1.3,

            "behaviour": "restricted_energy_function",
            # Possible values: "base_energy_function",
            #                  "restricted_energy_function"

            # Base Model Parameters
            "scarcity": 10,
            "greed": 5,

            # Restricted Model Parameters
            "caught_chance": 0.2,
            "caught_cooldown_factor": 0.3,
        }
    },

    "svo_dist": {
        "d1": {
            "m": 0.5,
            "s": .1
        },
        "d2": {
            "m": 0.5,
            "s": .1
        }
    },

    "resource": {
        "start_amount": 4000,
        "max_amount": -1,
        "min_amount": 1,

        "growth_function": "logarithmic",
        # Possible values: "exponential",
        #                  "logarithmic",
        #                  "nroot"
        "gf_params": {
            "exponential": {
                "rate": .25,
            },
            "logarithmic": {
                "a": 6,  # Scaling
                "t": 0,  # Translation
                "s": 3,  # Start jump
            },
            "nroot": {
                "a": 2500,   # Scaling
                "tx": 0,     # Translation x
                "ty": 1400,  # Translation y
                "n": 16,     # Root base
            },
        },
    },

    "simulation": {
        "max_epoch": 1000,
        "plot_interval": 1,
        "print_interval": 1,
        "log_interval": 1,
        "sleep": 0,

        # Restriction check parameters
        "res_limit_factor": 3,
        "res_unlimit_factor": 4,
    },

    "plotter_params": {
        "svo_bar_count": 20,
    },

    "logger_params": {
        "separator": ',',
        "separator_replacement": ' '
    },

    # Do not override this value!
    # For internal purposes only
    "batch": 1,
}
