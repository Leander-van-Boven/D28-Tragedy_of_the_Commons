---
layout: page
title: Model Interaction
---

1. toc
{:toc title="Contents"}

# The Command-Line Interface
Interaction with the model is done through the file `sim.py` that's located in the root directory. At any time, a discription of the CLI can be found by using ```python sim.py --help```.
```shell
nemo@p-sea$ python sim.py --help
```
```
usage: sim.py [-h] [-n scenario] [-p item [item ...]] [-b int]
              [-r item [item ...]] [-j int] [-o path] [-P [bool]]
              [-v [int]] [-f [bool]]
              {run,save,list}

positional arguments:
  {run,save,list}       run: run a simulation; save: save the previous
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
  -j int, --jobs int    the amount of parallel processes in range or batch
                        mode
  -o path, --out path   the output path for CSV logging
  -P [bool], --plot [bool]
                        whether to show a real-time plot
  -v [int], --verbose [int]
                        whether to enter verbose mode [0..2]
  -f [bool], --fullscreen [bool]
                        whether to show the plot in fullscreen
```

## Required argument
The only required argument is a positional argument. Possible options are `run`, `save` and `list`. 

* Specifying ```run``` will run a simulation with default parameters, real-time plotting and book-keeping in the CLI.
  ```shell
  $ py sim.py run
  ```
* Specifying ```save``` will save the parameters of the previously ran experiment as a scenario. The scenario will be saved with a default name.
  ```shell
  $ py sim.py save
  ```
* Specifying ```list``` will list the names of all saved scenarios. 
  ```shell
  $ py sim.py list
  ```

## Specifying a certain scenario
```
 -n    [name_of_scenario]
--name [name_of_scenario] 
```
With the `name` argument, it's possible to specify a certain scenario name.
* If the program is operating in `run`-mode, the `name` argument can be used to spedify the name of a scenario to load.
* If the program is operating in `save`-mode, the `name` argument can be used to specify the name of the to be saved scenario. 
* If the program is operating in `list`-mode, the `name` argument is ignored. 

### Examples
* Load a scenario called `stable_system`, and run this simulation:
  ```shell
  $ py sim.py run --name stable_system
  ``` 
* Save the previously ran simulation as a scenario named `interesting_results`
  ```shell
  $ py sim.py save --name interesting_results
  ```
It isn't possible to overwrite already saved scenarios. Scenarios can be manually deleted by deleting a the scenario directory in `./scenarios/`.
{:.note}

## Altering simulation parameters
```
 -p       [parameter_address]=[value]
--params  [parameter_address]=[value]
```
With the `param` argument, it's possible to override the default values of different parameters. The parameter address `[parameter_address]` follows the parameter syntax found in [Parameters](/D28-Tragedy_of_the_Commons/pages/parameters). The new parameter value `[value]` can be an integer, a float or a string. It is possible to override multiple paramers at once. Note that the `param` argument is only used in `run`-mode. 

### Examples
For an overview of all parameters available in this model, refer to [Parameters](/D28-Tragedy_of_the_Commons/pages/parameters/). 
{:.note}

* Change the initial agent count from 100 (default) to 10:
  ```shell
  $ py sim.py run --param agent:count=10
  ```
* Change the resource growth function[^1] from `logarithmic` (default) to `nroot`:
  ```shell
  $ py sim.py run --param resource:growth_function=nroot
  ```
* Change both the initial agent count and the resource growth function:
  ```shell
  $ py sim.py run --param agent:count=10 resource:growth_function=nroot
  ```
* Change the initial agents' SVO distribution to a bimodal normal distribution with $$\mu_1=0.2$$, $$\sigma_1=0.125$$, $$\mu_2=0.95$$, and $$\sigma_2=0.01$$:
  ```shell
  $ py sim.py run --param \
  >   svo_dist:d1:m=0.2 \
  >   svo_dist:d1:s=0.125 \
  >   svo_dist:d2:m=0.95 \
  >   svo_dist:d2:s=0.01
  ```

