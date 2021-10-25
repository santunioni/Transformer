## 2.2.0 (2021-10-25)

### Feat

- add possibility for changing the metadata

### BREAKING CHANGE

- Breaks backward compatibility, as the clients must now unpack the (data, metadata) tuple for retrieving the data field.

## 2.2.0a1 (2021-10-23)

## 2.2.0a0 (2021-10-21)

### Feat

- change library structure

### BREAKING CHANGE

- The API is now used differently. This can break code at "import-module-time".

## v2.1.7 (2021-10-06)

### Fix

- add build-system to pyproject.toml

## v2.1.6 (2021-10-06)

### Fix

- add __VERSION__ to __init__.py

## v2.1.5 (2021-10-06)

### Fix

- add license

## v2.1.4 (2021-10-06)

## v2.1.3 (2021-10-06)

## v2.1.2 (2021-10-06)

## v2.1.1 (2021-10-06)

## v2.1.0 (2021-10-06)

### Feat

- change attribute in commands "command_name" to "name"

### BREAKING CHANGE

- changing the "command_name" field to "name" may result in breaking some MatConfigs

## v2.0.1 (2021-09-30)

## v2.0.0 (2021-09-30)

### Fix

- change classes names

### Refactor

- fix typing in letter handler
- change config property names and add descriptor for each config to use

## v1.0.0 (2021-08-12)

### Refactor

- upgrade map_keys algorithm

### Feat

- translator service
