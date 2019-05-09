"""The main program.

This module is the command line interface for running "termlink."
"""
import argparse

from termlink.configuration import Config

from termlink.rxnorm import Command as RxNormCommand
from termlink.hpo import Command as HPOCommand
from termlink.common import Command as CommonCommand
from termlink.gsea import Command as GSEACommand

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

parser_common = subparsers.add_parser(
    "common",
    help="Converts a common format ontology",
    description="""
    Converts an ontology represented in a common format. The following file 
    types are supported: .obo and .owl. 
    """
)

parser_common.add_argument(
    "uri",
    metavar="URI",
    help="resource identifier for files"
)

parser_common.add_argument(
    "-s",
    "--system",
    help="identity of the terminology system",
    required=True
)

parser_common.set_defaults(execute=CommonCommand.execute)

parser_hpo = subparsers.add_parser(
    "hpo",
    help="Converts the 'Human Phenotype Ontology'",
    description="""
    The Human Phenotype Ontology (HPO) project provides an ontology of medically relevant phenotypes, disease-phenotype annotations, and the algorithms that operate on these. The HPO can be used to support differential diagnostics, translational research, and a number of applications in computational biology by providing the means to compute over the clinical phenotype. The HPO is being used for computational deep phenotyping and precision medicine as well as integration of clinical data into translational research. Deep phenotyping can be defined as the precise and comprehensive analysis of phenotypic abnormalities in which the individual components of the phenotype are observed and described. The HPO is being increasingly adopted as a standard for phenotypic abnormalities by diverse groups such as international rare disease organizations, registries, clinical labs, biomedical resources, and clinical software tools and will thereby contribute toward nascent efforts at global data exchange for identifying disease etiologies (Köhler et al, 2017). [1]
    """,
    epilog="""
    [1] Human Phenotype Ontology. Retrieved April 29, 2019, from https://hpo.jax.org/app/help/introduction
    """
)

parser_hpo.add_argument(
    "uri",
    metavar="URI",
    help="resource identifier for files"
)

parser_hpo.add_argument(
    "--skip-alt-ids",
    dest='skip_alt_ids',
    action='store_true',
    help="skips 'alt_id' references"
)

parser_hpo.add_argument(
    "--skip-synonyms",
    dest='skip_synonyms',
    action='store_true',
    help="skips 'synonym' references"
)

parser_hpo.set_defaults(execute=HPOCommand.execute)
parser_hpo.set_defaults(skip_alt_ids=False)
parser_hpo.set_defaults(skip_synonyms=False)


parser_rxnorm = subparsers.add_parser(
    "rxnorm",
    help="Converts the 'RxNorm' code system",
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
    "uri",
    metavar="URI",
    help="resource identifier for files"
)

parser_rxnorm.set_defaults(execute=RxNormCommand.execute)

parser_gsea = subparsers.add_parser(
    "gsea",
    help="Converts the 'Gene Set Enrichment Analysis Ontology'",
    description="""
    The Gene Set Enrichment Analysis Ontology (GSEA) project provides an ontology of genes grouped by a 
    relational concept. [1]
    """,
    epilog="""
    [1] Gene Set Enrichment Analysis Ontology. Retrieved May 8, 2019, from http://software.broadinstitute.org/gsea/msigdb/collections.jsp
    """
)

parser_gsea.add_argument(
    "uri",
    metavar="URI",
    help="resource identifier for files"
)

parser_gsea.set_defaults(execute=GSEACommand.execute)

args = parser.parse_args()

if hasattr(args, 'execute'):
    args.execute(args)
else:
    parser.print_help()

