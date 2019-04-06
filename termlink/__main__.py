"""The main program.

This module is the command line interface for running "termlink."
"""
import argparse

from termlink.configuration import Config

from termlink.rxnorm import Command as RxNormCommand

configuration = Config()
logger = configuration.logger

parser = argparse.ArgumentParser(
    description="A utility program for uploading terminologies"
)

subparsers = parser.add_subparsers(title="Commands", description="", help="")

parser_rxnorm = subparsers.add_parser("rxnorm", help="Upload an RxNorm dataset")
parser_rxnorm.add_argument("uri", metavar="URI", help="resource identifier for files")
parser_rxnorm.set_defaults(execute=RxNormCommand.execute)

args = parser.parse_args()
args.execute(args)
