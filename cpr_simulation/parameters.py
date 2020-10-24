"""This module contains the dictionary with the default parameters.

Explanation of parameters
-------------------------

agent_distributions : `dict`,
    Contians the different groups of agents, 
        with their respective parameter values.
    The key for each group denotes it label (this is also shown as line
        label in the legend of the real-time plot).

    line_style : `str`,
        The style to use for the plot for this group.
        Refer to https://tinyurl.com/y9go69zm for possible options.
        (#NOTE not all options seem to work)

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
    "agent" : {
        "count" : 100,
        "svo_convergence_factor" : 4,
        "params" : {
            "metabolism" : 5,
            "maximum_age" : 15,

            "consumption_factor" : 3,
            "procreate_cost_factor" : 4,
            "procreate_req_factor" : 5,
            "start_energy_factor" : 3,
                   
            "behaviour" : "restricted_energy_function", 
            # possible values: "base_energy_function", 
            #                  "restricted_energy_function"

            # Base Model Parameters
            "scarcity" : 10,
            "greed" : 5,

            # Restricted Model Parameters
            "res_limit_factor" : 2,
            "res_unlimit_factor" : 3,
            "caught_chance" : .25,
            "caught_cooldown" : 7,
        }
    },

    "svo_distributions" : [
        # [mean_i, variance_i]
        [0.25, 0.125],
        [0.75, 0.125],
    ],

    "resource" : {
        "start_amount" : 5000,
        "max_amount" : 10000,
        "min_amount" : 100,
        "cooldown" : 10,
        "growth_rate" : .25
    },

    "simulation" : {
        "max_epoch" : 1000,
        "plot_interval" : 1,
        "print_interval" : 1,
        "log_interval" : 1,
    },

    "plotter_params" : {
        "svo_bar_count" : 20,
    },

    "logger_params" : {
        "separator" : ',',
        "separator_replacement" : ' ',
        "print_interval" : 1
    },

    "batch" : 1,
}