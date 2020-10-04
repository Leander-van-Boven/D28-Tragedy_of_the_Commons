# Tragedy of the Commons Repository
### DMAS project, group D28

A tragedy about a planet with a single island in a sea of fish run by a bunch of self-ish and self-less agents.

## Structure of this repository
> All files are still under development and are heavily subdue of changes.

* The folders named to each group member contains some personal files or found literature.

* The `_Code` folder contains the simulation code and interface:
  - [`name_of_beautiful_project`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/tree/master/_Code/name_of_beautiful_project) is the module that contains the simulation code. 
  - [`scenarios`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/tree/master/_Code/scenarios) contains different scenarios that can be ran on the simulation that we found interesting. 
  - [`figures`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/tree/master/_Code/figures) contains interesting figures.
  - [`sim.py`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/sim.py) implements a command-line interface for the `name_of_beautiful_project` module.

* Structure of the `_Code/name_of_beautiful_project` folder:
  - [`agent.py`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/name_of_beautiful_project/agent.py) contains the `Agent` class. This class represents the agents of our model and contains their properties. 
  - [`attributes.py`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/name_of_beautiful_project/attributes.py) (_can be ignored_) consists of a few temporary lists that were used for initial model design. 
  - [`main.py`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/name_of_beautiful_project/main.py) is the file that is used to run the model. This file will parse command line arguments, initialize the simulation and graphing and run the model.
  - [`output.py`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/name_of_beautiful_project/output.py) will be used to plot the results from the model after and during the simulation.
  - [`resource.py`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/name_of_beautiful_project/resource.py) contains the `Resource` class. This class represents the common resource (fish) of our model. Includes all properties and methods that change these properties unique to this class.
  - [`simulation.py`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/name_of_beautiful_project/simulation.py) contains the `Simulation` class. This class runs the simulation. It manages changes to the common resource and the changes to the agents as a result of the changes in the resource, and vice-versa.
  - [`test.py`](https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons/blob/master/_Code/name_of_beautiful_project/test.py) (_can be ignored_) used to try out pieces of code.



## How to run the simulation
### Prerequisites
* The simulation assumes Python 3.6+, and requires the modules `numpy`, `argparse`, and `matplotlib` to be installed.
  ```
  pip3 install numpy matplotlib argparse
  ``` 
* Download the code by cloning this repository.
  ```
  git clone https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons
  ```
### Usage
After downloading the repository, open `./_Code/` in your favourite terminal. Simulations can be ran, saved and loaded through `sim.py`. 

* To run a simulation with default parameters, use: 
  ```
  python3 sim.py run
  ```

* To load and run a specific scenario, use:
  ```
  python3 sim.py run -n [name of scenario]
  ```

* To save the previously ran simulation as a scenario, use:
  ```
  python3 sim.py save -n [name of scenario]
  ```

* To list all available scenarios, use:
  ```
  python3 sim.py list
  ```

* For a full breakdown of availiable functions and flags, use:
  ```
  python3 sim.py --help
  ```

* It's also possible to import `name_of_beautiful_project` as a module in a custom python script for more fine-grained control over the simulation.