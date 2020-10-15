'''This module is the connection between the user and the simulation.

It parses the commandline arguments and starts the simulation accordingly.
The possible commandline arguments can be requested and reviewed by
running: 
>>> python3 sim.py --help
'''

#TODO:
# - Check behavior of output path for csv logger
# - Implement plot default true if single exp, default false if batch or
#   range. 

import cpr_simulation as cpr
import argparse
import json
import os, sys
from collections import defaultdict

SCENARIO_DIR = 'scenarios'
PARAM_NAME = 'params.json'
FIG_NAME = 'figure.pdf'


def test(args):
    pass


def dd_factory(d = None):
    if d:
        return defaultdict(dd_factory, d)
    else:
        return defaultdict(dd_factory)


def run(args):
    if args.name:
        path = '%s\\%s\\%s' % (SCENARIO_DIR, args.name, PARAM_NAME)

        if not os.path.isfile(path):
            print("Couldn't find scenario named %s" % args.name)
            sys.exit(1)

        with open(path) as file:
            param_dict = dd_factory(json.loads(file.read()))
    else: 
        param_dict = dd_factory()


    param_ranges = [(1,args.batch+1,1)]
    params_to_range = ["[run]"]

    if args.range:
        names, ranges = zip(*args.range)
        params_to_range += list(names)
        param_ranges += list(ranges)

    if args.param:
        for param_pair in args.param:
            exec('param_dict%s=%s' % param_pair)

    plot = args.plot if args.plot is not None else \
        not (args.range or args.batch-1)

    verbose = args.verbose if args.verbose is not None else \
        not (args.range or args.batch-1)

    cpr.run(param_dict, params_to_range, param_ranges, args.out, plot, 
            verbose)


def save(args):
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


def llist(_):
    print('\n'.join(
        sorted([path for path in os.listdir(SCENARIO_DIR) if \
                os.path.isdir('%s\\%s' % (SCENARIO_DIR, path))])))


def str2bool(v):
    if v is None:
        return None
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    if v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    raise argparse.ArgumentTypeError('Boolean value expected.')


def str2locint(x):
    try:
        (param, val) = tuple(x.split('='))
        return ("[\'" + "\'][\'".join(param.split(':')) + "\']", int(val))
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid argument syntax")


def str2locrange(x):
    try:
        (param, val) = tuple(x.split('='))
        return ("[\'" + "\'][\'".join(param.split(':')) + "\']", 
                map(int, val.split(',')))
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid argument syntax")


if __name__ == '__main__':
    # Define possible arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'command', choices=['run', 'save', 'list', 'test'], 
        help='run: run a simulation; save: save the previous simulation; ' +
             'list: list all saved simulations; test: for testing purposes')
    parser.add_argument(
        '-n', '--name', required=False, type=str, metavar='scenario',
        help='the scenario name to load from, or to save to')
    parser.add_argument(
        '-o', '--out', required=False, type=str, metavar='file_path',
        help='the output path for CSV logging')
    parser.add_argument(
        '-P', '--plot', required=False, default=None, const=True, type=str2bool,
        nargs='?', metavar='bool', help='whether to show a real-time plot')
    parser.add_argument(
        '-v', '--verbose', required=False, default=None, const=True, 
        type=str2bool, nargs='?', metavar='bool',
        help="whether to enter verbose mode")
    parser.add_argument(
        '-b', '--batch', required=False, default=1, type=int, metavar='amount',
        help='the amount of times the same experiment should be run (def. 1)')
    parser.add_argument(
        '-r', '--range', required=False, nargs='+', type=str2locrange,
        metavar='param=from,to,incr',
        help="add parameters to run the simulation with a range of values")
    parser.add_argument(
        '-p', '--param', required=False, nargs='+', type=str2locint, 
        metavar='param=value', help="add parameters to override its value")


    # Parse the inputted arguments
    args = parser.parse_args()

    # print(args)
    # sys.exit(1)

    # Run the right method, based on CL argument
    # We had to rename the method `list`, as otherwise it would have 
    # conflicted with the type.
    if args.command=='list':
        args.command='llist'
    eval(args.command)(args)


        