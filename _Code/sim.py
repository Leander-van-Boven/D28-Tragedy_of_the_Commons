'''This module is the connection between the user and the simulation.

It parses the commandline arguments and starts the simulation accordingly.
The possible commandline arguments can be requested and reviewed by
running: 
>>> python3 sim.py --help
'''

#TODO maybe find a more suitable name to nobp
import cpr_simulation as cpr
import argparse
import json
import os, sys

SCENARIO_DIR = 'scenarios'
PARAM_NAME = 'params.json'
FIG_NAME = 'figure.pdf'

if __name__ == '__main__':
    # Define possible arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'command', choices=['run', 'save', 'list'], 
        help='Whether to run a new simulation, or to save the previous one')
    parser.add_argument(
        '-n', '--name', required=False,
        help='The scenario name to load, or save to')
    parser.add_argument(
        '-o', '--logdir', required=False,
        help='If desired, the output directory for CSV logging')
    parser.add_argument(
        '--noplot', required=False, action='store_true',
        help='Add flag to disable real-time plotting')

    # Parse the inputted arguments
    args = parser.parse_args()

    # If we want to run the simulation:
    if args.command=='run':

        param_dict = None
        if args.name:
            path = '%s\\%s\\%s' % (SCENARIO_DIR, args.name, PARAM_NAME)

            if not os.path.isfile(path):
                print("Couldn't find scenario named %s" % args.name)
                sys.exit(1)

            with open(path) as file:
                param_dict = json.loads(file.read())

        cpr.run(param_dict, args.logdir, not args.noplot)

    # Or, if we want to save the previous simulation:
    elif args.command=='save':

        if not os.path.isdir(SCENARIO_DIR):
            os.mkdir(SCENARIO_DIR)

        if args.name:
            path = '%s\\%s' % (SCENARIO_DIR, args.name)

            if os.path.isdir(path):
                print("A scenario named \'%s\' already exists" % args.name)
                sys.exit(1)  

            name = args.name
            os.mkdir(path)         
        else:
            i=0
            name = 'scenario%s' % i
            path = '%s\\%s' % (SCENARIO_DIR, name)

            while(os.path.isfile(path)):
                i += 1
                name = 'scenario%s' % i
                path = '%s\\%s' % (SCENARIO_DIR, name)

            os.mkdir(path)
            
        param_path = '%s\\%s' % (path, PARAM_NAME)
        fig_path = '%s\\%s' % (path, FIG_NAME)

        if cpr.copy_last_run(param_path, fig_path):
            print("Saved scenario as \'%s\'" % name)
        else:
            print("There is no scenario to save :(")

    # Or, if we want to list all saved scenarios:
    elif args.command=='list':

        print('\n'.join(sorted([path for path in os.listdir(SCENARIO_DIR) if \
              os.path.isdir('%s\\%s' % (SCENARIO_DIR, path))])))