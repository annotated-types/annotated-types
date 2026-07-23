.DEFAULT_GOAL := all
paths = annotated_types tests

.PHONY: install
install:
	uv sync
	uv run pre-commit install

.PHONY: format
format:
	uv run isort $(paths)
	uv run black $(paths)

.PHONY: lint
lint:
	uv run flake8 $(paths)
	uv run isort $(paths) --check-only --df
	uv run black $(paths) --check

.PHONY: test
test:
	uv run coverage run -m pytest

.PHONY: testcov
testcov: test
	@uv run coverage report --show-missing
	@uv run coverage html

.PHONY: mypy
mypy:
	uv run mypy annotated_types tests

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
