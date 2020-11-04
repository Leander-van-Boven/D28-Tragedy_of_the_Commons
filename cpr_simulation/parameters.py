"""This module contains the dictionary with the default parameters.

Refer to the documentation for a very thorough explanation of each
parameter:
https://leander-van-boven.github.io/D28-Tragedy_of_the_Commons/pages/parameters/
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

    # This parameter is set empty by default.
    # This is to allow for a variable amount
    # of distributions to be manually added.
    # The default values are specified in 
    # agent.py:from_svo_distribution()
    "svo_dist": {},

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
