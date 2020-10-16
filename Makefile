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
		@echo "  help - to show this message"
		@echo "  dist - to build the collection archive"
		@echo "  lint - to run code linting"

lint:
	flake8 phpypam

dist:
	python3 setup.py sdist bdist_wheel

check: dist
	$(TWINE_CMD) check dist/*

publish: check
	$(TWINE_CMD) upload $(TWINE_OPTIONS) dist/*

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

FORCE:

.PHONY: help dist lint publish FORCE
