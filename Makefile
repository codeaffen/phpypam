default: help

help:
	@echo "Please use \`make <target>' where <target> is one of:"
		@echo "  help - to show this message"
		@echo "  dist - to build the collection archive"
		@echo "  lint - to run code linting"

lint:
	flake8 pyhpipam

dist:
	python3 setup.py sdist bdist_wheel

publis:
	python3 -m twine upload --repository testpypi dist/*

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
