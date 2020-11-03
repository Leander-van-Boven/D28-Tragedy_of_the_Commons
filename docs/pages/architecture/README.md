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
* `parameters.py`: Contains the default parameter dictionary. For more information, refer to [Parameters](/docs/PAGES/PARAMETERS/).
* `resource.py`: Contains the `Resource` class, specifying the consumption and growth behavriour of the resource pool.
* `simulation.py`: Contains the `Simulator` class, wherein the simulation is set up and run. 
* `util.py`: Contains some context-free helper methods.
* `sim.py`: Contains the command-line interface and imports `cpr_simulation` to set-up and run a simulation. For more informatin about the command-line interface, refer to [Interaction](/docs/pages/interaction/).

In the sections below, the `Agent`, `Resource` and `Simulation` classes are more thoroughly explained. 

# Agent 

```python
class Agent:
    def __init__(params):
        # Class constructor

    @classmethod
    def from_svo_distribution(cls, dist_params, n, 
                              agent_params=dict()):
        # Generate set of agents with their SVO's 
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
```
Because what would a common-pool resource be without any exploitants. 

# Resource

# Simulation