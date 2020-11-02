import itertools as it
import json
import os
import shutil

from numpy import arange, prod

from . import exception
from .logger import CsvLogger
from .output import ResultsPlotter
from .parameters import default_params
from .simulation import Simulator
from .util import update_dict


def run(override_params=dict(), params_to_range=None, param_ranges=None,
        log_path=None, use_plot=True, n_jobs=1, fullscreen_plot=True, 
        verbose=1):
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

    log_path : `str`, optional,
        The path where to save the output, by default None.

    use_plot : `bool`, optional,
        Whether to use real time plotting, by default True.

    n_jobs : `int`, optional,
        The amount of jobs to simultaneously run.

    fullscreen_plot : `bool`, optional,
        Whether to make the real-time plotting window full-screen, by
        default True

    verbose : `int`, optional,
        The verbose mode. 0 = iteration count, 1 = status every
        epoch, 2 = detailed breakdown per epoch, halt each epoch.
    """

    # Update the parameter dictionary with the override values
    assert isinstance(override_params, dict)
    params = update_dict(default_params, override_params)

    # Get more print-friendly parameter locations
    param_names = [
        ':'.join(x.split('\'][\''))[2:-2] for x in params_to_range]

    def _get_logger(fn=None):
        """Generate a CsvLogger class with right parameters, 
        if out_path is specified. Returns None if not.
        """

        if log_path:
            col_names = \
                ['Exp Num'] + param_names + \
                ['Epoch', 'Resource', 'Count', 'A', 'B', 'C', 'D', 'E',
                 'Median', 'Below', 'Above', 'Mean', 'STD', 'Resource Limit',
                 'Resource Unlimit']
            if fn:
                ld = f"{log_path}/{fn}"
            else:
                ld = log_path
            logger = CsvLogger(params['logger_params'], col_names, ld)
        else:
            logger = None
        return logger

    def _run_sim(p, c=[0], lg=None):
        """Local method that generates and runs a simulation. This is a 
        local method as the way we call it depends on operating mode.
        """

        # If real-time plot is on, generate the ResultPrinter class
        printer = None if not use_plot else \
            ResultsPlotter(
                params['agent']['count'],
                params['plotter_params']['svo_bar_count'],
                params['resource']['start_amount'],
                fullscreen_plot)

        # Generate the Simulator class
        simulator = Simulator(p, printer, lg, list(c),
                              verbose)

        # If we use real-time plotting, we need to pass the simulation
        # to the printer.
        if use_plot:
            printer.start_printer(simulator.generate_simulation)
        # If not, we need to manually iterate over the simulation
        else:
            simulation = simulator.generate_simulation()
            while True:
                try:
                    next(simulation)
                except StopIteration:
                    break

    # If not parameter range is specified, no loop is required.
    if not params_to_range:
        logger = _get_logger()

        with open('.last.json', 'w') as file:
            file.write(json.dumps(params))

        _run_sim(params, lg=logger)

    # If a parameter range is specified, we'll need to find out
    # what to loop over
    else:
        # Generate all discrete values for each ranged parameter
        param_values = [arange(*x) for x in param_ranges]

        # Generate all possible combinations of these ranged values
        value_combis = it.product(*param_values)

        # Calculate the total number of iterations
        number_of_combis = prod([len(x) for x in param_values])

        if n_jobs <= 1:
            # If running single-threaded
            logger = _get_logger()

            # Iterate
            for (run, combi) in enumerate(value_combis):
                # Provide run information if verbose mode is on
                if verbose == 1:
                    print('\nIteration: %s/%s' % (run + 1, number_of_combis))
                    print('Params: ' +
                          ', '.join(
                            ["%s = %s" % i for i in zip(param_names, combi)]))
                else:
                    # If not, keep a simple run counter
                    print('Iteration: %s/%s' % (run + 1, number_of_combis),
                          end='\r', flush=True)

                # Add values of ranged parameters to the dictionary
                curr_params = params.copy()
                for param_pair in zip(params_to_range, combi):
                    exec('curr_params%s=%s' % param_pair)

                _run_sim(curr_params, [run] + list(combi), logger)
        else:
            # If running multi-threaded
            if not log_path:
                raise exception.MissingArgumentError(
                    "Please specify the target directory for the output CSV"
                    " files using --out.")
            if not os.path.exists(log_path):
                os.mkdir(log_path)
            elif not os.path.isdir(log_path):
                raise exception.InvalidArgumentError(
                    "Error: --out argument should be a directory in" +
                    " multithreaded mode")

            from joblib import Parallel, delayed
            print("Running %s instances..." % number_of_combis)

            # Make a method that can be called by the Parallel class
            def _run_parallel(run, combi):
                logger = _get_logger(f"run{run}.csv")

                # Add values of ranged parameters to the dictionary
                curr_params = params.copy()
                for param_pair in zip(params_to_range, combi):
                    exec('curr_params%s=%s' % param_pair)

                _run_sim(curr_params, [run] + list(combi), logger)

                if logger:
                    logger.write()

            # Run all experiments in parallel, with batch_size to 16 as 
            # experiments tend to be quite quick
            Parallel(n_jobs=n_jobs, verbose=10, batch_size=16)(
                delayed(_run_parallel)(*tup) for tup in enumerate(value_combis))

    # If we have a CsvLogger, then write it to a CSV file
    if log_path and n_jobs <= 1:
        logger.write()


def save_modified_params(path, override_params=dict()):
    """Don't run, but only save the overriden parameter file."""
    assert isinstance(override_params, dict)
    params = update_dict(default_params, override_params)

    with open(path, 'w') as file:
        file.write(json.dumps(params))


def save_default_params(path=".defaults.json"):
    """Used to generate the parameters for the simulation."""

    with open(path, "w") as file:
        file.write(json.dumps(default_params))


def copy_last_run(param_path, fig_path):
    """Used to save the results from last run."""

    if not os.path.isfile('.last.json'):
        return False

    shutil.copyfile('.last.json', param_path)
    if os.path.isfile('.lastplot.pdf'):
        shutil.copyfile('.lastplot.pdf', fig_path)
    return True
