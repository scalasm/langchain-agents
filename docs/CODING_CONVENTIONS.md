# Python Coding Conventions

This document outlines the coding standards and best practices for the LangChain Agents project.

## General Principles

- **Readability counts**: Code is read more often than written
- **Explicit is better than implicit**: Be clear in your intentions
- **Simple is better than complex**: Favor straightforward solutions
- **Consistency matters**: Follow established patterns in the codebase

## Type Hints

### Mandatory Usage

Type hints are **required** for all function and method signatures.

```python
# ✅ Good
def process_data(items: list[str], limit: int = 10) -> dict[str, int]:
    """Process a list of items."""
    return {item: len(item) for item in items[:limit]}

# ❌ Bad
def process_data(items, limit=10):
    return {item: len(item) for item in items[:limit]}
```

### Type Hint Best Practices

- Use built-in generic types from Python 3.9+ (`list`, `dict`, `set`, `tuple`)
- Import typing constructs only when needed (`Optional`, `Union`, `Protocol`, etc.)
- Use `None` return type explicitly when functions don't return values
- Prefer `Sequence` for read-only iterables, `Iterable` for one-time iteration
- Use `TypeVar` for generic functions

```python
from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")

def first_item(items: Sequence[T]) -> T | None:
    """Return the first item or None if empty."""
    return items[0] if items else None
```

## No Magic Numbers or Literals

### Use Named Constants

Define constants at module level with UPPER_CASE names.

```python
# ✅ Good
DEFAULT_TIMEOUT_SECONDS = 30
MAX_RETRY_ATTEMPTS = 3
API_BASE_URL = "https://api.example.com"

def fetch_data(timeout: int = DEFAULT_TIMEOUT_SECONDS) -> dict:
    """Fetch data with configurable timeout."""
    ...

# ❌ Bad
def fetch_data(timeout: int = 30) -> dict:
    if retry_count > 3:  # What does 3 mean here?
        raise TimeoutError()
```

### Configuration Values

For complex configuration, use dataclasses or Pydantic models.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class APIConfig:
    """API configuration settings."""

    base_url: str = "https://api.example.com"
    timeout_seconds: int = 30
    max_retries: int = 3
    retry_backoff_factor: float = 2.0
```

## Naming Conventions

### Functions and Variables

- Use `snake_case` for functions, methods, and variables
- Choose descriptive, meaningful names
- Avoid single-letter names except for counters and comprehensions

```python
# ✅ Good
def calculate_total_cost(items: list[Item]) -> Decimal:
    """Calculate the total cost of items."""
    total_amount = sum(item.price for item in items)
    return total_amount

# ❌ Bad
def calc(x: list) -> Decimal:
    t = sum(i.p for i in x)
    return t
```

### Classes

- Use `PascalCase` for class names
- Use descriptive nouns
- Suffix exceptions with `Error`

```python
# ✅ Good
class UserAccount:
    """Represents a user account."""
    pass

class ValidationError(Exception):
    """Raised when validation fails."""
    pass

# ❌ Bad
class user_account:
    pass

class ValidateFail(Exception):
    pass
```

### Constants

- Use `UPPER_CASE_WITH_UNDERSCORES`
- Define at module level

```python
# ✅ Good
MAX_CONNECTIONS = 100
API_VERSION = "v1"
DEFAULT_ENCODING = "utf-8"
```

### Private Members

- Prefix with single underscore for internal use
- Use double underscore only for name mangling (rare)

```python
class DataProcessor:
    """Process data with internal state."""

    def __init__(self) -> None:
        self._cache: dict[str, Any] = {}  # Internal use
        self.__secret = "value"  # Name mangling (rare)

    def _internal_helper(self) -> None:
        """Internal helper method."""
        pass
