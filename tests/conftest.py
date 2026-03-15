"""Shared test configuration and fixtures."""

import pytest


@pytest.fixture(autouse=True)
def _reset_environment() -> None:
    """Reset environment for each test.

    This fixture runs automatically before each test to ensure
    a clean testing environment.
    """
    # Add any cleanup or setup logic here


# Register custom markers
def pytest_configure(config: pytest.Config) -> None:
    """Register custom pytest markers.

    Args:
        config: Pytest configuration object.
    """
    config.addinivalue_line(
        "markers",
        "unit: Unit tests - fast, isolated tests with no external dependencies",
    )
    config.addinivalue_line(
        "markers",
        "integration: Integration tests - tests requiring local services (testcontainers)",
    )
    config.addinivalue_line(
        "markers",
        "e2e: End-to-end tests - tests requiring external services (OpenAI, AWS, etc.)",
    )
