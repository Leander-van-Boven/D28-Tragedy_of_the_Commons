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

## Agent construction
The constructor of `Agent`, `Agent.__init__()`, constructs a new instance of the `Agent` class. It fills all attributes based on the parameter dictionary `params`. In addition, the static method `Agent.from_svo_distribution()` can be used to make a collection of agents, with their social value orientation drawn from a multi-modal normal distribution.

In this method, the means and standard deviations are passed through the `dist_params` argument. However, instead of using this to make a single multi-modal normal distribution, we make multiple unimodal distributions. For each agent, we take one such distribution by chance, and sample its social value orientation from that. This is mathematically equivalent so sampling all agents from a multi-modal distribution. 

The initial SVO distribution can be altered through the `svo_dist` parameter. Refer to [Parameters](../parameters/) for more information.
{:.note}

## Agent act
The behaviour 'act', represented by the method `Agent.act()`, represents the behaviour of this agent for an entire epoch. In our model, the act comprises of two things:
* Metabolise some energy (agent's energy level decreases)
* Decide whether to go fishing (energy leven increases)

How much energy the agent metabolises is decided by a parameter that's constant across all agents. 

The agents' fish consumption can be altered through the  `agent:metabolism` and `agent:consumption_factor` parameters. Refer to [Parameters](../parameters/) for more information.
{:.note}

Whether to go fishing, and how much fish to catch, is decided by the *energy function*. The outcome of these functions relies solely on the agent's social value orientation and the amount of resource that's left. This model implements two such functions, which both are described in the sections below.

The energy function used by the agents can be altered through the `agent:behaviour` parameter. Refer to [Parameters](../parameters/) for more information.
{:.note}

### Base energy function
The base energy function, represented by the method `Agent.base_energy_function()`, is the initially proposed agent behaviour function. This functions is very naive in that it makes a black and white separation between pro-self and pro-social agents (<.5 SVO means pro-self, >=.5 SVO means pro-social). While pro-social agents will always fish their consumption, the consumption of the pro-self agents differs based on the available resources.  
Let $$A_p\subseteq A$$ be the set of all pro-self agents as a subset of the set of all agents. Each agent $$a\in A_p$$ has a predetermined and constant metabolism value, which we define here as $$m$$. An agent consumes a little more than they need, which is why a predefined and constant consumption factor is added. Let us define this factor as $$c$$.  
Say that the total amount of resource that's available when agent goes fishing is denoted as $$f_a$$. If the amount of resource that available fish for each agent falls below a certain threshold (denoted $$s$$), pro-self agents start behaving differently. Their behaviour can be defined as follows:

$$
\begin{array}{lr}c_a=
    \begin{cases}
        m\cdot c\cdot g\ & \frac{f_a}{|A|}<s\\
        m\cdot c & \text{otherwise}
    \end{cases} & \forall a\in A_p
\end{array}
$$

### Restricted energy function (default)
The restricted energy function, represented by the method `Agent.restricted_energy_function`(), builds on the base function by adding a epoch-based resource restriction. 

The point at which the restriction kicks in or out can be altered through the `simulation:res_limit_factor` and `simulation:res_unlimit_factor` parameters respectively. Refer to [Restricted model limit parameters](../parameters/restricted-model-limit-parameters) for more information.
{:.note}

If this restriction is active, agents are only allowed to fish if they would die otherwise. However, each agent has a chance of ignoring this restriction. The probability hereof is linearly dependent of the agent's social value orientation, i.e. if they range more towards pro-selfness, they are inclined to ignore the restriction more often.  
However, agents that choose to ignore this rule have have a probability of being caught. If they are catched red-handed, they are punished and can't fish for a predetermined number of epochs. 

The probability of an agent being caught and the amount of epochs they can't fish if they are caught can be altered through the `agent:caught_chance` and `agent:caught_cooldown_factor` parameters respectively. Refer to [Agent-specific parameters](../parameters/#agent-specific-parameters) for more information.
{:.note}

## Agent procreation
If agents have enough energy available, they can procreate. The procreation is implemented in the static method `Agent.procreate()`. Repeatedly, two random agents are taken from the list of parents and they procreate. Apart from the child's social value orientation, all attributes remain constant. The child's social value orientation is dynamic however, and is chosen depending on the parents' social value orientations and energy levels. This model implements two social value orientation inheritance functions, which are described in the sections below.

The social value orientation inheritance function can be altered through the `agent:svo_inheritance_function` parameter. Refer to [General agent parameters](../parameters/#general-agent-parameters) for more information.
{:.note}

### SVO inheritance from either parent (default)
This function is represented by the local method `svo_either_parent()` that is located within `Agent.procreate()`. With this method, the child's social value orientation is based on one of their parents. We first have to decide which parent to take, which is done probabilisticly based on the parents' energy level:

$$
\begin{align}
P(\mu_c=svo_{p1}) &= \frac{e_{p1}}{e_{p1}+e_{p2}}\\[2em]
P(\mu_c=svo_{p2}) &= \frac{e_{p2}}{e_{p1}+e_{p2}}\\[2em]
&=1-P(\mu_c=svo_{p1})
\end{align}
$$

The probabilities of the child's mean svo to become that of both parents. Here, $$P(\phi )$$ denotes the probability that $$\phi$$.
{:.figcaption}

Notice that $$\mu_c$$ is used instead of $$svo_c$$. This because the social value orientation of the child is drawn from a normal distribution with a predetermined standard deviation. Thus we get:

$$
\begin{array}{ll}svo_c = \max(\min(\alpha,1),\ 0) & \alpha \sim \mathcal{N}(\mu_c, \sigma_c)\end{array}
$$

The social value orientation is drawn from a normal distribution. Here, $$\sigma_c$$ denotes the predetermined standard deviation
{.figcaption}

The standard deviation for the final normal distribution can be altered through the `agent:svo_convergence_factor:svo_either_parent` parameter. Refer to [General Agents Parameters](../parameters/#general-agent-parameters) for more information.

### SVO inheritance from both parents
This function is represented by the lcoal method `svo_both_parents()` that is located within `Agent.procreate()`. With this method, the child's social value orientation is based on both parents. As before, we construct a normal distribution where the social value orientation is sampled from. However, in this case the mean $$\mu_c$$ is determined by the weighted mean of the parents' social value orientations:

$$
\mu_c=\frac{svo_{p1}\cdot e_{p1} + svo_{p2}\cdot e_{p2}}{e_{p1}+e_{p2}}
$$

So the mean social value orienation of the child lies somewhere between the social value orientations of its parents. The standard deviation depends on the actual distance of $$\mu_c$$ from the parents' social valure orientations:

$$
\sigma_c=\frac{1}{3}\cdot \min(\vert\mu_c, svo_{p1}\vert, \vert\mu_c, svo_{p2}\vert)\cdot t
$$

Put in words, the extremes of the normal distributions ($$\pm 3\sigma_c$$) are made so that it will not exceed the parents' social value orientation. That is, if $$t$$ is set to 1. This factor can thus be used to allow for some exploration in the social value orientation search space. 

The value of $$t$$ can be altered through the `agent:svo_convergence_factor:svo_both_parents` parameter. Refer to [General agent parameters](../parameters/#general-agent-parameters) for more information.
{:.note}

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

## Resource construction

## Growth functions
Three different growth functions are defined.

### Exponential

The exponential resource growth function is defined as follows:

$$
\begin{align}
r_{t+1} &= r_t + f(r_t)\\[2em]
f(x) &= e\cdot x
\end{align}
$$

Note that this function in itself isn't exponential. However, when it is repeatedly applied each epoch, it will be. This function has one parameter, $$e$$, which determines the amount of exponential growth.

The exponent $$e$$ can be altered through the `resource:gf_params:exponential:rate` parameter. Refer to [Exponential growth function](../parameters/$exponential-growth-function) for more information. 
{:.note}

### Nth root

The nth root function is defined as follows:

$$
\begin{align}
r_{t+1} &= r_{t} + g(r_t)\\[2em]
g(x) &= a\cdot\frac{1}{(x-\frac{t_x}{a})^\frac{1}{n}}-t_y
\end{align}
$$

The value of this one over log function decreases as $$r_t$$ increases. This allows for a radical resource growth at the start, but a more gradual resource growth if there is already a high amount of resources available. This function was designed to be resemble a 'nested' common-pool resource, where the lake is able to support but a limited amount of fish. The exponents $$a$$, $$t_x$$, $$t_y$$ and $$n$$ have the following implications on $g(x)$:

* $a$: Scales the whole function. Scales any properties that are already existent.
* $t_x$: Translation over x axis. Makes the decrease 

### Logarithmic (default)

The logarithmic function is defined as follows:

$$
\begin{align}
r_{t+1} &= r_{t} \cdot h(r_t)\\[2em]
h(x) &= \frac{a}{\log(x)+\frac{a}{s-t}} + t
\end{align}
$$

 With the current parameters



# Simulation
```python
class Simulation:
    def __init__(self, param_dict, printer=None, logger=None, 
                 row_head=[], verbose=True):
        # Params and modules initializer
    
    def get_agent_count(self, min_social_values=0, max_social_value=1):
        # Get amount of agents based on min and max SVO

    def add_agent(self, agent):
        # Adds an agent to the simulation
    
    def remove_agent(self, agent):
        # Removes an agent from the simulation

    def generate_simulation(self):
        # Initializes and runs the simulation

    def plot_results(self):
        # Updates the real-time plot

    def print_results(self):
        # Updates the command-line output

    def log_results(self):
        # Updates the CSV logger
```

This class is the spine of the simulation, hence its name. Here is where the agents and fish live and where the actual results of the model are produced by controlling both the community of agents and the common resource.

## Simulation construction
The constructor of `Simulation`, `Simulation.__init__()`{:.python}, constructs a new intance of the `Simulation` class. Not only will this class set the values of its own attributes and variables, it will also receive the parameters for both the `Agent` and `Resource` classes, of which it will instantiate instances. Here the `Simulation` class also receives a reference to a `ResultPlotter` or `CsvLogger` class if specified via the command-line and/or instatiated in `main.py`. 
Furthermore, the thresholds for activating and deactivating the resource restriction are calculated.

## Simulation loop
### Initialisation
Before the simulation goes into its simulation loop, the simulation is first initialised:
* First the list of agents is initialised using the [`Agent.from_svo_distribution()`](#agent-construction) function.
* Then the resources are [`initialised`](#resource-construction).
* The current statistics and epoch counter are reset.
* If required, the initial statistics are plotted, printed and logged.

### The epoch loop
Once initialisation is complete, the epoch loop starts. This loop will run untill either of the stopping conditions are met. There are two different stopping conditions:
* Either the maximum amount of epochs are reached; or
* The amount of alive agents drops under a certain threshold.
The first stopping condition can be specified by setting the `simulation:max_epoch` parameter. The second stopping condition is set to 2. This is done so since 1 agent will not be able to procreate, and will eventually die of age. It may however happen that all alive agents die all within the epoch, therefore we need to check whether $$|A|<2$$ (where $$A$$ denotes the set of alive agents), instead of $$|A|=1$$

# Output

## Real-time plot
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

## CSV logger
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

# util.py
def do_nothing(self, *args, **kwargs):
    pass

def dd_factory(d=None):
    # asd

def update_dict(d, u, omit_new=False):
    # asd
```

