---
layout: page
title: Model Parameters
---

1. toc
{:toc title="Contents"}

# General
Despite its relative simplicity, this model already contains a lot of parameters. To enhance readability and scalability, these parameters are defined in a dictionary grouped by there architectural part in the model. 

The following structure for the parameter dictionary arises:
```python
parameters = {
    "agent": {
        # General agent parameters
        "count": 100,
        "svo_procreation_function": "svo_either_parent"
        # Possible values:          "svo_either_parent
        #                           "svo_between_parents"
        "svo_convergence_factor": {
            "svo_either_parent": 0.15,
            "svo_between_parents": 3
        },
        "params": {
            # Agent specific prameters
        }
    },
    "svo_dist": {
        "d1": {
            "m" : 0.5,
            "s" : 0.1
        },
        # More distributions can be added here, or via the CLI
    },
    "resource": {
        # General resource parameters
        "growth_function": "logarithmic"
        "gf_params": {
            # Growth function parameters
        }
    },
    "simulation": {
        # General simulation parameters
    },
    "plotter_params": {
        # General real-time plot parameters
    },
    "logger_params": {
        # General csv-logger parameters
    },

    # Do not override this value!
    # For internal purposes only
    "batch": 1
}
```
Structure of the parameters dictionary with placeholder values.
{:.figcaption}

<!-- * [Agent Parameters](agent_parameters.md){:.heading.flip-title} --- An explanation of each parameter for the agents.
* [Resource Parameters](resource_parameters.md){:.heading.flip-title} --- An explanation of each parameter for the resources.
* [Simulation Parameters](simulation_parameters.md){:.heading.flip-title} --- An explanation of each parameter for the simulation.
* [Output Parameters](output_parameters.md){:.heading.flip-title} --- An explanation of each parameter for the command-line output, csv-logger and real-time plot. -->

Below is a listing of **all** parameters in the model that can be changed.  
Use `--param [parameter_location]=[value]` to change a parameter using the command-line interface. The `parameter_location` is given by the first text of each listing below. The type of value is put between parentheses.

# Agent Parameters
> Refer to the explanation of the [Agent](/D28-Tragedy_of_the_Commons/pages/architecture/agent/) class for a full explanation of the effects of each parameter.

## General agent parameters
* `agent:count` (`int`): Determines the start amount of agents.
* `agent:svo_procreation_function` (`str`): Function to use to determine the SVO of a new agent. Can be either `"svo_either_parent"` or `"svo_between_parents"`.
* `agent:svo_convergence_factor:svo_either_parent` (`float`): The SVO convergence factor for the `svo_either_parent` procreate function.
* `agent:svo_convergence_factor:svo_between_parents` (`float`): The SVO convergence factor for the `svo_between_parents` procreate function.

## Agent-specific parameters
* `agent:params:metabolism` (`float`): Sets the cost of staying alive (in energy / epoch).
* `agent:params:maximum_age` (`int`): Sets the mean of the Gaussian distribution used to determine the actual age of the agent (in epochs).
* `agent:params:maximum_age_std_factor` (`float`): Sets the standard deviation of the Gaussian distribution used to determine the actual maximum age of the agent.

* `agent:params:consumption_factor` (`float`): This factor is multiplied with the metabolism to determine the amount of fish an agent will catch (in terms of energy), if it is allowed. (<1 values means that the consumption will be lower than the metabolism, therefore not allowing the agent to fish more energy than it loses per epoch.)
* `agent:params:procreate_cost_factor` (`float`): This factor is multiplied with the metabolism to determine the amount of energy it costs to procreate. Values >1 are desirable.
* `agent:params:procreate_req_factor` (`float`): This factor is multiplied with the metabolism to determine the amount of energy an agent needs to have before it is allowed to procreate. Values >1 are desirable.
  
* `agent:params:behaviour` (`str`): Sets the behaviour model to use for the agents. Currently the only two options are `"base_energy_function"` and `"restricted_energy_function"`.
  
### Base model parameters
* `agent:params:scarcity` (`float`): If $$\frac{current\_resource\_amount}{agent\_count}<value$$, pro-self agents (all agents with a SVO<.5) will try to fish more, therefore allowing them to stockpile energy.
* `agent:params:greed` (`float`): When resources are scarce, pro-self agents (all agents with a SVO<.5) will try to fish more: $$consumption\cdot value$$.
  
### Restricted model parameters
* `agent:params:caught_chance` (`float`): When an agent violates the restriction when the restriction is active, this value determines the chance that the agent is caught violating the restriction. (0.5 means 50% chance of getting caught)
* `agent:params:caught_cooldown_factor` (`float`): When an agent is caught violating the restriction when it is active, this parameter determines how long this agent is prohibited from fishing (in epochs).

