"""This module contains the dictionary with the default parameters.

Explanation of parameters
-------------------------

agent_distributions:
    Contians the different groups of agents, 
        with their respective parameter values.

    label: `str`,
        The name of the group.

    line_style: `str`,
        The style to use for the plot for this group.
        Refer to https://tinyurl.com/y9go69zm for possible options.

    agent_count: `int`,
        The amount of agents in the group.

    min_social_value: `float`,
        The lower limit of the SVO for agents in this group.

    max_social_value: `float`, 
        The upper limit of the SVO for agents in this group.


    standard_param_deviation: `float`,
        How much the actual metabolism, consumption and maximum_age 
        may deviate from the set value (.1 means 10%).

    metabolism: `double`,
        The cost of staying alive (in energy / epoch)

    consumption: `double`,
        The amount of fish per epoch an agent catches.

    maximum_age: `int`,
        The maximum age for the agent (in epochs).


    procreate_req: `double`,
        How much energy an agent needs before it may procreate.

    procreate_cost: `double`,
        Cost of energy to procreate.


resource:
    Contains the parameters for the common resource (fish in our case).

    start_amount: `double`,
        The starting amount for the common resource.

    max_amount: `double`,
        The maximum amount for the common resource.
        If the amount of resource exceeds this limit, 
            the amount of resource gets reset to this limit.

    min_amount: `double`,
        The minimum amount for the common resource.
        If the amount of resource gets lower than this limit,
            the amount of resource gets reset to this limit.

    growth_rate: `double`,
        Determines the percentage with which the resource growths /epoch.
        0 means no regrowth, 1 means a doubling of the resource, etc.


simulation:
    Contains the parameters for the simulation.

    max_epoch: `int`,
        The maximum amount of epochs for the simulation.

    plot_interval: `int`,
        How many every epoch the plot should be updated,
        only used when real-time plot is enabled.

    print_interval: `int`,
        How many every epoch the console should be updated.
"""

default_params = {
    "agent_distributions" : [
        {
            "label" : "proself",
            "line_style" : ':',
            "agent_count" : 25,
            "min_social_value" : 0,
            "max_social_value" : .25,

            "standard_param_deviation" : .1,
            "start_energy_multiplier" : 3,
            "metabolism" : 1,
            "consumption" : 1,
            "maximum_age" : 100,

            "procreate_req" : 16,
            "procreate_cost" : 10,
        },
        {
            "label" : "prosocial",
            "line_style" : '--',
            "agent_count" : 75,
            "min_social_value" : .75,
            "max_social_value" : 1,

            "standard_param_deviation" : .1,
            "start_energy_multiplier" : 3,
            "metabolism" : 1,
            "consumption" : 1,
            "maximum_age" : 100,

            "procreate_req" : 16,
            "procreate_cost" : 10
        }
    ],

    "resource" : {
        "start_amount" : 250,
        "max_amount" : 250,
        "min_amount" : 0,
        "growth_rate" : .25
    },

    "simulation" : {
        "max_epoch" : 1000,
        "plot_interval" : 1,
        "print_interval" : 1
    }
}