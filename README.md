# Tragedy of the Commons Repository
### DMAS project, group D28 

Welcome to the repository of a model modeling a community of agents living in a common resource environment. 
> This README only elaborates on the general file structure of this repository, and provides some quick start directives. For the documentation of the actual simulation model, please refer to the [Official Documentation](https://leander-van-boven.github.io/D28-Tragedy_of_the_Commons/).

# Overview
```
D28-Tragedy_of_the_Commons
├───commands
├───cpr_simulation
├───data_analysis
│   ├───final_results
│   │   └───final_csv
│   │       └───trimodal
│   └───habitable_zone
│       └───CSV
│           └───top5_batch
├───docs
│   ├───assets
│   │   ├───icons
│   │   └───img
│   ├───pages
│   │   ├───architecture
│   │   ├───background
│   │   ├───interaction
│   │   ├───output
│   │   └───parameters
│   └───_data
├───meta_plots
│   ├───csv
│   ├───plots
│   └───plotting_files
└───scenarios
    ├───resourcef_exp
    ├───resourcef_log
    ├───resourcef_nroot
    └───semi_stable
```

The repository is separated into multiple parts:
* The Python module for running the simulation called `cpr_simulation`. All files concerning this module are contained in the equally named folder. The file running importing and running this module is called `sim.py` and is found in the root directory of the repository.
* Scenarios for the simulation. These are contained in subfolders (named by the scenario name) in the `scenarios` folder. Refer to the [documentation](https://leander-van-boven.github.io/D28-Tragedy_of_the_Commons/pages/interaction/#specifying-a-certain-scenario) on how to run the various scenarios.
* Data Analysis. Contained in the `data_analysis` folder, there are two subfolders used for data analysis. 
  * The `data_analysis/habtiable_zone/` subdirectory contains the data analysis of the 270 000 experiments run to find the habtiable zone for the model, using various `R` scripts.
  * The `data_analysis/final_results/` subdirectory contains the data analysis of the final experiments, also using `R`. Refer to the report for the method of these final experiments.
* The `meta_plots` folder consists of a lot of processed CSV files and many plots thereof, placed in the `csv` and `plots` subfolders respectively. The `plotting_files` subdirectory contains the Python files used to create these plots.
* Last, but certainly not least, the `docs` folder. This folder contains all the pages for the [documentation](https://leander-van-boven.github.io/D28-Tragedy_of_the_Commons/). (this folder also contains all rendered pages in the `_site` subfolder, however this folder can be safely ignored)

## Quick Start
### Prerequisites
* The simulation assumes Python 3.6+, and requires the modules `numpy`, `argparse`, `matplotlib` and`joblib` to be installed.
  ```bash
  pip3 install numpy argparse matplotlib joblib
  ``` 
* Download the code by cloning this repository.
  ```bash
  git clone "https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons"
  ```

### Quick Run
Since all parameters have a preset default value, the model can be started without changing any settings. The most basic command to use is therefore (this assumes that this command is run from the base folder of the repository):

```bash
nemo@p-sea:~/D28-Tragedy_of_the_Commons$ python3 sim.py run
```

Refer to the [Interaction](https://leander-van-boven.github.io/D28-Tragedy_of_the_Commons/pages/interaction) page in our [documentation](https://leander-van-boven.github.io/D28-Tragedy_of_the_Commons/) for more information about the command-line interface.


