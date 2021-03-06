import argparse
import json
import os
import sys

import cpr_simulation as cpr

"""This module is the connection between the user and the simulation.

It parses the commandline arguments and starts the simulation accordingly.
The possible commandline arguments can be requested and reviewed by
running:
>>> python3 sim.py --help
"""

# Constant values for loading and saving scenarios.
SCENARIO_DIR = 'scenarios'
PARAM_NAME = 'params.json'
FIG_NAME = 'figure.pdf'


def run(args):
    """This method is called when `sim.py run` is run.

    This method reads out all command-line arguments parses them and
    starts a simulation from the `cpr_simulation` package.

    Parameters
    ----------
    args : `argparse.Namespace`
        The command-line arguments.
    """

    if args.name:
        path = '%s/%s/%s' % (SCENARIO_DIR, args.name, PARAM_NAME)

        if not os.path.isfile(path):
            print("Couldn't find scenario named %s" % args.name)
            sys.exit(1)

        with open(path) as file:
            param_dict = cpr.util.dd_factory(json.loads(file.read()))
    else:
        param_dict = cpr.util.dd_factory()

    param_ranges = []
    params_to_range = []

    if args.batch > 1:
        param_ranges.append((1, args.batch + 1, 1))
        params_to_range.append("[\'batch\']")

    if args.range:
        names, ranges = zip(*args.range)
        params_to_range += list(names)
        param_ranges += list(ranges)

    if args.param:
        for key, val in args.param:
            if type(val) == str:
                val = "str('%s')" % val
            exec("param_dict%s=%s" % (key, val))

    if args.verbose >= 0:
        verbose = args.verbose
    elif args.range or (args.batch > 1):
        verbose = 0
    else:
        verbose = 1

    if args.jobs > 1:
        plot = False
    elif args.plot is not None:
        plot = args.plot
    elif verbose == 2:
        plot = False
    else:
        plot = (not args.range) and args.batch == 1

    if not args.out and (args.range or args.batch > 1):
        if args.jobs == 1:
            args.out = 'out.csv'
            print("WARNING: No output file specified. falling back to " +
                  "'out.csv'.")
        else:
            if os.path.exists('out'):
                print("Missing argument: Please specify output directory " +
                      " for multi-threaded batch or range mode.")
                sys.exit(1)
            else:
                args.out = 'out'
                print("WARNING: No output directory specified. falling back " +
                      "to 'out'.")

    try:
        cpr.run(param_dict, params_to_range, param_ranges, args.out, plot,
                args.jobs, args.fullscreen, args.resize, verbose)
    except cpr.exception.InvalidArgumentError as e:
        print(f"Inalid argument: {e.message}")
        sys.exit(1)
    except cpr.exception.MissingArgumentError as e:
        print(f"Missing argument: {e.message}")
        sys.exit(1)
    except cpr.exception.InvalidParameterError as e:
        print(f"Invalid parameter: {e.message}")


def save(args):
    """This method is called when `sim.py save` is run.

    This method saves the parameters of the last run non-batch or
    non-range simulation, if it exists.

    Parameters
    ----------
    args : `argparse.Namespace`
        The command-line arguments.
    """

    if not os.path.isdir(SCENARIO_DIR):
        os.mkdir(SCENARIO_DIR)

    if args.name:
        path = '%s/%s' % (SCENARIO_DIR, args.name)

        if os.path.isdir(path):
            print("A scenario named \'%s\' already exists" % args.name)
            sys.exit(1)

        name = args.name
        os.mkdir(path)
    else:
        i = 0
        name = 'scenario%s' % i
        path = '%s/%s' % (SCENARIO_DIR, name)

        while os.path.isfile(path):
            i += 1
            name = 'scenario%s' % i
            path = '%s/%s' % (SCENARIO_DIR, name)

        os.mkdir(path)

    param_path = '%s/%s' % (path, PARAM_NAME)
    fig_path = '%s/%s' % (path, FIG_NAME)

    if cpr.copy_last_run(param_path, fig_path):
        print("Saved scenario as \'%s\'" % name)
    else:
        print("There is no scenario to save :(")


