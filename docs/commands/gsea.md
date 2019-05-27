# GSEA - Gene Set Enrichment Analysis

The `gsea` command is used to convert the Gene Set Enrichment Analysis gene set
database.

The input files for this command are available on the [Gene Set Enrichment Analysis](http://software.broadinstitute.org/gsea/downloads.jsp) downloads page.

The command supports the following files:

- msigdb.v6.2.symbols.gmt

These files have been validated and tested. The command may work for other file
types, but is not guaranteed to.

## Getting Started

```sh
python -m termlink gsea file:///msigdb.v6.2.symbols.gmt
```