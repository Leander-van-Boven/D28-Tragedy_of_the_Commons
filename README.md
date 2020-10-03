# Tragedy of the Commons Repository
### DMAS project, group D28

A tragedy about a planet with a single island in a sea of fish run by a bunch of self-ish and self-less agents.

## Structure of this repository
> All files are still under development and are heavily subdue of changes.

* The folders named to each group member contains some personal files or found literature.

* The \_Code folder contains the code for the model:
  - [`name_of_beautiful_project`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/tree/master/_Code/name_of_beautiful_project) is the module that contains the simulation code. 
  - [`scenarios`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/tree/master/_Code/scenarios) contains different scenarios that can be ran on the simulation that we found interesting. 
  - [`figures`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/tree/master/_Code/figures) contains interesting figures.
  - [`sim.py`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/sim.py) implements a command-line interface for the `name_of_beautiful_project` module.

* Structure of the `name_of_beautiful_project` module:
  - [`agent.py`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/name_of_beautiful_project/agent.py) contains the `Agent` class. This class represents the agents of our model and contains their properties. 
  - [`attributes.py`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/name_of_beautiful_project/attributes.py) (_can be ignored_) consists of a few temporary lists that were used for initial model design. 
  - [`main.py`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/name_of_beautiful_project/main.py) is the file that is used to run the model. This file will parse command line arguments, initialize the simulation and graphing and run the model.
  - [`output.py`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/name_of_beautiful_project/output.py) will be used to plot the results from the model after and during the simulation.
  - [`resource.py`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/name_of_beautiful_project/resource.py) contains the `Resource` class. This class represents the common resource (fish) of our model. Includes all properties and methods that change these properties unique to this class.
  - [`simulation.py`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/name_of_beautiful_project/simulation.py) contains the `Simulation` class. This class runs the simulation. It manages changes to the common resource and the changes to the agents as a result of the changes in the resource, and vice-versa.
  - [`test.py`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/name_of_beautiful_project/test.py) (_can be ignored_) used to try out pieces of code.

## How to run the simulation
After downloading the repository, open `.\\\_Code` in your favourite terminal. 