## Specifying output behaviour
```
 -o   [path]
--out [path]
```
```
 -v       [?mode]
--verbose [?mode]
```
This model has multiple ways of showing the condition of the simulation each epoch. Real-time plotting is used to make a simulation more insightful to the human eye, however when running a lot of experiments or closely monitoring the behaviour of each agent, these plots might not be sufficient. This is where the CSV logging and verbosity modes come into play. 

### Output path for CSV logging
The `out` argument can be used to specify the output path for the CSV file. Note that CSV logging will only be enabled when this argument is specified (unless running a [batch or range](#batch-and-range) of experiments). It is possible to specify either a relative path (relative to 'sim.py') or an absolute path.

For example, to enable CSV logging and have the CSV output path be `results/out.csv`, use:
```shell
$ py sim.py run --out results/out.csv
```

### Verbosity
The `verbose` argument specifies the level of verbosity of the model. Three modes are available:

|Mode| Description |
|:-:|-|
|0| Only experiment counter, no epoch status |
|1| Experiment counter and status per epoch |
|2| Detailed overview of all agents and their behaviour each epoch. Halts after each epoch to allow for the digestion of all information |

For examples of the exact output of the different verbosity modes, refer to [Output](../output/#verbosity). So for example, to use verbosity mode 1, use:
```shell
$ py sim.py run --verbose 1 
```

## Running multiple experiments at once
```
 -b     [amount]
--batch [amount]
```
```
 -r     [parameter_address]=[from],[to],[increment]
--range [parameter_address]=[from],[to],[increment]
```
```
 -j    [number_of_jobs]
--jobs [number_of_jobs]
```
### Batch and range
With the `batch` argument, it's possible to specify the mount of times a single experiment should be run. As our model is highly stochastic, this functionality can be used to determine more accurately the impact that a certain parameter has on system outcomes. 

With the `range` argument, it's possible to specify a range of values that a specific parameter will iterate over. The list of values is obtained by repeatedly adding `[increment]` to the value of `[from]` (inclusive), until the value of `[to]` (exclusive) is reached. For example, if `0,5,1` is given, the resulting set of values will be $$\{0,1,2,3,4\}$$. It is possible to specify ranges for multiple parameters at once. 

When using a range and/or batch, CSV logging is enabled by default. If the `out` argument isn't specified, it will default to `./out.csv`. 
{:.note}

### Total amount of experiments
Suppose $$P$$ is the set of all parameters that are specified through the `range` argument. Say that, for each specified parameter $$p\in P$$, the set of values that $$p$$ will range over is called $$V_p$$. Finally, suppose that the batch amount is set as $$b$$. The total amount of experiments is then equal to $$b\cdot\prod_{p\in P}V_p$$. 

Keep in mind that the total number of experiments can increase very fast!
{:.note title="Important"}

### Multi-threading 
If the total amount of experiments is very high, depending on your CPU, it might be beneficial to enable multi-threading mode. This is done through the `jobs` argument. This argument specifies the amount of threads that will be used in parallel. The default value of `jobs` is 1, i.e. the model runs in single-threaded mode by default. To enable multi-threading mode, set the `jobs` argument to a value higher than 1. 

In multi-threading mode, each experiment will be saved to a separate file due to memory concerns and multi-threaded file access limitations. This means that the `out` argument should contain the path to a directory instead of a file. If the `out` argument isn't specified and the simulation runs multi-threaded, it will default to the directory `./out/`. 
{:.note}

### Examples
For an overview of all parameters available in this model, refer to [Parameters](/D28-Tragedy_of_the_Commons/pages/parameters/). 
{:.note}

* Run the default experiment 10 times:
  ```shell
  $ py sim.py run --batch 10
  ``` 
* Range over the agents' consumption factor with values ranging from 1 to and including 5:
  ```shell
  $ py sim.py run --range agent:consumption_factor=1,6,1
  ``` 
* Run the same experiment as above but repeat it 5 times, and save it to `nice_experiment.csv`:
  ```shell
  $ py sim.py run \
  >   --range agent:consumption_factor=1,6,1 \
  >   --out nice_experiment.csv \
  >   --batch 5 
  ``` 
  This results in a total of 25 experiments. 
* Use a bimodal starting SVO distribution where both standard deviations are equal and fixed. We range over both means, where $$\mu_1$$ explores `[0..0.5]` in three steps and $$\mu_2$$ explores `[0.5..1]` in three steps. We also repeat each experiment 12 times. Save to `quite_large.csv`.
  ```shell
  $ py sim.py run \
  >   --param \
  >       svo_dist:d1:m=0 \
  >       svo_dist:d1:s=0.125 \
  >       svo_dist:d2:m=0 \
  >       svo_dist:d2:s=0.125 \
  >   --range \
  >       svo_dist:d1:m=0,0.5,0.17 \
  >       svo_dist:d2:m=0.5,1,0.16 \
  >   --out quite_large.csv \
  >   --batch 12
  ```
  We first use `--param` to create the parameter entries for both means and standard deviations. This is because `svo_dist` is empty by default. Therefore, we first have to generate both modes of the multi-modal distribution before we can range over any of them. For more information about the `svo_dist` parameter, refer to [Parameters](../parameters/).
  {:.note}
  
  This results in a total of 108 experiments.

* Now we also want to range over both standard deviations. This results in quite a high number of        experiments, so we use multi-threading to speed up the process.
  ```shell
  $ py sim.py run \
  >   --param \
  >       svo_dist:d1:m=0 \
  >       svo_dist:d1:s=0.125 \
  >       svo_dist:d2:m=0 \
  >       svo_dist:d2:s=0.125 \
  >   --range \
  >       svo_dist:d1:m=0,0.5,0.17 \
  >       svo_dist:d1:s=0.01,0.32,0.1 \
  >       svo_dist:d2:m=0.5,1,0.16 \
  >       svo_dist:d2:s=0.01,0.32,0.1 \
  >   --out very_big \
  >   --batch 12 \
  >   --jobs 8 
  ```
  Note that we specify a directory for the `out` argument, instead of a file. 
  {:.note}

  This results in a total of 1728 experiments, divided over 8 parallel threads. 

## Specifying real-time plotting behaviour
```
 -P     [?boolean]
--plot  [?boolean]
```
```
 -f
--fullscreen
```
```
--resize
```
By default, the real-time plotting window will pop up in a small window. Also, depending on the mode of the simulation, real-time plotting might be enabled or disabled by default. 

The `plot` argument can be used to override whether to enable the real-time plotting functionality.
* To forcefully enable the real-time plotting:
  ```shell
  $ py sim.py run --plot true
  ```
* To forcefully disable the real-time plotting:
  ```shell
  $ py sim.py run --plot false
  ```

The `fullscreen` argument can be used to make the real-time plotting window show up in full screen. To enable this, simply add the `--fullscreen` or `-f` argument. 

The `resize` argument can be used in a similar way as the `fullscreen` argument. Specifying this argument will cause the plot to start in a different mode allowing the plot to be resized without it resetting the current plot. 

Setting this option however will cause a significant base slow-down of the plot, and cause the plot to become gradually slower over the epochs too!
{:.note title="Important"}

## Default Values of Arguments
If left unspecified, some arguments have different defaults based on the current running mode. This is mainly influenced by whether the model is running a batch or range of experiments, and whether this is done in a multi-threaded environment. In the table below, 

|`batch` or `range`|`jobs`||`plot`|`verbose`|`out`|
|no|1||yes|1|none|
|yes|1||no|0|'`out.csv`'|
|yes|>1||ignored|ignored|'`./out/`'|

Default values of `plot`, `verbose` and `out` arguments depending on values of `batch`/`range` and `jobs` arguments.
{:.figcaption}

Note that both the `verbose` and `plot` arguments are _ignored_ if the model is running in multi-threaded mode. This means that, even when you override the `verbose` or `plot` arguments, it will not matter. This is because the multi-threading has a custom output, and showing multiple plotting windows is not feasible in a multi-threaded environment. 
{:.note}

[^1]: For more information about the characteristics of the different resource growth functions, refer to [Resource](../architecture/resource/).