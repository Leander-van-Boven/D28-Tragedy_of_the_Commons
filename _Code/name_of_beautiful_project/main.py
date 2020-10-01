from .simulation import Simulation
from .output import ResultsPrinter
from .logger import CsvLogger
from .parameters import p as default_params
import json
import os,sys
import shutil

def run(params=None, out_dir=None, use_plot=True):
    """Reads and generates param dicts and runs the simulation with them

    Parameters
    ----------
    params : `dict`, optional,
        A dictionary with parameters to use by the sim, by default None

    out_dir : `str`, optional,
        The directory where to save the output, by default None

    use_plot : `bool`, optional,
        Whether to use real time plotting, by default True
    """

    if not params:
        # if not os.path.isfile('.defaults.json'):
        #     generate_default_params()
        generate_default_params()
        with open('.defaults.json', 'r') as file:
            s = file.read()
        params = json.loads(s)

    if out_dir:
        logger = CsvLogger(out_dir)
    else:
        logger = None
    
    sim = Simulation(params, logger)

    with open(".last.json", "w") as file:
        file.write(json.dumps(params))

    if use_plot:
        printer = ResultsPrinter(
            params['agent_distributions']
            , params['resource']['max_amount'])
        printer.start_printer(sim.run_simulation)
    else:
        sim.run_simulation()

    #print(sim.result)


def generate_default_params():
    '''Used to generate the parameters for the simulation'''

    with open(".defaults.json", "w") as file:
        file.write(json.dumps(default_params))


def copy_last_run(path):
    '''Used to save the results from last run'''

    if not os.path.isfile('.last.json'):
        return False

    shutil.copyfile('.last.json', path)
    return True