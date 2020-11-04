---
layout: page
title: Introduction
cover: true
---

Welcome to the documentation of a model modeling a community of agents living in a common resource environment. 

1. toc
{:toc title="Contents"}

## Overview
The documentation is separated into multiple parts:

* [Model Background](/D28-Tragedy_of_the_Commons/pages/background/){:.heading.flip-title} --- Describes the concept and literature of the model in a broader context.
* [Model Architecture](/D28-Tragedy_of_the_Commons/pages/architecture){:.heading.flip-title} --- Shows the different (code) parts of the model and how they are connected.
* [Model Interaction](/D28-Tragedy_of_the_Commons/pages/interaction){:.heading.flip-title} --- Explains how to interact with the model.
* [Model Parameters](/D28-Tragedy_of_the_Commons/pages/parameters){:.heading.flip-title} --- Shows a listing of all parameters of the model per submodule.
* [Model Output](/D28-Tragedy_of_the_Commons/pages/output){:.heading.flip-title} --- Gives an overview and explanation of the inner workings of all submodules producing about.

## Quick Start
### Prerequisites
* The simulation assumes Python 3.6+, and requires the modules `numpy`, `argparse`, and `matplotlib` to be installed.
  ```bash
  pip3 install numpy argparse matplotlib
  ``` 
* Download the code by cloning this repository.
  ```bash
  git clone "https://github.com/Leander-van-Boven/D28-Tragedy_of_the_Commons"
  ```

### Quick Run
Since all parameters have a preset default value, the model can be started without changing any settings. The most basic command to use is therefore:
```bash
python3 sim.py run
```
This assumes that this command is run from the base folder of the repository.
{:.figcaption}

### Important Command-line Arguments
To change a the parameter of the model the `--param [parameter]=[value]` or `-p [parameter]=[value]` argument can be used 

> Refer to [Parameters](/D28-Tragedy_of_the_Commons/pages/parameters) for a listing of all parameters per submodule

### Interesting Scenarios to run
NEEDS CONTENT

<clap-button></clap-button>