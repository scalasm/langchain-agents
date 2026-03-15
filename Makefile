.PHONY: help install format lint type-check test-unit test-integration test-e2e test-all coverage ci clean

help:
	@echo "Available targets:"
	@echo "  make install           - Install all dependencies with uv"
	@echo "  make format            - Format code with ruff"
	@echo "  make lint              - Lint code with ruff"
	@echo "  make type-check        - Type check with mypy"
	@echo "  make test-unit         - Run unit tests"
	@echo "  make test-integration  - Run integration tests"
	@echo "  make test-e2e          - Run end-to-end tests"
	@echo "  make test-all          - Run all tests"
	@echo "  make coverage          - Generate detailed coverage report"
	@echo "  make ci                - Run all CI checks (format-check, lint, type-check, test-all)"
	@echo "  make clean             - Remove build artifacts and caches"

install:
	uv sync

format:
	uv run ruff format .

format-check:
	uv run ruff format . --check

lint:
	uv run ruff check . --fix

lint-check:
	uv run ruff check .

type-check:
	uv run mypy src/

test-unit:
	uv run pytest tests/unit/ -v

test-integration:
	uv run pytest tests/integration/ -v

test-e2e:
	uv run pytest tests/e2e/ -v

test-all:
	uv run pytest tests/ -v

coverage:
	uv run pytest tests/ --cov=src/my_langchain_agents --cov-report=html --cov-report=term-missing --cov-report=xml
	@echo "Coverage report generated in htmlcov/index.html"

ci: format-check lint-check type-check test-all
	@echo "✅ All CI checks passed!"

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .mypy_cache/
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf coverage.xml
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
