# Changelog

## [3.3.0] 2019-08-05

### Changed

- [TD-2008] Remove top level condition from neo queries
- [TD-2009] Changed group by system_external_id in cache

## [3.2.0] 2019-07-24

- [TD-1970] Cache all structures external ids under set "structures:external_ids:{system_external_id}"

## [3.1.0] 2019-07-08

### Changed

- [TD-1681] Cache improvements. Field external_ids are now written to the Set "data_fields:external_ids".

## [2.21.0] 2019-06-10

### Changed

- [TD-1824] Changed lua redis script to check for hash type

## [2.15.5] 2019-03-20

### Changed

- [TD-1444] Removes PORT_PRO environment variable

## [2.15.4] 2019-03-18

### Changed

- [TD-1561] Support for Neo4j APOC plugin

## [2.15.3] 2019-03-11

### Changed

- Limit dependencies to 300 in paths query

## [2.15.1] 2019-03-08

### Changed

- Update neo4j driver to 1.7.1
- Increase gunicorn worker timeout to 90s

## [2.14.0] 2019-02-21

### Changed

- [TD-1501] Data import is now managed by neo4j daemon
- [TD-1501] Remove environment-specific configuration from code
- [TD-1478] Refactor PATH_NEO4J to NEO4J_PATH

### Added

- Added changelog file.
