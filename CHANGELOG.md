# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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