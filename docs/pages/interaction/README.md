---
layout: page
title: Interaction with the Model
---

1. toc
{:toc title="Contents"}

# The Command-Line Interface
```
usage: sim.py [-h] [-b amount] [-r item [item ...]] [-p item [item ...]]
              [-n scenario] [-o file_path] [-P [bool]] [-f [bool]]
              [-v [0, 1 or 2]] [--jobs n_jobs]
              {run,save,list,test}
```

## Required argument
The only required argument is a positional argument. Options can be taken from ```{run, save, list, test}```. 

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

## Specifying a certain scenario
```
 -n    [name_of_scenario]
--name [name_of_scenario] 
```
With the ```name``` argument, it's possible to specify a certain scenario name.
* If the program is operating in ```run```-mode, the ```name``` argument can be used to spedify the name of a scenario to load.
* If the program is operating in ```save```-mode, the ```name``` argument can be used to specify the name of the to be saved scenario. 
* If the program is operating in ```list```-mode, the ```name``` argument is ignored. 

## Altering simulation parameters