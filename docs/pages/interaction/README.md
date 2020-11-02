---
layout: page
title: Model Interaction
---

1. toc
{:toc title="Contents"}

# The Command-Line Interface
Interaction with the model is done through the file `sim.py` that's located in the root directory. At any time, a discription of the CLI can be found by using ```python sim.py --help```.
```
nemo@p-sea:~/D28-Tragedy_of_the_Commons$ python sim.py --help
```
```
usage: sim.py [-h] [-n scenario] [-p item [item ...]] [-b int]
              [-r item [item ...]] [-o path] [-P [bool]] [-v [int]]
              [-f [bool]] [--jobs int]
              {run,save,list}

positional arguments:
  {run,save,list}  run: run a simulation; save: save the previous
                        simulation; list: list all saved simulations

optional arguments:
  -h, --help            show this help message and exit
  -n scenario, --name scenario
                        the name of the scenario to load or to save
  -p item [item ...], --param item [item ...]
                        add parameters to override its value, e.g.
                        resource:start_amount=600
  -b int, --batch int   the amount of times the same experiment should be run
                        (defaults to 1)
  -r item [item ...], --range item [item ...]
                        add parameters to run the simulation with a range of
                        values, e.g. resource:start_amount=300,601,100
  -o path, --out path   the output path for CSV logging
  -P [bool], --plot [bool]
                        whether to show a real-time plot
  -v [int], --verbose [int]
                        whether to enter verbose mode [0..2]
  -f [bool], --fullscreen [bool]
                        whether to show the plot in fullscreen
  --jobs int            the amount of parallel processes in range or batch
                        mode
```

## Required Argument
The only required argument is a positional argument. Options can be taken from ```{run, save, list}```. 

* Specifying ```run``` will run a simulation with default parameters, real-time plotting and book-keeping in the CLI.
  ```bash
  python3 sim.py run
  ```
* Specifying ```save``` will save the parameters of the previously ran experiment as a scenario. The scenario will be saved with a default name.
  ```
  python3 sim.py save
  ```
* Specifying ```list``` will list the names of all saved scenarios. 
  ```
  python3 sim.py list
  ```

## Specifying a Certain Scenario
```
 -n    [name_of_scenario]
--name [name_of_scenario] 
```
With the `name` argument, it's possible to specify a certain scenario name.
* If the program is operating in `run`-mode, the `name` argument can be used to spedify the name of a scenario to load.
* If the program is operating in `save`-mode, the `name` argument can be used to specify the name of the to be saved scenario. 
* If the program is operating in `list`-mode, the `name` argument is ignored. 

## Altering Simulation Parameters
>For an overview of all parameters available in this simulation, refer to [Parameters](/pages/parameters/). 

```
 -p       [parameter_address]=[value]
--params  [parameter_address]=[value]
```
With the `param` argument, it's possible to override the default values of different parameters. The parameter address `[parameter_address]` follows the parameter syntax found in [Parameters](/pages/parameters). The new parameter value `[value]` can be an integer, a float or a string. It is possible to override multiple paramers at once. Note that the `param` argument is only used in `run`-mode. 

### Examples
* Change the initial agent count from 100 (default) to 10:
  ```
  $ python sim.py run --param agent:count=10
  ```
* Change the resource growth function[^1] from `logarithmic` (default) to `nroot`:
  ```
  $ python sim.py run --param resource:growth_function=nroot
  ```
* Change both the initial agent count and the resource growth function:
  ```
  $ python sim.py run --param agent:count=10 resource:growth_function=nroot
  ```
* Change the initial agents' SVO distribution to a bimodal normal distribution with $$\mu_1=0.2$$, $$\sigma_1=0.125$$, $$\mu_2=0.95$$, and $$\sigma_2=0.01$$:
  ```
  $ python sim.py run --param \
      svo_dist:d1:m=0.2 \
      svo_dist:d1:s=0.125 \
      svo_dist:d2:m=0.95 \
      svo_dist:d2:s=0.01
  ```

[^1]: For more information about the characteristics of the different resource growth functions, refer to [Resource](/pages/architecture/resource/).