def llist(_):
    """This method is called when `sim.py list` is run.

    This method lists all saved scenarios as saved by the save method.

    Parameters
    ----------
    _ : `argparse.Namespace`
        The command-line arguments.
    """
    print('\n'.join(
        sorted([path for path in os.listdir(SCENARIO_DIR) if
                os.path.isdir('%s\\%s' % (SCENARIO_DIR, path))])))


def str2bool(v):
    """Converts a string representation of a truth value to a boolean
    type. This method is case-insensitive.

    Parameters
    ----------
    v : `str`,
        The input string that represents a truth value. Should be one of
        the following: yes/no, true/false, t/f, y/n, 1/0.

    Returns
    -------
    `bool`,
        The output boolean.
    """

    if v is None:
        return None
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    if v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    raise argparse.ArgumentTypeError('Boolean value expected.')


def str2locval(x):
    """Converts a string to a parameter tuple.

    Parameters
    ----------
    x : `str`,
        The input string. Should follow this syntax:
        `root:nest:nest=int`.

    Returns
    -------
    `(str, int)`,
        `str` represents the literal location of the parameter in the
        dictionary, and `int` represents the value this parameter should
        get.
    """
    try:
        (param, val) = tuple(x.split('='))
        res = "[\'" + "\'][\'".join(param.split(':')) + "\']"
        try:
            return res, type(eval('cpr.default_params' + res))(val)
        except KeyError:
            return res, float(val)

    except ValueError:
        raise argparse.ArgumentTypeError("Invalid argument syntax")


def str2locrange(x):
    """Converts a string to a parameter tuple.

    Parameters
    ----------
    x : `str`,
        The input string. Should follow this syntax:
        `root:nest:nest=from,to,incr`.

    Returns
    -------
    `(str, tup)`,
        `str` represents the literal location of the parameter in the
        dictionary, and `tup` represents the value range this parameter
        should get.
    """
    try:
        (param, val) = tuple(x.split('='))
        return ("[\'" + "\'][\'".join(param.split(':')) + "\']",
                map(float, val.split(',')))
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid argument syntax")


if __name__ == '__main__':
    '''Main script fuction'''

    # Define possible CL arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'command', choices=['run', 'save', 'list'],
        help='run: run a simulation; save: save the previous simulation; ' +
             'list: list all saved simulations')
    parser.add_argument(
        '-n', '--name', required=False, type=str, metavar='scenario',
        help='the name of the scenario to load or to save')
    parser.add_argument(
        '-p', '--param', required=False, nargs='+', type=str2locval,
        metavar='item', help='add parameters to override its value, ' +
                             'e.g. resource:start_amount=600')
    parser.add_argument(
        '-b', '--batch', required=False, default=1, type=int, metavar='int',
        help='the amount of times the same experiment should be run '
             + '(defaults to 1)')
    parser.add_argument(
        '-r', '--range', required=False, nargs='+', type=str2locrange,
        metavar='item', help="add parameters to run the simulation with a " +
                             "range of values, e.g. resource:start_amount=" +
                             "300,601,100")
    parser.add_argument(
        '-j', '--jobs', required=False, default=1, type=int, metavar='int',
        help="the amount of parallel processes in range or batch mode")
    parser.add_argument(
        '-o', '--out', required=False, type=str, metavar='path',
        help='the output path for CSV logging')
    parser.add_argument(
        '-P', '--plot', required=False, default=None, const=True,
        type=str2bool, nargs='?', metavar='bool',
        help='whether to show a real-time plot')
    parser.add_argument(
        '-v', '--verbose', required=False, default=-1, const=1,
        type=int, nargs='?', metavar='int',
        help="whether to enter verbose mode [0..2]")
    parser.add_argument(
        '-f', '--fullscreen', required=False, default=False, const=True,
        type=str2bool, nargs='?', metavar='bool',
        help='whether to show the plot in fullscreen')
    parser.add_argument(
        '--resize', required=False, default=False, const=True,
        type=str2bool, nargs='?', metavar='bool',
        help='whether to enable plot resizing without plot reset')

    # Parse the arguments that were input
    args = parser.parse_args()

    # Run the right method, based on CL arguments
    # We had to rename the method `list`, as otherwise it would have
    # conflicted with the `list` type.
    if args.command == 'list':
        args.command = 'llist'
    eval(args.command)(args)
