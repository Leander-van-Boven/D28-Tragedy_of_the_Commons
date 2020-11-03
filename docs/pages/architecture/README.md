---
layout: page
title: Model Architecture
---

1. toc
{:toc title="Contents"}

# Introduction

On this page, the structure and architecture of the implementation is explained. The simulation is built using the object-oriented programming paradigm, which means that each entity (agent, resource, etc.) is represented by a `class` containing all its values and behaviours. The files that are relevant to the implementation model are:

```
D28-Tragedy_of_the_Commons/
├── cpr_simulation/
│   ├── __init__.py
│   ├── agent.py
│   ├── exception.py
│   ├── logger.py
│   ├── output.py
│   ├── parameters.py
│   ├── resource.py
│   ├── simulation.py
│   └── util.py
└── sim.py
```
* `__init__.py`: Module initiator file that determines that methods and attributes are exposed if `cpr_simluation` is imported as a module.
* `agent.py`: Contains the `Agent` class, specifying the behaviour of each agent.
* `exception.py`: Constains multiple custom exceptions that can be raised by `cpr_simulation`.
* `logger.py`: Contains the CSV logger logic.
* `output.py`: Contains the real-time plotting logic. 
* `parameters.py`: Contains the default parameter dictionary. For more information, refer to [Parameters](/D28-Tragedy_of_the_Commons/pages/parameters/).
* `resource.py`: Contains the `Resource` class, specifying the consumption and growth behavriour of the resource pool.
* `simulation.py`: Contains the `Simulator` class, wherein the simulation is set up and run. 
* `util.py`: Contains some context-free helper methods.
* `sim.py`: Contains the command-line interface and imports `cpr_simulation` to set-up and run a simulation. For more informatin about the command-line interface, refer to [Interaction](/D28-Tragedy_of_the_Commons/pages/interaction/).

In the sections below, the `Agent`, `Resource` and `Simulation` classes are more thoroughly explained. 

# Agent 
```python
class Agent:
    # Attributes:
    #  - energy
    #  - social_value_orientation

    def __init__(self, params, **kwargs):
        # Class constructor

    @classmethod
    def from_svo_distribution(cls, dist_params, n, 
                              agent_params=dict()):
        # Generate set of n agents with their SVO's 
        # sampled from a multi-modal normal 
        # distribution 

    def act(self, sim):
        # Epoch behaviour entry point

    def base_energy_function(self, sim):
        # Base energy function behaviour

    def restricted_energy_function(self, sim):
        # Restricted energy function behaviour

    @classmethod
    def procreate(cls, sim, parents):
        # Procreation function

        def svo_either_parent():
            # SVO inheritance function based on
            # either parent

        def svo_both_parents():
            # SVO inheritance function based on
            # both parents
```
Because what would a common-pool resource be without any exploitants. 
{:.figcaption}

## Agent Construction
The constructor of `Agent`, `Agent.__init__()`, constructs a new instance of the `Agent` class. It fills all attributes based on the parameter dictionary `params`. In addition, the static method `Agent.from_svo_distribution()` can be used to make a collection of agents, with their social value orientation drawn from a multi-modal normal distribution.

In this method, the means and standard deviations are passed through the `dist_params` argument. However, instead of using this to make a single multi-modal normal distribution, we make multiple unimodal distributions. For each agent, we take one such distribution by chance, and sample its social value orientation from that. This is mathematically equivalent so sampling all agents from a multi-modal distribution. 

> The initial SVO distribution can be altered through the `svo_dist` parameter. Refer to [Parameters](D28-Tragedy_of_the_Commons/pages/parameters) for more information.

