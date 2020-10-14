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

    out_dir : `str`, optional,
        The directory where to save the output, by default None.

    use_plot : `bool`, optional,
        Whether to use real time plotting, by default True.
    """

    # if not override_params:
    #     params = default_params
    # else:
    #     params = override_params

    #TODO: Check if update_dict performs as expected
    assert isinstance(override_params, dict)
    params = update_dict(default_params, override_params)

    #print(params)

    if not params_to_range:
        params_to_range = ['[run]']
        param_ranges = [(1,2,1)]
        

    if log_dir:
        #TODO Do something with experiment number?
        col_names = params_to_range + ['Epoch', 'Resource']
        for dist in params['agent_distributions']:
            col_names.append(dist['label'])
        logger = CsvLogger(params['logger_params'], col_names, log_dir)
    else:
        logger = None

    # Generate all combinations of parameters we'll run
    param_values = [arange(*x) for x in param_ranges]
    value_combis = it.product(*param_values)
    number_of_combis = prod([len(x) for x in param_values])

    for (run, combi) in enumerate(value_combis):
        if verbose:
            print('\n%s/%s' % (run+1, number_of_combis))
            print(', '.join(["%s = %s" % i 
                                  for i in zip(params_to_range, combi)]))
        else:
            print('%s/%s' % (run+1, number_of_combis), end='\r', flush=True)

        curr_params = params.copy()
        for param_pair in zip(params_to_range, combi):
            exec('curr_params%s=%s' % param_pair)

        printer = None if not use_plot else \
            ResultsPrinter(params['agent_distributions'],
                        params['resource']['max_amount'])

        simulator = Simulator(curr_params, printer, logger, list(combi), 
                              verbose)

        with open(".last.json", "w") as file:
            file.write(json.dumps(curr_params))

        if use_plot:
            printer.start_printer(simulator.generate_simulation)
        else:
            simulation = simulator.generate_simulation()
            while True:
                try: next(simulation)
                except StopIteration: break

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