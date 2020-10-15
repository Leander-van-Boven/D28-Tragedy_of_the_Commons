# Tragedy of the Commons Repository
### DMAS project, group D28

A tragedy about a planet with a single island in a sea of fish run by a bunch of self-ish and self-less agents.

## Structure of this repository
> All files are still under development and are heavily subdue of changes.

* The folders named to each group member contains some personal files or found literature.

* The `_Code` folder contains the simulation code and interface:
  - [`cpr_simulation`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/tree/master/_Code/cpr_simulation) is the module that contains the simulation code. 
  - [`scenarios`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/tree/master/_Code/scenarios) contains different scenarios that can be run on the simulation that we found interesting. 
  - [`figures`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/tree/master/_Code/figures) contains interesting figures.
  - [`sim.py`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/sim.py) implements a command-line interface for the `cpr_simulation` module.

* Structure of the `_Code/cpr_simulation` folder:
  - [`main.py`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/cpr_simulation/main.py) is the entry point to the module. This file contains methods that can be used to run and save simulations. These methods are exposed when the module is imported.
  - [`simulation.py`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/cpr_simulation/simulation.py) contains the `Simulator` class. This class runs the simulation. It manages changes to the common resource and the changes to the agents as a result of the changes in the resource, and vice-versa.
  - [`agent.py`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/cpr_simulation/agent.py) contains the `Agent` class. This class represents the agents of our model and contains their properties. 
  - [`resource.py`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/cpr_simulation/resource.py) contains the `Resource` class. This class represents the common resource (fish) of our model. Includes all properties and methods that change these properties unique to this class.
  - [`parameters.py`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/cpr_simulation/parameters.py) contains the default parameters that are used in the simulation.
  - [`output.py`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/cpr_simulation/output.py) is used to plot the results from the model after and during the simulation.
  - [`logger.py`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/cpr_simulation/logger.py) contains a class that is used to construct and write CSV files.
  - [`test.py`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/cpr_simulation/test.py) (_can be ignored_) is used to try out pieces of code.
  - [`redundant.txt`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/cpr_simulation/redundant.txt) (_can be ignored_) contains some deprecated and/or redundant snippets of code.



## How to run the simulation
### Prerequisites
* The simulation assumes Python 3.6+, and requires the modules `numpy`, `argparse`, and `matplotlib` to be installed.
  
  ```
  pip3 install numpy argparse matplotlib
  ``` 
* Download the code by cloning this repository.
  
  ```
  git clone https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons
  ```
### Usage
The simulation itself is encapsulated in the module called `cpr_simulation`. There are two ways to use this module: either by importing this module in a custom Python script or interactive notebook, or by using the included command-line interface. We recommend the latter, as it is the quickest way to get a simulation up and running. Its controls are documented below.

After following the steps to install the simulation, open your favourite terminal and `cd` into `./_Code/`. The CLI can now be accessed through `sim.py`. The most important (and the only one that's required) argument, is the `command` argument, with possible choices being `run`, `save` and `list`. Using `run` will run a simulation, `save` saves a previously run simulation as a scenario, and `list` lists all saved scenarios. The most import commands are thus:
* To run a single simulation with default parameters, run 
  ```shell
  python sim.py run
  ```
* To inspect all possible command-line arguments, run
  ```shell
  python sim.py --help
  ```
* Some notes regarding different command-line arguments:
  * With the `-n`/`--name` argument, the behaviour is different bepending on the `command` argument. 
    * If `command` is set to `run`, `-n`/`--name` specifies the name of the scenario that will be loaded. If `-n`/`--name` isn't specified, the default parameters will be loaded instead. 
    * If `command` is set to `save`, `-n`/`--name` specifies the name that the previously run scenario will be saved to. If `-n`/`--name` isn't specified, the scenario will be saved with a default name. 
    * Specifying the `-n`/`--name` argument doesn't have any behaviour with the `list` command. 
  * The range (`-r`/`--range`) and parameter override (`-p`/`--param`) arguments use the exact location of the parameters in the [parameter dictionary](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/cpr_simulation/parameters.py). So, for instance, if you want to target the metabolism parameter of the proself agent distribution, use `agent_distributions:proself:metabolism=[value]`.
  * For the range argument `--range location=from,to,incr`, the argument `from` is inclusive whereas `to` is exclusive. The ranges work with integers as well as with floats. 
  * Verbose mode and real-time plotting mode are on by default if no range or batch argument is specified. If one or more such argument is specified, both modes are off by default. These values can be overridden by the `-v`/`--verbose` and the `-P`/`--plot` arguments respectively. 
  * The `save` command currently doesn't support scenarios with `-b`/`--batch`, `-p`/`--param` or `-r`/`--range` arguments specified. This will be implemented for the final model. 

## Goals for the Final Model
Below are listed some features that aren't implemented right now, but that we aim to have implemented for the final model. 
* Right now, the energy function (the function that decides how much resource the agent will take for himself this epoch) is to a high degree discrete. In fact, at this moment we have implemented two functions: A base function (that was used in the report) and a restricted version that provides more complex information (For more information on that function, read its docstring in [`agent.py`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/cpr_simulation/agent.py)). We want to make this function more continuous, and make it so that multiple kinds of (contradicting) behaviours can be active at once. We are working on a way to implement this, and its proposal can be found 
[here](https://htmlpreview.github.io/?https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/agentfunc_prop.html). 
* In light of the model above, we also want to implement more kinds of realistic behaviours. 
* We want to incorporate a simple form of mutation and evolution in our procreate function. 