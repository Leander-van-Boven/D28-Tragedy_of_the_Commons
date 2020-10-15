from .simulation import Simulator
from .output import ResultsPrinter
from .logger import CsvLogger
from .parameters import default_params
from .util import update_dict
import json
import os
import shutil
from numpy import arange, prod
import itertools as it

def run(override_params=dict(), params_to_range:list=None, 
        param_ranges:list=None, log_dir=None, use_plot=True, verbose=True):
    """Reads and generates param dicts and runs the simulation with them.

    Parameters
    ----------
    override_params : `dict`, optional,
        A dictionary with parameters to override from default, 
        by default None.

    params_to_range : `list`, optional,
        The list of parameters (based on location in parameter 
        dictionary) that will be ranged over.

    param_ranges : `list`, optional,
        The ranges (organized by index) that the params_to_range will 
        range over.

    log_dir : `str`, optional,
        The directory where to save the output, by default None.

    use_plot : `bool`, optional,
        Whether to use real time plotting, by default True.
    """


    # Update the parameter dictionary with the override values
    assert isinstance(override_params, dict)
    #TODO: Check if update_dict performs as expected
    params = update_dict(default_params, override_params)

    # As we need to have at least one iteration, add a single value
    # to the dictionaries if they aren't specified. 
    if not params_to_range:
        params_to_range = ['[\'batch\']']
        param_ranges = [(1,2,1)]
        
    # Generate a CsvLogger class if log_dir is specified
    if log_dir:
        #TODO Add more columns to log
        col_names = params_to_range + ['Epoch', 'Resource']
        for dist_name in params['agent_distributions']:
            col_names.append(dist_name)
        logger = CsvLogger(params['logger_params'], col_names, log_dir)
    else:
        logger = None

    # Generate all discrete values for each ranged parameter
    param_values = [arange(*x) for x in param_ranges]

    # Generate all possible combinations of these ranged values
    value_combis = it.product(*param_values)

    # Calculate the total number of iterations 
    number_of_combis = prod([len(x) for x in param_values])

    # Write the parameters to a json file to make saving possible
    #TODO: Incorporate range and batch parameters to save. 
    with open(".last.json", "w") as file:
        file.write(json.dumps(params))

    # Iterate
    for (run, combi) in enumerate(value_combis):
        
        # Provide run information if verbose mode is on
        if verbose:
            print('\nIteration: %s/%s' % (run+1, number_of_combis))
            print('Params: ' + ', '.join(["%s = %s" % i 
                                         for i in zip(params_to_range, combi)]))
        
        # If not, keep a simple run counter
        else:
            print('Iteration: %s/%s' % (run+1, number_of_combis), end='\r', 
                  flush=True)

        # Add values of ranged parameters to the dictionary
        curr_params = params.copy()
        for param_pair in zip(params_to_range, combi):
            exec('curr_params%s=%s' % param_pair)

        # If real-time plot is on, generate the ResultPrinter class
        printer = None if not use_plot else \
            ResultsPrinter(params['agent_distributions'],
                        params['resource']['max_amount'])

        # Generate the Simulator class
        simulator = Simulator(curr_params, printer, logger, list(combi), 
                              verbose)

        # If we use real-time plotting, we need to pass the simulation
        # to the printer.
        if use_plot:
            printer.start_printer(simulator.generate_simulation)

        # If not, we neet to manually iterate over the simulation
        else:
            simulation = simulator.generate_simulation()
            while True:
                try: next(simulation)
                except StopIteration: break

    # If we have a CsvLogger, then write it to a CSV file
    if log_dir:
        logger.write()

def generate_default_params(path=".defaults.json"):
    '''Used to generate the parameters for the simulation.'''

    with open(path, "w") as file:
        file.write(json.dumps(default_params))


def copy_last_run(param_path, fig_path):
    '''Used to save the results from last run.'''

    if not os.path.isfile('.last.json'):
        return False

    if not os.path.isfile('.lastplot.pdf'):
        return False

    shutil.copyfile('.last.json', param_path)
    shutil.copyfile('.lastplot.pdf', fig_path)

    return True