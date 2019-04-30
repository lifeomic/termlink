"""The main program.

This module is the command line interface for running "termlink."
"""
import argparse

from termlink.configuration import Config

from termlink.rxnorm import Command as RxNormCommand

configuration = Config()
logger = configuration.logger

parser = argparse.ArgumentParser(
    description="""
    An ontology conversion toolkit for the Precision Health Cloud.
    """
)

subparsers = parser.add_subparsers(
    title="Commands",
    metavar=""
)

parser_rxnorm = subparsers.add_parser(
    "rxnorm",
    help="RxNorm provides normalized names for clinical drugs.",
    description="""
    RxNorm provides normalized names for clinical drugs and links its names to
    many of the drug vocabularies commonly used in pharmacy management and drug
    interaction software, including those of First Databank, Micromedex, 
    Gold Standard Drug Database, and Multum. By providing links between these 
    vocabularies, RxNorm can mediate messages between systems not using the 
    same software and vocabulary. [1] 
    """,
    epilog="""
    [1] RxNorm. Retrieved April 22, 2019, from https://www.nlm.nih.gov/research/umls/rxnorm/
    """
)
parser_rxnorm.add_argument(
    "uri", metavar="URI", help="resource identifier for files")
parser_rxnorm.set_defaults(execute=RxNormCommand.execute)

args = parser.parse_args()

if hasattr(args, 'execute'):
    args.execute(args)
else:
    parser.print_help()
