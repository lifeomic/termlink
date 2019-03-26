"""The main program.

This module is the command line interface for running "termlink."
"""
import argparse

from urllib.parse import urlparse

from termlink import rxnorm
from termlink.configuration import Config

configuration = Config()
logger = configuration.logger

parser = argparse.ArgumentParser(
    description="A utility program for uploading terminologies"
)

subparsers = parser.add_subparsers(title="Commands", description="", help="")

parser_rxnorm = subparsers.add_parser("rxnorm", help="Upload an RxNorm dataset")
parser_rxnorm.add_argument("uri", metavar="URI", help="resource identifier for files")

args = parser.parse_args()

uri = urlparse(args.uri)

logger.info("Loading dataset from %s.", uri.scheme)
if uri.scheme == "file":
    path = uri.path
    rxnorm.upload(path)
else:
    raise Exception("Scheme %s not supported" % uri.scheme)
