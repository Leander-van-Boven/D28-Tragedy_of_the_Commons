# List of todo's for implementation model
## Implementation
* ~~Show how to cross an item off the todo list~~
  * Use ALT+S to strikethrough selection
### CPR simulation
* ~~Fix save scenario functionality~~
* ~~Go through CLI help page ordering & texts~~
* ~~Implement make new folder in multi-threaded logging mode where output folder specified doesn't exist yet (and isn't a file)~~
* ~~Add custom Exceptions to catch in sim.py~~
* ~~Fix staticity of attributes (static if needed, else not)~~
* ~~Add parameter for old SVO procreation function?~~
* Remove redundant blocks of code (getters/setters)
  * ~~```__init__.py```~~
  * ~~```agent.py```~~
    * ~~Make ```act_restricted``` not be a local method? AFAIK it's only called once anyways~~
    * ~~Local procreate method functions in procreate class method (choosable via parameter in def procreate)~~
  * ~~```logger.py```~~
  * ~~```main.py```~~
  * ```output.py```
  * ~~```parameters.py```~~
  * ~~```resource.py```~~
  * ~~```simulation.py```~~
  * ~~```util.py```~~
* ~~Check and fix any and all docstrings~~
  * ~~```__init__.py```~~
  * ~~```agent.py```~~
  * ~~```logger.py```~~
  * ~~```main.py```~~
  * ```output.py```
  * ~~```parameters.py```~~
  * ~~```resource.py```~~
  * ~~```simulation.py```~~
  * ~~```util.py```~~
* ~~Final check PEP8-compliance~~
  * ~~```__init__.py```~~
  * ~~```agent.py```~~
  * ~~```logger.py```~~
  * ~~```main.py```~~
  * ```output.py```
  * ~~```parameters.py```~~
  * ~~```resource.py```~~
  * ~~```simulation.py```~~
  * ~~```util.py```~~
* ~~Solve fig.savefig() problem~~
  * ~~create new plot with data and save this figure instead.~~
* ~~Add more maximized function supports~~
* Add some nice scenarios
* ~~Check whether all code is compliant to beta implementation feedback~~
* ~~For each class, link to documentation in docstring~~
* ~~Decide what to do with ```parameters.py``` docstring~~
* Determine behaviour of agent count is set to 0. Should iterate without agent limit.

### General repository
* Change README (decide on what we want to have there)
  * Explain file structure
  * link to documentation
  * quick start?
* <3
* Cleanup of repository (file structure)
  * Remove redundant files/folders
  * Maybe put CSV files of experiments in separate repository? We can then put that repository in our main repository but it will only be cloned if ```git clone --recursive``` is used. 
## Documentation
* General
  * ~~Nicify logo picture~~
  * Finalize layout
  * Add scenario that is actually included in the --name example
* Introduction
  * Interesting scenarios to run
* ~~Background pages~~
  * ~~'Imagine a small island with no food but fish in the sea around it. Any agent living on that island...'~~
  * ~~TOC vs CPR~~
* ~~Architecture pages~~
  * ~~Intro~~
    * ~~Explanation general framework~~
  * ~~Agent class~~
    * ~~Multi modal gauss~~
    * ~~Procreate~~
    * ~~Behaviour~~
  * ~~Resource class~~
  * ~~Simulation class~~
    * ~~Add pseudo code~~
  * ~~Output classes~~
    * ~~Mention list of strings instead of pandas frame for output~~
  * ~~Helper classes?~~
* ~~Interaction pages~~
  * ~~Overview of workflow of implementation~~
  * ~~Thorough explanation of every CL argument~~
  * ~~Lots of example commands (w/ pictures?)~~
* ~~Output pages~~
  * ~~Explanation of real-time plots~~
  * ~~Explanation of different verbosity modes and their uses~~
  * ~~Explanation of CSV logging functionality~~
  * ~~Add links~~
    * ~~from #epoch-statistics to location where limit and unlimit factor are calculated~~
* ~~Parameters pages~~
  * ~~first headername "General" or "General Structure", or...?~~
  * ~~Simulation parameters~~
  * ~~Agent parameters~~
  * ~~Resource parameters~~
    * ~~Add description to resource growth function parameters~~
  * ~~SVO distribution parameters~~
* Check and Fix all links
  * Add additional /#header-title thingies if feasible
* ~~Fix section header capitalization~~
* Data analysis page? Or in README? Should we mention it?
* ~~Put GNU-GPL license in the /docs folder somewhere~~
* ~~Make links in Interaction/Agent somewhat more specific (subsection in parameter)~~
* Add default off parameter to save the figure after simulation
## Report
* Read through section Implementation Model, add/fix things where needed
* (Put things needed to fix below)

## Later
* Default values in parameter listing docs