.DEFAULT_GOAL := all
paths = annotated_types tests

.PHONY: install
install:
	uv sync
	uv run pre-commit install

.PHONY: format
format:
	uv run ruff format $(paths)
	uv run ruff check --fix $(paths)

.PHONY: lint
lint:
	uv run ruff format --check $(paths)
	uv run ruff check $(paths)

.PHONY: test
test:
	uv run coverage run -m pytest

.PHONY: testcov
testcov: test
	@uv run coverage report --show-missing
	@uv run coverage html

.PHONY: typecheck
typecheck:
	uv run ty check annotated_types tests

.PHONY: all
all: lint typecheck testcov

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
