# import name_of_beautiful_project as nobp
import argparse
import json
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['run', 'save'], 
                        help="Whether to run a new simulation, or to save the previous one")
    parser.add_argument('-d', '--dir', required=False,
                        help="The scenario load or save directory.")
    parser.add_argument('-o', '--out', required=False,
                        help="If desired, the output directory for logging")
    parser.add_argument('--noplot', required=False, action="store_true",
                        help="Add flag to disable real-time plotting")
    print(parser.parse_args())
    args = parser.parse_args()

    if args.command=="run":

        if args.scenario:
            with open(args.scenario, "r") as file:
                param_dict = json.loads(file.read())
        else: param_dict = None

        use_plot = not args.noplot

        nobp.run(param_dict, args.output, use_plot)
    
    elif args.command=="save":

        if args.scenario:
            path = args.scenario
        else:
            i=0
            while(os.path.isfile("run"+i+".py")):
                i+=1
            path = "run"+i+".py"

            


        if nobp.copy_last_run(path):
            print("Saved last run to", path)
        else:
            print("No run to save :(")