## Agent Act
The behaviour 'act', represented by the method `Agent.act()`, represents the behaviour of this agent for an entire epoch. In our model, the act comprises of two things:
* Metabolise some energy (agent's energy level decreases)
* Decide whether to go fishing (energy leven increases)

How much energy the agent metabolises is decided by a parameter that's constant across all agents. 

> The agents' fish consumption can be altered through the  `agent:metabolism` and `agent:consumption_factor` parameters. Refer to [Parameters](D28-Tragedy_of_the_Commons/pages/parameters) for more information.

Whether to go fishing, and how much fish to catch, is decided by the *energy function*. The outcome of these functions relies solely on the agent's social value orientation and the amount of resource that's left. This model implements two such functions, which both are described in the sections below.

> The energy function used by the agents can be altered through the `agent:behaviour` parameter. Refer to [Parameters](D28-Tragedy_of_the_Commons/pages/parameters) for more information.
### Base Energy Function
The base energy function, represented by the method `Agent.base_energy_function()`, .... 
### Restricted Energy Function (Default)
The restricted energy function, represented by the method `Agent.restricted_energy_function`(), builds on the base function by adding a epoch-based resource restriction. 

> The point at which the restriction kicks in or out can be altered through the `simulation:res_limit_factor` and `simulation:res_unlimit_factor` parameters respectively. Refer to [Parameters](D28-Tragedy_of_the_Commons/pages/parameters) for more information.

If this restriction is active, agents are only allowed to fish if they would die otherwise. However, each agent has a chance of ignoring this restriction. The probability hereof is linearly dependent of the agent's social value orientation, i.e. if they range more towards pro-selfness, they are inclined to ignore the restriction more often.  
However, agents that choose to ignore this rule have have a probability of being caught. If they are catched red-handed, they are punished and can't fish for a predetermined number of epochs. 
> The probability of an agent being caught and the amount of epochs they can't fish if they are caught can be altered through the `agent:caught_chance` and `agent:caught_cooldown_factor` parameters respectively. Refer to [Parameters](D28-Tragedy_of_the_Commons/pages/parameters) for more information.

## Agent Procreation
If agents have enough energy available, they can procreate. The procreation is implemented in the static method `Agent.procreate()`. Repeatedly, two random agents are taken from the list of parents and they procreate. Apart from the child's social value orientation, all attributes remain constant. The child's social value orientation is dynamic however, and is chosen depending on the parents' social value orientations and energy levels. This model implements two social value orientation inheritance functions, which are described in the sections below.

### SVO Inheritance from Either Parent (Default)
This function is represented by the local method `svo_either_parent()` that is located within `Agent.procreate()`. With this method, the child's social value orientation is based on one of their parents. We first have to decide which parent to take, which is done probabilisticly based on the parents' energy level:
$$
P(\mu_c=svo_{p1}) = \frac{e_{p1}}{e_{p1}+e_{p2}}\\
P(\mu_c=svo_{p2}) = \frac{e_{p2}}{e_{p1}+e_{p2}}\\
P(\mu_c=svo_{p1}\vee svo_{p2}) =1
$$
Notice that $$\mu_c$$ is used instead of $$svo_c$$. This because the child

### SVO Inheritance from Both Parents

# Resource
```python
class Resource:
    def growth_exponential(self, val, rate):
        # Exponential growth function

    def growth_logarithmic(self, val, a, t, s):
        # 1 / log growth function

    def growth_nroot(self, a, tx, ty, n):
        # 1 / nth root growth function

    def __init__(self, params):
        # Resource pool constructor

    def grow_resource(self):
        # Resource growth function entry point

    def consume_resource(self, amount):
        # Resource consumption entry pont
```

# Simulation
```python
class Simulation:
    def __init__(self, param_dict, printer=None, logger=None, row_head=[], verbose=True):
        # Params and modules initializer
    
    def get_agent_count(self, min_social_values=0, max_social_value=1):
        # 
```

# Ouput

## Real-Time Plot
```python
class ResultsPlotter:
    def __init__(self, start_agent, svo_bar_count, start_resource, fullscreen):
        # Sets up all parameters and attributes of the class
    
    def init_plot(self):
        # Initializes the plot for the animation

    def update(self, data):
        # Updates the plot from the data provided

    def start_printer(self, data_gen):
        # Initializes the animation and shows the plot

    def save_fig(self, path):

```

## CSV Logger
```python
class 
```

# Utilities
```python
class InvalidArgumentError(Exception):
    pass

class MissingArgumentError(Exception):
    pass

class InvalidParameterError(Exception):
    pass
```

