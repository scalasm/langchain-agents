# LangChain Agents - Workspace Instructions

AI coding assistant instructions for the LangChain agents learning and experimentation project.

## Project Overview

Modern Python 3.13+ project for learning and experimenting with LangChain agents. Emphasizes **type safety**, **code quality**, and **comprehensive testing** with a clean, maintainable architecture.

## Core Technologies

- **Python 3.13+** - Latest Python with modern syntax
- **UV** - Fast, reliable dependency and environment management (replaces pip/poetry)
- **Ruff** - Lightning-fast linting and formatting (replaces black/flake8/isort)
- **mypy** - Strict static type checking
- **pytest** - Testing framework with three-tier organization (unit/integration/e2e)
- **pre-commit** - Automated code quality checks
- **Typer** - CLI framework for command-line interfaces

## Essential Commands

### Build & Dependencies
```bash
uv sync                    # Install/sync dependencies from lockfile
uv add <package>           # Add new dependency
uv run <command>           # Run command in project venv (auto-activates)
```

### Development Workflow
```bash
make ci                    # Run ALL checks (what CI runs - do this before PRs!)
make format                # Auto-format code with ruff
make lint                  # Lint and auto-fix with ruff
make type-check            # Type check with mypy
make test-all              # Run all tests with coverage
make test-unit             # Run unit tests only
make coverage              # Generate detailed HTML coverage report
```

### Pre-commit
```bash
uv run pre-commit run --all-files    # Run all hooks manually
```
Note: Pre-commit hooks run automatically on `git commit` - they MUST pass before code can be committed.

## Code Quality Standards

### Type Hints (MANDATORY)
**All functions and methods MUST have complete type hints.** This is enforced by mypy with `disallow_untyped_defs = true`.

```python
# ✅ CORRECT
def process_items(items: list[str], limit: int = 10) -> dict[str, int]:
    """Process items and return counts."""
    return {item: len(item) for item in items[:limit]}

# ❌ WRONG - will fail mypy
def process_items(items, limit=10):
    return {item: len(item) for item in items[:limit]}
```

**Key type hinting rules:**
- Use built-in generics: `list[T]`, `dict[K, V]` (not `List`, `Dict` from typing)
- Explicit `None` return types: `-> None` for functions without return values
- Use `| None` instead of `Optional[T]` (Python 3.10+ style)
- Import from `collections.abc` for abstract types: `Sequence`, `Iterable`, `Mapping`

### Formatting & Linting
- **Line length:** 88 characters max
- **Quotes:** Double quotes (`"`) for strings
- **Import order:** Automatic via ruff's isort integration
- **All ruff rules are fixable** - run `make format` and `make lint` to auto-fix

