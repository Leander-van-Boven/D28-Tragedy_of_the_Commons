#import name_of_beautiful_project as nobp
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['run', 'save'], 
                        help="Whether to run a new simulation, or to save the previous one")
    parser.add_argument('directory',
                        help="The directory to load, or save, the parameters from, or to")
    parser.add_argument('--output', '-o', required=False,
                        help="If desired, the output directory")
    parser.add_argument('--noplot', '-n', required=False, action="store_true",
                        help="Add flag to disable real-time plotting")
    print(parser.parse_args())
