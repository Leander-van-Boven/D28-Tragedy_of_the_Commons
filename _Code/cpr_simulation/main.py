from .simulation import Simulation
from .output import ResultsPrinter
from .logger import CsvLogger
from .parameters import default_params
from .util import update_dict
import json
import os
import shutil
from numpy import arange
import itertools as it

def run(params_to_range:list=["['run']"], param_ranges:list=[(1,2,1)], 
    override_params=dict(), out_dir=None, use_plot=True, use_logger=True):
    """Reads and generates param dicts and runs the simulation with them.

    Parameters
    ----------
    params_to_range : `list`, optional,
        The list of parameters (based on location in parameter 
        dictionary) that will be ranged over.

    param_ranges : `list`, optional,
        The ranges (organized by index) that the params_to_range will 
        range over.

    override_params : `dict`, optional,
        A dictionary with parameters to override from default, 
        by default None.

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
    params = update_dict(default_params, override_params)
        
    param_range_names = [x.replace('][', ':')
                          .replace(']', '')
                          .replace('[', '')
                          .replace('\'', '')
                         for x in params_to_range]

    if out_dir is not None and use_logger:
        #TODO Do something with experiment number?
        col_names = param_range_names + ['Epoch', 'Resource']
        for dist in params['agent_distributions']:
            col_names.append(dist['label'])
        logger = CsvLogger(params['logger_params'], out_dir, col_names)
    else:
        logger = None

    # Generate all combinations of parameters we'll run
    range_combis = it.product(*[arange(*x) for x in param_ranges])

    for combi in range_combis:
        print(', '.join(["%s = %s" % i for i in zip(param_range_names, combi)]))

        curr_params = params.copy()
        for pair in zip(params_to_range, combi):
            exec('curr_params%s=%s' % pair)

        printer = None if not use_plot else \
            ResultsPrinter(params['agent_distributions'],
                        params['resource']['max_amount'])

        sim = Simulation(curr_params, printer, logger, list(combi))

        with open(".last.json", "w") as file:
            file.write(json.dumps(curr_params))

        if use_plot:
            printer.start_printer(sim.run_simulation)
        else:
            sim.run_simulation()

    if out_dir is not None and use_logger:
        logger.write("log.csv")


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