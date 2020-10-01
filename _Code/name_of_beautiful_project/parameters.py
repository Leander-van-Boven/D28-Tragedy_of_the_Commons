"""This module contains the dictionary with the default parameters.

Explanation of parameters
-------------------------

agent_distributions:
    Contians the different groups of agents, 
        with their respective parameter values

        label: `str`
            the name of the group

        line_style: the style to use for the plot for this group.
            Refer to https://tinyurl.com/y9go69zm for possible options.

        agent_count: the amount of agents in the group

        min_social_value: the lower limit of the SVO for agents 
            in this group

        max_social_value: the upper limit of the SVO for agents
            in this group


        standard_param_deviation: how much the metabolism and 

        metabolism: the cost of staying alive (in energy / epoch)

        maximum_age: the maximum age for the agent


        procreate_req: how much energy an agent needs before it can
            procreate

        procreate_cost: cost of energy to procreate
"""

p = {
    "agent_distributions" : [
        {
            "label" : "proself",
            "line_style" : ':',
            "agent_count" : 50,
            "min_social_value" : 0,
            "max_social_value" : .25,

            "standard_param_deviation" : .1,
            "metabolism" : 2,
            "maximum_age" : 100,

            "procreate_req" : 16,
            "procreate_cost" : 10,
        },
        {
            "label" : "prosocial",
            "line_style" : '--',
            "agent_count" : 50,
            "min_social_value" : .75,
            "max_social_value" : 1,

            "standard_param_deviation" : .1,
            "metabolism" : 2,
            "maximum_age" : 100,

            "procreate_req" : 16,
            "procreate_cost" : 10,
        }
    ],

    "resource" : {
        "start_amount" : 1000,
        "max_amount" : 1000,
        "min_amount" : 0,
        "growth_rate" : 1.42,
        "energy_per_unit" : 1,
    },

    "simulation" : {
        "max_epoch" : 1000,
        "plot_interval" : 1,
        "print_interval" : 1
    }
}