'''This module is the connection between the user and the simulation.

It parses the commandline arguments and starts the simulation accordingly.
The possible commandline arguments can be requested and reviewed by
running: 
>>> python3 sim.py -h
'''

#TODO maybe find a more suitable name to nobp
import name_of_beautiful_project as nobp
import argparse
import json
import os, sys

if __name__ == '__main__':
    # Define possible arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'command', choices=['run', 'save'], 
        help='Whether to run a new simulation, or to save the previous one')
    parser.add_argument(
        '-p', '--path', required=False,
        help='The scenario load or save directory.')
    parser.add_argument(
        '-o', '--logdir', required=False,
        help='If desired, the output directory for logging')
    parser.add_argument(
        '--noplot', required=False, action='store_true',
        help='Add flag to disable real-time plotting')

    # Parse the inputted arguments
    args = parser.parse_args()

    # Run the simulation
    if args.command=='run':
        if args.path:
            try:
                if os.path.isdir(args.path):
                    loc = f'{args.path}\\params.json'
                    with open(args.path+'\\params.json', 'r') as file:
                        param_dict = json.loads(file.read())
                elif os.path.isfile(args.path):
                    loc = args.path
                    with open(args.path, 'r') as file:
                        param_dict = json.loads(file.read())
            except FileNotFoundError:
                print('Parameter file not found: %s' % loc)
                sys.exit(1)
            #TODO: Catch more errors if needed
        # Load correct scenario if provided
        # if args.scenario != None:
        #     with open(args.scenario, 'r') as file:
        #         param_dict = json.loads(file.read())
        else: param_dict = None

        nobp.run(param_dict, args.logdir, not args.noplot)
    
    # Save the results from the previous run
    #TODO test if this works.
    elif args.command=='save':
        if args.path and os.path.isdir(args.path):
            path = args.path
        else:
            i=0
            while(os.path.isfile('run'+i+'.py')):
                i+=1
            path = 'run'+i+'.py'

        if nobp.copy_last_run(path):
            print('Saved last run to', path)
        else:
            print('No run to save :(')