### Code Style Principles
1. **No magic numbers** - Use named constants (ALL_CAPS)
2. **Explicit over implicit** - Clear variable/function names
3. **Type hints everywhere** - Function signatures must be typed
4. **Docstrings for public APIs** - Use Google-style docstrings
5. **DRY (Don't Repeat Yourself)** - Extract common patterns

## Testing Strategy

### Three-Tier Test Organization
```
tests/
├── unit/           # Fast, isolated, no external dependencies
├── integration/    # Requires local services (e.g., testcontainers)
└── e2e/            # Requires external services (OpenAI, AWS, etc.)
```

### Test Markers
Use pytest markers to categorize tests:
```python
@pytest.mark.unit          # Fast unit tests
@pytest.mark.integration   # Integration tests
@pytest.mark.e2e          # End-to-end tests
```

Run specific test categories:
```bash
uv run pytest -m unit              # Unit only
uv run pytest -m "not e2e"         # Everything except e2e
```

### Coverage Requirements
- **Minimum 80% coverage** enforced by CI
- Coverage reports: `htmlcov/index.html` (open in browser)
- Command: `make coverage` for detailed report

### Test Patterns
```python
from typer.testing import CliRunner

def test_cli_command(capsys: object) -> None:
    """Test CLI output using capsys fixture."""
    runner = CliRunner()
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.stdout
```

**Key fixtures:**
- `capsys` - Capture stdout/stderr
- `CliRunner` - Test Typer CLI applications
- `_reset_environment` - Auto-use fixture for test isolation (in conftest.py)

### Test Exemptions
Tests are exempt from:
- `disallow_untyped_defs` (mypy allows untyped test functions)
- Magic value rules (PLR2004), assert statements (S101), unused args (ARG)

## Project Structure

```
langchain-agents/
├── src/
│   └── my_langchain_agents/    # Main package (import as: from my_langchain_agents import ...)
│       ├── __init__.py
│       ├── hello_world.py      # Example: CLI demo with Typer
│       └── py.typed            # PEP 561 type stub marker
├── tests/
│   ├── conftest.py            # Shared fixtures and pytest configuration
│   ├── unit/                  # Unit tests (fast, isolated)
│   ├── integration/           # Integration tests (local services)
│   └── e2e/                   # End-to-end tests (external services)
├── docs/
│   └── CODING_CONVENTIONS.md  # Detailed coding standards
├── .github/
│   └── workflows/ci.yml       # CI/CD pipeline (runs on all PRs and main pushes)
├── pyproject.toml             # Project config, dependencies, tool settings
├── Makefile                   # Development commands
└── README.md
```

## Dependency Management with UV

UV is a **single tool** that replaces pip, virtualenv, and poetry:

### Key UV Commands
```bash
uv sync                        # Install deps from uv.lock (reproducible)
uv add <package>               # Add to dependencies
uv add --dev <package>         # Add to dev dependencies
uv run <command>               # Run in venv (no manual activation needed)
uv python install 3.13         # Install Python 3.13
```

### UV Workflow
1. **Never manually activate venv** - Use `uv run` prefix instead
2. **Lock file is committed** - `uv.lock` ensures reproducibility
3. **Fast installs** - UV is ~10-100x faster than pip
4. **Automatic venv creation** - `.venv/` created and managed automatically

## CI/CD Pipeline

**Runs on:** Every push to `main` + all pull requests

**Steps (must all pass):**
1. Code formatting check (`ruff format --check`)
2. Linting (`ruff check`)
3. Type checking (`mypy src/`)
4. **Unit tests** (always runs)
5. **Integration tests** (skips if no tests exist)
6. **E2E tests** (only on `main` branch pushes, skips if no tests exist)
7. **Coverage threshold check** (fails if <80%)

**Before submitting PRs:** Run `make ci` locally to catch issues early!

## Common Workflows

### Adding a New Feature
```bash
# 1. Create feature branch
git checkout -b feature/my-feature

# 2. Add dependencies if needed
uv add <package>

# 3. Write code with full type hints
# 4. Write tests (unit tests at minimum)
# 5. Run all checks
make ci

# 6. Commit (pre-commit hooks will run)
git add .
git commit -m "Add my feature"

# 7. Push and create PR
git push -u origin feature/my-feature
```

### Adding a New CLI Command
```python
# src/my_langchain_agents/my_command.py
import typer

app = typer.Typer()

@app.command()
def greet(name: str, loud: bool = False) -> None:
    """Greet someone by name."""
    message = f"Hello, {name}!"
    if loud:
        message = message.upper()
    typer.echo(message)

if __name__ == "__main__":
    app()
```

Register in `pyproject.toml`:
```toml
[project.scripts]
my-command = "my_langchain_agents.my_command:app"
```

Test with `uv run my-command --help`.

### Debugging Coverage Issues
```bash
# Generate detailed HTML report
make coverage

# Open report in browser
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux

# Look for red-highlighted lines (missing coverage)
# Add tests to cover those lines
```

## Common Pitfalls & Solutions

### ❌ Pitfall: Untyped function signatures
```python
def process(data):  # ❌ mypy will fail
    return data.upper()
```
**Solution:** Add type hints:
```python
def process(data: str) -> str:  # ✅
    return data.upper()
```

### ❌ Pitfall: Using old typing module generics
```python
from typing import List, Dict  # ❌ Deprecated style

def func(items: List[str]) -> Dict[str, int]:
    pass
```
**Solution:** Use built-in generics (Python 3.9+):
```python
def func(items: list[str]) -> dict[str, int]:  # ✅
    pass
```

### ❌ Pitfall: Running commands without `uv run`
```bash
pytest tests/  # ❌ May use wrong Python/venv
```
**Solution:** Always use `uv run`:
```bash
uv run pytest tests/  # ✅ Uses project venv
```

### ❌ Pitfall: Magic numbers in code
```python
if age >= 18:  # ❌ Magic number
    pass
```
**Solution:** Use named constants:
```python
LEGAL_AGE = 18

if age >= LEGAL_AGE:  # ✅
    pass
```

## Pre-commit Hooks Details

Hooks run automatically on commit (in order):
1. **ruff** - Lint and auto-fix violations
2. **ruff-format** - Format code
3. **mypy** - Type check `src/` directory (with typer dependency)
4. **trailing-whitespace** - Remove trailing spaces
5. **end-of-file-fixer** - Ensure newline at EOF
6. **check-yaml** - Validate YAML syntax
7. **check-toml** - Validate TOML syntax
8. **check-added-large-files** - Prevent large file commits
9. **check-merge-conflict** - Detect merge conflict markers
10. **debug-statements** - Detect leftover debug code

**If hooks fail:** Fix the issues and commit again. Most issues auto-fix (just re-stage and commit).

## Development Environment

### DevContainer Support
This project includes a `.devcontainer/` configuration for VS Code:
- Pre-configured Python 3.13 environment
- Docker Compose support (Docker-in-Docker)
- All tools pre-installed (UV, pre-commit, etc.)
- Automatic extension recommendations

Open in DevContainer: `Ctrl+Shift+P` → "Reopen in Container"

### Recommended VS Code Extensions
- Python (ms-python.python)
- Pylance (ms-python.vscode-pylance)
- Ruff (charliermarsh.ruff)
- GitHub Copilot (github.copilot)

## References

- **Detailed coding standards:** [docs/CODING_CONVENTIONS.md](docs/CODING_CONVENTIONS.md)
- **UV documentation:** https://docs.astral.sh/uv/
- **Ruff rules:** https://docs.astral.sh/ruff/rules/
- **pytest documentation:** https://docs.pytest.org/
- **Typer documentation:** https://typer.tiangolo.com/

---

**Quick Start for AI Agents:**
1. Use `uv run` prefix for all commands
2. Add type hints to everything (except test implementations)
3. Run `make format && make lint` before analysis/commits
4. Maintain 80%+ test coverage
5. Follow three-tier test structure (unit/integration/e2e)
6. Run `make ci` before creating PRs
