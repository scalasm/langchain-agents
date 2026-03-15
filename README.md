# LangChain Agents

[![CI](https://github.com/scalasm/langchain-agents/actions/workflows/ci.yml/badge.svg)](https://github.com/scalasm/langchain-agents/actions/workflows/ci.yml) [![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

A modern Python project for learning and experimenting with LangChain agents.

## Features

- **Modern Python 3.13** with full type hints
- **UV** for fast, reliable dependency management
- **Ruff** for linting and formatting (replaces black, flake8, isort)
- **mypy** for static type checking
- **pytest** with comprehensive test organization (unit/integration/e2e)
- **pre-commit** hooks for code quality
- **DevContainer** support with Docker-in-Docker
- **GitHub Actions** CI/CD pipeline

## Quick Start

### Prerequisites

- [UV](https://docs.astral.sh/uv/) installed
- Python 3.13+

### Installation

```bash
# Clone the repository
git clone https://github.com/scalasm/langchain-agents.git
cd langchain-agents

# Install dependencies (creates .venv automatically)
uv sync

# Activate the virtual environment (optional, uv run handles this)
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows
```

### Running the Demo CLI

```bash
# Using uv run (recommended)
uv run python -m my_langchain_agents.hello_world

# Or using the installed script
uv run hello

# Or if venv is activated
python -m my_langchain_agents.hello_world
```

## Development

### Available Make Targets

```bash
make help           # Show all available targets
make install        # Install dependencies
make format         # Format code with ruff
make lint           # Lint code with ruff
make type-check     # Type check with mypy
make test-unit      # Run unit tests
make test-integration  # Run integration tests
make test-e2e       # Run end-to-end tests
make test-all       # Run all tests
make coverage       # Generate coverage report
make ci             # Run all CI checks (format, lint, type-check, test)
make clean          # Remove build artifacts
```

### Running Tests

```bash
# Run all tests with coverage
make test-all

# Run specific test categories
make test-unit
make test-integration
make test-e2e

# Run tests with pytest directly
uv run pytest tests/unit/
uv run pytest -m unit
uv run pytest -m "not e2e"
```

### Code Quality

```bash
# Format code
make format

# Lint code
make lint

# Type check
make type-check

# Run all checks (what CI runs)
make ci
```

### Pre-commit Hooks

Pre-commit hooks are automatically installed in the devcontainer. To install manually:

```bash
uv run pre-commit install

# Run hooks on all files
uv run pre-commit run --all-files
```

## Project Structure

```
langchain-agents/
├── src/
│   └── my_langchain_agents/    # Main package
│       ├── __init__.py
│       ├── hello_world.py      # Demo CLI
│       └── py.typed            # PEP 561 marker
├── tests/
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests (local services)
│   └── e2e/                    # End-to-end tests (external services)
├── docs/
│   └── CODING_CONVENTIONS.md   # Coding standards
├── .devcontainer/              # VS Code devcontainer config
├── .github/
│   └── workflows/
│       └── ci.yml              # CI/CD pipeline
├── pyproject.toml              # Project configuration
├── Makefile                    # Development tasks
└── README.md
```

## Documentation

- [Coding Conventions](docs/CODING_CONVENTIONS.md)
- [Project Configuration](pyproject.toml)

## Testing Strategy

- **Unit Tests** (`tests/unit/`): Fast, isolated tests with no external dependencies
- **Integration Tests** (`tests/integration/`): Tests requiring local services (e.g., testcontainers)
- **E2E Tests** (`tests/e2e/`): Tests requiring external services (OpenAI, AWS, etc.)

Run tests by marker:
```bash
uv run pytest -m unit           # Unit tests only
uv run pytest -m integration    # Integration tests only
uv run pytest -m e2e            # E2E tests only
uv run pytest -m "not e2e"      # Everything except e2e
```

## CI/CD

The project uses GitHub Actions for CI/CD:

- **Pull Requests**: Runs linting, type checking, unit tests, and integration tests
- **Main Branch**: Runs all checks including e2e tests
- **Coverage**: Enforces 80% minimum coverage threshold

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

1. Create a feature branch
2. Make your changes
3. Run `make ci` to ensure all checks pass
4. Submit a pull request

## Repository

https://github.com/scalasm/langchain-agents
