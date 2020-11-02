# List of todo's for implementation model
## Implementation
* ~~Show how to cross an item off the todo list~~
  * Use ALT+S to strikethrough selection
### CPR simulation
* Fix save scenario functionality
* Go through CLI help page ordering & texts
* Implement make new folder in multi-threaded logging mode where output folder specified doesn't exist yet (and isn't a file)
* Remove redundant blocks of code
  * ```__init__.py```
  * ```agent.py```
    * Make ```act_restricted``` not be a local method? AFAIK it's only called once anyways
  * ```logger.py```
  * ```main.py```
  * ```output.py```
  * ```parameters.py```
  * ```resource.py```
  * ```simulation.py```
  * ```util.py```
* Check and fix any and all docstrings
  * ```__init__.py```
  * ```agent.py```
  * ```logger.py```
  * ```main.py```
  * ```output.py```
  * ```parameters.py```
  * ```resource.py```
  * ```simulation.py```
  * ```util.py```
* Final check PEP8-compliance
  * ```__init__.py```
  * ```agent.py```
  * ```logger.py```
  * ```main.py```
  * ```output.py```
  * ```parameters.py```
  * ```resource.py```
  * ```simulation.py```
  * ```util.py```

### General repository
* Change README (decide on what we want to have there)
* <3
* Cleanup of repository (file structure)
  * Remove redundant files/folders
  * Maybe put CSV files of experiments in separate repository? We can then put that repository in our main repository but it will only be cloned if ```git clone --recursive``` is used. 
* Check whether docs/FILES/file_structure.md is still up-to-date
## Documentation
* Background pages
  * 'Imagine a small island with no food but fish in the sea around it. Any agent living on that island...'
* Architecture pages
  * Home page
    * Explanation general framework
    * TOC
  * Agent class
  * Resource class
  * Simulation class
  * Helper classes?
* Interaction pages
  * Overview of workflow of implementation
  * Thorough explanation of every CL argument
  * Explanation and use-case of all 'modes' we thought of
    * Regular mode
      * Single experiment
      * Real-time plots
      * Verbosity 1
    * Close-up mode
      * Single experiment 
      * No real-time plots
      * Verbosity 2
    * Small sweep
      * Small number of experiments (```range``` and/or ```batch```)
      * No real-time plots
      * Verbosity 0
      * Single-threaded
      * Logging to single CSV file
    * Large sweep
      * Big number of experiments (```range``` and/or ```batch```)
      * No real-time plots
      * Verbosity 0
      * Multi-threaded (```jobs``` > 1)
      * Logging to multiple CSV files
  * Lots of example commands (w/ pictures?)
* Output pages
  * Explanation of real-time plots
  * Explanation of different verbosity modes and their uses
  * Explanation of CSV logging functionality
* Parameters pages
  * Parameters home page
  * Simulation parameters
  * Agent parameters
  * Resource parameters
  * SVO distribution parameters
  * For every parameter, its syntax for calling it with  ```--range/--param``` argument
* Data analysis page? Or in README? Should we mention it?
## Report
* Read through section Implementation Model, add/fix things where needed
* (Put things needed to fix below)