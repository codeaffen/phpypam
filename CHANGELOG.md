# phpypam CHANGELOG

## Unreleased

### New

* add make target for setting up local test environment

  Add target ```setup-phpipam``` to setup a local test environment on an easy way.

### Changes

* Switch sphinx from recommonmark to myst_parser
* remove duplicated code from test cases
* Add ability to use ```podman``` if available on your system to spin up local test environment.

### Fixes
* \#57 - add headers parameter to methods create, update and delete
  * to modify the the output format header `Content-Type: application/xml` is needed
  * requests to `/addresses` endpoint needs sometimes `Content-Type: application/x-www-form-urlencoded` to work 

* \#51 - Subnet address search with zero results raises incorrect exception

  When searching for addresses in an empty subnet, ```PHPEntityNotFoundException``` will be raised.

### Breaks

## 1.0.2 - (2021-09-02)

---

### New

* add test cases to check PHPyPAMEntityNotFoundException

### Fixes

* fix #48 - raise PHPyPAMEntityNotFoundException if searching for non existing host

## 1.0.1 - (2021-01-04)

### New

* add markdownlint config
* add changelog

### Fixes

* fix exception handling for connection errors

## 1.0.0

### New

* documentation tool chain (#27)
* Merge pull request #28 from cmeissner/contributing\_and\_documentation

## 0.1.7

### Fixes

* We now should evaluate almost all not found messages and raise the correct Exception.

## 0.1.6

### New

* handle not found execption for vrf

## 0.1.5

### Fixes

* return controller paths not names

### Breakes

* returns controller paths not names

## 0.1.4

### New

* some project stuff

## 0.1.3

### Fixes

* fix typo

## 0.1.2

### New

* detailed exception handling

## 0.1.1

### Fixes

* Add exception handling for stupid error reporting of non existing subnets

## 0.1.0

### New

* First more or less productive release. Feel free to report bugs and issues

## 0.0.2

### Changes

* add controllers method
* add first simple tests
* extend documentation
