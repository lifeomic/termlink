# Common

The `common` command is used to convert ontologies, not otherwise supported,
in a generic way.

The command supports the following file formats:

- OBO (.obo)
- RDF/XML (.owl)

It is expected that the system to be recorded in the Precision Health Cloud to
be different than the provided ontology IRI. Therefore a system value is also
required.

## Getting Started

```sh
python -m termlink common file://FILE.{obo,owl} -s SYSTEM
```