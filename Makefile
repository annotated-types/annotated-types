.DEFAULT_GOAL := all
paths = annotated_types tests

.PHONY: install
install:
	pip install -r requirements/all.txt
	pre-commit install

.PHONY: generate-dependencies
generate-dependencies:
	pip-compile --output-file=requirements/all.txt --resolver=backtracking requirements/all.in

.PHONY: format
format:
	isort $(paths)
	black $(paths)

.PHONY: lint
lint:
	flake8 $(paths)
	isort $(paths) --check-only --df
	black $(paths) --check

.PHONY: test
test:
	coverage run -m pytest

.PHONY: testcov
testcov: test
	@coverage report --show-missing
	@coverage html

.PHONY: mypy
mypy:
	mypy annotated_types tests

.PHONY: all
all: lint mypy testcov

.PHONY: clean
clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -rf .cache
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf *.egg-info
	rm -f .coverage
	rm -f .coverage.*
	rm -rf build
