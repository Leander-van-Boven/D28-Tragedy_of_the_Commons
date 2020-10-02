"""This module is the connection between the user and the simulation.

It parses the commandline arguments and starts the simulation accordingly.
The possible commandline arguments can be requested and reviewed by
running: 
>>> python3 sim.py -h
"""

#TODO maybe find a more suitable name to nobp
import name_of_beautiful_project as nobp
import argparse
import json
import os

__author__ = "Leander van Boven\\ Aurelien Adraenssen\\ " + \
             "Jesper Kuiper\\ Ryan O'Loughlin"

if __name__ == "__main__":
    # Define possible arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'command', choices=['run', 'save'], 
        help="Whether to run a new simulation, or to save the previous one")
    parser.add_argument(
        '-d', '--indir', required=False,
        help="The scenario load or save directory.")
    parser.add_argument(
        '-o', '--outdir', required=False,
        help="If desired, the output directory for logging")
    parser.add_argument(
        '--noplot', required=False, action="store_true",
        help="Add flag to disable real-time plotting")
    parser.add_argument(
        '-s', '--scenario', required=False, choices=[0, 1, 2],
        help="Which scenario to run")

    # Parse the inputted arguments
    args = parser.parse_args()

    # Run the simulation
    if args.command=="run":
        # Load correct scenario if provided
        if args.scenario != None:
            with open(args.scenario, "r") as file:
                param_dict = json.loads(file.read())
        else: param_dict = None

        use_plot = not args.noplot

        nobp.run(param_dict, args.outdir, use_plot)
    
    # Save the results from the previous run
    #TODO test if this works.
    elif args.command=="save":
        if args.scenario:
            path = args.scenario
        else:
            i=0
            while(os.path.isfile("run"+i+".py")):
                i+=1
            path = "run"+i+".py"

        if nobp.copy_last_run(path):
            print("Saved last run to", path)
        else:
            print("No run to save :(")