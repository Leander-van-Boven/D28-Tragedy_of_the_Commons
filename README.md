# Tragedy of the Commons Repository
### DMAS project, group D28

A tragedy about a planet with a single island in a sea of fish run by a bunch of self-ish and self-less agents.


## Structure of this repository
> All files are still under development and are heavily subdue of changes.

* The folders named to each group member contains some personal files or found literature.

* The \_Code folder contains the code for the model:
  - [`agent.py`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/agent.py) contains the `Agent` class. This class represents the agents of our model and contains their properties. 
  - [`attributes.py`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/attributes.py) (_can be ignored_) consists of a few temporary lists that were used for initial model design. 
  - [`main.py`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/main.py) is the file that is used to run the model. This file will parse command line arguments, initialize the simulation and graphing and run the model.
  - [`output.py`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/output.py) will be used to plot the results from the model after and during the simulation.
  - [`parameters.py`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/parameters.py) consists of multiple dictionaries. Each dictionary contains the default parameters for each class in the model.
  - [`resource.py`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/resource.py) contains the `Resource` class. This class represents the common resource (fish) of our model. Includes all properties and methods that change these properties unique to this class.
  - [`simulation.py`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/simulation.py) contains the `Simulation` class. This class runs the simulation. It manages changes to the common resource and the changes to the agents as a result of the changes in the resource, and vice-versa.
  - [`test.py`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/test.py) (_can be ignored_) used to try out pieces of code.