```

## Docstrings

### Google Style

Use Google-style docstrings for all public APIs.

```python
def fetch_user_data(
    user_id: str,
    include_metadata: bool = False,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    """Fetch user data from the API.

    Retrieves comprehensive user information including profile data
    and optionally metadata about account creation and activity.

    Args:
        user_id: Unique identifier for the user.
        include_metadata: Whether to include account metadata.
        timeout: Request timeout in seconds.

    Returns:
        Dictionary containing user data with keys 'profile', 'email',
        and optionally 'metadata'.

    Raises:
        ValueError: If user_id is empty or invalid.
        TimeoutError: If the request exceeds the timeout.
        APIError: If the API returns an error response.

    Examples:
        >>> data = fetch_user_data("user123")
        >>> print(data['email'])
        'user@example.com'
    """
    ...
```

### When to Document

- **Always**: Public functions, classes, and methods
- **Consider**: Complex private functions
- **Skip**: Trivial getters/setters, obvious helper functions

## Import Organization

### Order and Grouping

Organize imports in three groups, separated by blank lines:

1. Standard library imports
2. Third-party imports
3. Local application imports

Ruff's isort integration handles this automatically.

```python
# Standard library
import os
import sys
from pathlib import Path
from typing import Any

# Third-party
import httpx
import typer
from pydantic import BaseModel

# Local
from my_langchain_agents.config import settings
from my_langchain_agents.models import User
```

### Import Style

- Prefer absolute imports over relative imports
- Import modules, not individual names (exceptions for commonly used types)
- Use `from X import Y` for frequently used items

```python
# ✅ Good
from pathlib import Path
import my_langchain_agents.processors as processors

# Also acceptable for typing
from typing import Any, Protocol

# ❌ Avoid relative imports in application code
from ..models import User  # Use absolute import instead
```

## Error Handling

### Explicit Exception Types

Always catch specific exception types, never bare `except:`.

```python
# ✅ Good
try:
    data = fetch_data()
except (httpx.TimeoutError, httpx.ConnectionError) as e:
    logger.error(f"Network error: {e}")
    raise APIError("Failed to fetch data") from e
except ValueError as e:
    logger.warning(f"Invalid data format: {e}")
    return None

# ❌ Bad
try:
    data = fetch_data()
except:  # Too broad!
    return None
```

### Custom Exceptions

Define custom exceptions for domain-specific errors.

```python
class AgentError(Exception):
    """Base exception for agent-related errors."""
    pass

class AgentConfigurationError(AgentError):
    """Raised when agent configuration is invalid."""
    pass

class AgentExecutionError(AgentError):
    """Raised when agent execution fails."""
    pass
```

### Error Context

Use `raise ... from` to preserve exception context.

```python
# ✅ Good
try:
    config = load_config(path)
except FileNotFoundError as e:
    raise ConfigurationError(f"Config file not found: {path}") from e

# ❌ Bad
try:
    config = load_config(path)
except FileNotFoundError:
    raise ConfigurationError(f"Config file not found: {path}")  # Lost context!
```

## Testing

### Test Organization

- One test file per module: `test_<module>.py`
- One test class per class under test (optional)
- One assertion per test when practical

```python
# tests/unit/test_processor.py
import pytest
from my_langchain_agents.processor import DataProcessor

class TestDataProcessor:
    """Tests for DataProcessor class."""

    def test_process_valid_data_returns_result(self) -> None:
        """Test that valid data is processed correctly."""
        processor = DataProcessor()
        result = processor.process({"key": "value"})
        assert result == {"key": "VALUE"}

    def test_process_empty_data_raises_error(self) -> None:
        """Test that empty data raises ValueError."""
        processor = DataProcessor()
        with pytest.raises(ValueError, match="Data cannot be empty"):
            processor.process({})
```

### Test Naming

Use descriptive test names following the pattern:
`test_<what>_<condition>_<expected_result>`

```python
# ✅ Good
def test_user_creation_with_valid_email_succeeds() -> None:
    ...

def test_user_creation_with_invalid_email_raises_validation_error() -> None:
    ...

# ❌ Bad
def test_user() -> None:
    ...

def test1() -> None:
    ...
```

### Fixtures and Test Data

Use fixtures for shared test data and setup.

```python
import pytest
from my_langchain_agents.models import User

@pytest.fixture
def sample_user() -> User:
    """Provide a sample user for testing."""
    return User(
        id="user123",
        email="test@example.com",
        name="Test User",
    )

def test_user_email_validation(sample_user: User) -> None:
    """Test user email validation."""
    assert sample_user.email.endswith("@example.com")
```

## Code Style

### Line Length

Maximum line length is 88 characters (Black/Ruff default).

### String Quotes

Use double quotes by default (enforced by Ruff formatter).

```python
# ✅ Good
name = "Alice"
message = "Hello, world!"

# Use single quotes only when avoiding escape
message_with_quote = 'He said "Hello"'
```

### List Comprehensions

Prefer comprehensions for simple transformations, but maintain readability.

```python
# ✅ Good - simple and clear
squares = [x**2 for x in range(10)]
active_users = [u for u in users if u.is_active]

# ✅ Also good - complex logic deserves a loop
results = []
for item in items:
    processed = item.process()
    if processed.is_valid():
        results.append(processed.transform())

# ❌ Bad - too complex for comprehension
results = [
    item.process().transform()
    for item in items
    if item.process().is_valid() and item.created > cutoff
]
```

### Function Length

Keep functions focused and reasonably short (generally under 50 lines).

## Path Handling

Use `pathlib.Path` instead of string manipulation.

```python
from pathlib import Path

# ✅ Good
config_dir = Path("config")
config_file = config_dir / "settings.yaml"
if config_file.exists():
    content = config_file.read_text()

# ❌ Bad
import os
config_file = os.path.join("config", "settings.yaml")
if os.path.exists(config_file):
    with open(config_file) as f:
        content = f.read()
```

## Logging

Use structured logging with appropriate levels.

```python
import logging

logger = logging.getLogger(__name__)

def process_request(request_id: str) -> None:
    """Process an incoming request."""
    logger.info("Processing request", extra={"request_id": request_id})

    try:
        result = perform_operation()
        logger.debug("Operation completed", extra={"result": result})
    except Exception as e:
        logger.error(
            "Operation failed",
            extra={"request_id": request_id, "error": str(e)},
            exc_info=True,
        )
        raise
```

## Summary Checklist

- [ ] All functions have type hints
- [ ] No magic numbers or string literals
- [ ] Descriptive variable and function names (snake_case)
- [ ] Class names use PascalCase
- [ ] Public APIs have Google-style docstrings
- [ ] Imports organized (stdlib, third-party, local)
- [ ] Specific exception types (no bare `except:`)
- [ ] Tests have descriptive names
- [ ] Code formatted with Ruff
- [ ] Type checked with mypy