# SVO Distributions Parameters
> Refer to the explanation of the [Agent](/D28-Tragedy_of_the_Commons/pages/architecture/agent/) class for a full explanation of the effects of each parameter.

The `svo_dist` paramater is a dictionary containing the Gaussian distributions from which the starting SVO of the initial agent group is drawn. Multiple distributions can be added. Each distributions should be a dictionary with an unique key (d1, d2, ..., dn) and follow the following structure:
```python
"svo_dist": {
    "d1": {
        "m": 0.5,
        "s:" 0.1
    }
}
```
The `"m"` key then denotes the mean of the Gaussian distribution, `"s"` then denotes the standard deviation of the Gaussian distribution.

# Resource Parameters
> Refer to the explanation of the [Resource](/D28-Tragedy_of_the_Commons/pages/architecture/resource/) class for a full explanation of the effects of each parameter.

* `resource:start_amount` (`float`): The amount of resources to start the simulation with.
* `resource:max_amount` (`float`): The maximum amount for the resources. If resources grow beyond this value, it is set to this value. When set to $$-1$$, this parameter is ignored. This parameter can be used to keep resources within a reasonable amount, allowing the plot to not slow down too much.
* `resource:min_amount` (`float`): The minimum amount of resources. If the resources drop below this limit, it is reset to this value.
* `resource:growth_function` (`str`): The growth function to use. Choices are: `"exponential"`, `"logarithmic"` and `"nroot"`.

## Growth function parameters
The parameters below are sorted by the resource growth function they apply to. 
### Exponential growth function
* `resource:gf_params:exponential:rate` (`float`): The exponential rate for the exponential growth function.
  
### Logarithmic growth function
* `resource:gf_params:logarithmic:a` (`float`): The scaling factor of the logarithmic growth function.
* `resource:gf_params:logarithmic:t` (`float`): The translation factor of the logarithmic growth function.
* `resource:gf_params:logarithmic:s` (`float`): The initial jump scaling factor of the logarithmic growth function.
   
### NRoot growth function
* `resource:gf_params:nroot:a` (`float`): The scaling factor of the nroot growth function.
* `resource:gf_params:nroot:tx` (`float`): The translation factor over the x axis of the nroot growth function.
* `resource:gf_params:nroot:ty` (`float`): The translation factor over the y axis of the nroot growth function.
* `resource:gf_params:nroot:n` (`float`): The base of the root that's used in the nroot growth function. ($$\sqrt[n]{x}$$)

# Simulation Parameters
> Refer to the explanation of the [Simulation](/D28-Tragedy_of_the_Commons/pages/architecture/simulation/) class for a full explanation of the effects of each parameter.

* `simulation:max_epoch` (`int`): The maximum amount of epochs for the simulation.
* `simulation:plot_interval` (`int`): How many every epoch the real-time plot should be updated. This parameter is only used when the real-time plot is enabled.
* `simulation:print_interval` (`int`): How many every epoch the console should be updated.
* `simulation:log_interval` (`int`): How many every epoch the current stats of the simulation should be posted to the logger. (When set to e.g. 2, the stats of epoch 1,3,5,etc. will be logged. No buffer is created!).
* `simulation:sleep` (`float`): The amount of time (in seconds) to pause the simulation between each epoch. Setting this value to >0 allows for better oversight of the model, but will obsviously make the simulation take longer to complete.
  
## Restricted model limit parameters
* `simulation:res_limit_factor` (`float`): Determines when to activate the restriction in the restricted energy function based on when $$agent\_count\cdot consumption\cdot value$$ is greater than the currently available resources. Values <1 mean that the restriction will become active at a point that if all agents would fish their consumption, some agents will not get any resources.
* `simluation:res_unlimit_factor` (`float`): Determines when to deactivate the restriction in the restricted energy function. This follows the same functions as for the `res_limit_factor` parameter. It is desirable to set `res_limit_factor`<`res_unlimit_factor` to allow the resources to regrow before all agents are allowed to fish their consumption again (resulting in the restriction to become active again at some point).

# Output Parameters
## Real-time plot parameters
* `plotter_params:svo_bar_count` (`int`): The amount of bars to show in the real-time histogram plot. To allow fast plotting this value should be kept below ~50 [^1].
  
## CSV-Logger parameters
* `logger_params:separator` (`str`): The separator to use to separate the individual items in a row with.
* `logger_params:separator_replacement` (`str`): The string to use when an item in a row contains the separator.


[^1]: This is a recommendation for average speed computers. Below 100 should still run fine on fast computers. Default 20 should be runnable at decent speed on all kinds of computers.