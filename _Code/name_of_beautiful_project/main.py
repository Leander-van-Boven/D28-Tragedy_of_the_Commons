from .simulation import Simulation
from .output import ResultsPrinter
from .logger import CsvLogger
import json
import os,sys
import shutil

def run(params=None, out_dir=None, use_plot=True):
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
            sum(dist['agent_count'] 
                for dist 
                in params['simulation']['agent_distributions'])
            , params['simulation']['agent_distributions']
            , params['resource']['max_amount'])
        printer.start_printer(sim.run_simulation)
    else:
        sim.run_simulation()

    #print(sim.result)


def generate_default_params():
    p = {
        "agent" : {
            "metabolism" : 2,               # The 'cost' of staying alive per epoch (in energy)
            "procreate_req" : 16,           # The amount of energy an agent needs to have before it can create offspring
            "procreate_cost" : 10,          # The amount of energy it costs to create a new child
            "maximum_age" : 100,           # The maximum age for the agent, the agent gets 'removed' when its age exceeds this parameter
        },

        "resource" : {
            "start_amount" : 500,           # The starting amount of units of the common resource
            "max_amount" : 1000,              # The maximum amount units there can be at one epoch
            "min_amount" : 0,                # The minimum amount of units. 
            "growth_rate" : 1.42,            # The growth rate (in units) of the common resource
            "energy_per_unit" : 5,          # The amount of energy one unit provides
        },

        "simulation" : {
            "max_epoch" : 1000,
            "plot_interval" : 2,
            "print_interval" : 1,
            "agent_distributions" : [
                {
                    "label" : "proself",
                    "line_style" : ':',
                    "agent_count" : 25,
                    "min_social_value" : 0,
                    "max_social_value" : .25
                },
                {
                    "label" : "prosocial",
                    "line_style" : '--',
                    "agent_count" : 25,
                    "min_social_value" : .75,
                    "max_social_value" : 1
                }
            ]
        }
    }

    with open(".defaults.json", "w") as file:
        file.write(json.dumps(p))


def copy_last_run(path):

    if not os.path.isfile('.last.json'):
        return False

    shutil.copyfile('.last.json', path)
    return True