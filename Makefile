.DEFAULT_GOAL := all
isort = isort annotated_types tests
black = black annotated_types tests

.PHONY: install
install:
	pip install -r tests/requirements.txt
	pip install -r tests/requirements-linting.txt
	poetry install
	pre-commit install

.PHONY: format
format:
	$(isort)
	$(black)

.PHONY: lint
lint:
	flake8 --max-complexity 10 --max-line-length 120 --ignore E203,W503 annotated_types tests
	$(isort) --check-only --df
	$(black) --check

.PHONY: test
test:
	coverage run -m pytest

.PHONY: testcov
testcov: test
	@coverage report --show-missing
	@coverage html

.PHONY: docs
docs:
	mkdocs build --strict

.PHONY: all
all: lint testcov docs

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
