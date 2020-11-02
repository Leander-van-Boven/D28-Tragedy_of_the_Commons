---
layout: page
title: Model Output
---

1. toc
{:toc title="Contents"}

# Verbosity
The most basic form of output, in the command-line itself.
The type of verbosity can be specified using the `--verbose [mode]`  or `-v` command-line argument together with the `run` command. Three different modes of verbosity are available:

## Minimal Mode (`--verbose 0`)
This will only print out the number of the currently running experiment, together with the total amount of experiments to run. This verbose option is used when a batch experiments are run, or when a range of experiments over some parameter values is run.

# Real-time Plot


# CSV-logger
The CSV logger logs the statistics of the simulation into a CSV- or [comma-separated values file](https://en.wikipedia.org/wiki/Comma-separated_values). This file can then be used for further data processing. Its usage becomes most optimal if combined with the [--range](/pages/interaction/#batch-and-range) command-line argument. 


## Logged values
The contents in each row of the logger are split into two parts.
* The parameters of the experiment; and
* The statistics of the simulation at a certain epoch.

The former will change per experiment, the latter per call of the `add_row` function.

### Experiment Values