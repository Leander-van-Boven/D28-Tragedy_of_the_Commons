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

SCENARIO_DIR = 'scenarios'
PARAM_NAME = 'params.json'
FIG_NAME = 'figure.pdf'

if __name__ == '__main__':
    # Define possible arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'command', choices=['run', 'save', 'list'], 
        help='Whether to run a new simulation, or to save the previous one')
    # parser.add_argument(
    #     '-p', '--path', required=False,
    #     help='The scenario load or save directory.')
    parser.add_argument(
        '-n', '--name', required=False,
        help='The scenario name to load, or save to')
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

        param_dict = None
        if args.name:
            path = '%s\\%s\\%s' % (SCENARIO_DIR, args.name, PARAM_NAME)

            if not os.path.isfile(path):
                print("Couldn't find scenario named %s" % args.name)
                sys.exit(1)

            with open(path) as file:
                param_dict = json.loads(file.read())

        nobp.run(param_dict, args.logdir, not args.noplot)
        # if args.path:
        #     try:
        #         if os.path.isdir(args.path):
        #             loc = f'{args.path}\\params.json'
        #             with open(args.path+'\\params.json', 'r') as file:
        #                 param_dict = json.loads(file.read())
        #         elif os.path.isfile(args.path):
        #             loc = args.path
        #             with open(args.path, 'r') as file:
        #                 param_dict = json.loads(file.read())
        #     except FileNotFoundError:
        #         print('Parameter file not found: %s' % loc)
        #         sys.exit(1)
            #TODO: Catch more errors if needed
        # Load correct scenario if provided
        # if args.scenario != None:
        #     with open(args.scenario, 'r') as file:
        #         param_dict = json.loads(file.read())


    
    # Save the results from the previous run
    #TODO test if this works.
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

        if nobp.copy_last_run(param_path, fig_path):
            print("Saved scenario as \'%s\'" % name)
        else:
            print("There is no scenario to save :(")

        # if args.path and os.path.isdir(args.path):
        #     path = args.path
        # else:
        #     i=0
        #     while(os.path.isfile('run'+i+'.py')):
        #         i+=1
        #     path = 'run'+i+'.py'

        # if nobp.copy_last_run(path):
        #     print('Saved last run to', path)
        # else:
        #     print('No run to save :(')

    elif args.command=='list':
        print('\n'.join(sorted([path for path in os.listdir(SCENARIO_DIR) if \
            os.path.isdir('%s\\%s' % (SCENARIO_DIR, path))])))