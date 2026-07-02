"""Pytest configuration and fixtures for pg-g4public-orm tests."""

from collections.abc import Generator

import pytest

from pg_g4public_orm.core.session import close_all_sessions


@pytest.fixture(autouse=True)
def _reset_singletons() -> Generator[None]:
    """Reset the session-engine singletons before and after each test.

    The genew4-style session surface holds process-wide singletons
    (``_engine_factory`` / ``_session_factory`` / ``_global_settings``) that
    leak across tests when their configuration differs (e.g. per-test ``DB_*``
    env vars or ``.env`` files). Resetting them keeps every test isolated.

    This fixture fails fast if session imports break, so harness regressions are
    surfaced immediately instead of being silently skipped.
    """
    close_all_sessions()
    yield
    close_all_sessions()


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Automatically mark tests in tests/integration/ with the integration marker.

    This hook is called after test collection is complete.
    """
    for item in items:
        if "/integration/" in str(item.fspath) or "\\integration\\" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
