ifndef PHPIPAM_VALIDATE_CERTS
override PHPIPAM_VALIDATE_CERTS = true
endif

ifdef PYPI_REPO
TWINE_OPTIONS = --repository $(PYPI_REPO)
endif

ifdef PYPI_API_TOKEN
TWINE_OPTIONS += --username __token__ --password $(PYPI_API_TOKEN)
endif

ifdef PYPI_DRY_RUN
TWINE_CMD = echo twine
else
TWINE_CMD = twine
endif

default: help

help:
	@echo "Please use \`make <target>' where <target> is one of:"
		@echo "  help 			- to show this message"
		@echo "  dist 			- to build the collection archive"
		@echo "  lint 			- to run code linting"
		@echo "  clean			- clean workspace"
		@echo "  doc-setup		- prepare environment for creating documentation"
		@echo "  docs 			- create documentation"
		@echo "  test-setup		- prepare environment for tests"
		@echo "  test-all		- run all tests"
		@echo "  test-<test>		- run a specifig test"
		@echo "  coverage		- display code coverage"
		@echo "  coverage-xml		- create xml coverage report"

lint:
	flake8 phpypam

dist:
	python3 setup.py sdist bdist_wheel

check: dist
	$(TWINE_CMD) check dist/*

publish: check
	$(TWINE_CMD) upload $(TWINE_OPTIONS) dist/*

clean:
	rm -Rf docs/{build,_build} {build,dist} *.egg-info coverage.xml .pytest_cache
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +
	coverage erase

doc-setup:
	pip install --upgrade -r docs/requirements.txt

doc:
	install -d -m 750 ./docs/plugins
	sphinx-apidoc -M -f -o docs/plugins/ phpypam
	make -C docs html

test-setup: | tests/vars/server.yml
	pip install --upgrade -r requirements-dev.txt

tests/vars/server.yml:
	sed -e "s#~~url~~#$(PHPIPAM_URL)#" -e "s#~~app_id~~#$(PHPIPAM_APPID)#" -e "s#~~username~~#$(PHPIPAM_USERNAME)#" -e "s#~~password~~#$(PHPIPAM_PASSWORD)#" -e "s#~~ssl_verify~~#$(PHPIPAM_VALIDATE_CERTS)#" $@.example > $@

test-all:
	coverage run -m pytest tests/test_cases/* -v

test-%:
	coverage run -m pytest tests/test_cases/$*.py -v

coverage: test-all
	coverage report -m --include 'phpypam/*','phpypam/**/*','tests/**/*'

coverage-xml: test-all
	coverage xml --include 'phpypam/*','phpypam/**/*','tests/**/*'

FORCE:

.PHONY: help dist lint publish FORCE
