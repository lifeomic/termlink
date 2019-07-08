# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## Added

- Adds support for ValueSet and CodeSystem system identifiers to the `common` sub-command.

## 0.9.2

## Added

- Adds optional argument `--output` to `gsea` sub-command
- Adds support for inverse relationship to the `common` sub-command

## 0.9.1

## Added

- Adds support for 'equivalent_to' relationships in the `common` sub-command
- Adds support for implicit system references in the `common` sub-command

## 0.9.0

### Added

- Adds a new sub-command: `code-system`

### Changed

- Alters the output format for the `common` sub-command to JSON Lines
- Improves the runtime performance of the `gsea` sub-command
- Reduces the memory footprint of the `gsea` sub-command

## 0.8.1

### Fixed

- Fixes the PyPi release package

## 0.8.0

### Added

- Adds a new sub-command: `snomed-ct`

## 0.7.1

### Added

- Adds support for additional source vocabularies to the `rxnorm` sub-command using the `-v` option
- Adds support for additional suppress flag filtering to the `rxnorm` sub-command using the `-s` option

## 0.7.0

### Added

- Adds a new sub-command: `gsea`

## 0.6.1

### Fixed

- Fixed `rxnorm` sub-command to properly display output

## 0.6.0

## Added

- Adds a new sub-command: `common`
- Adds support for .obo file types to `common` sub-command
- Adds support for .owl file types to `common` sub-command

### Changed

- Improved performance of internal JSON serialization.

## 0.5.0

### Added

- Adds support for the Human Phentotype Ontology: `hpo` subcommand
- Adds `--skip-alt-ids` flag to `hpo` sub-command
- Adds `--skip-synonyms` flag to `hpo` sub-command

### Changed

- Updates Docker image to latest pip version

## 0.4.4

### Changed

- Prints the help message by default if a valid command is not provided.

## 0.4.3

### Changed

- Improved the `rxnorm` sub-command help documentation

### Fixed

- Fixed "File Not Found" error in `rxnorm` sub-command for case sensitive file systems

## 0.4.2

### Security

- Patched CVE-2019-11324 - Upgraded urllib3 library to v1.24.2

## 0.4.1

### Fixed

- Added new line to output of `rxnorm` sub-command

## 0.4.0

### Changed

- Improved performance of the `rxnorm` sub-command

### Fixed

- Corrected the output of the `rxnorm` sub-command to include the correct concept relationships.
