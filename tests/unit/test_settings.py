"""Tests for ``pg_g4public_orm`` PostgreSQL ``DatabaseSettings``.

Following TDD: written FIRST, before implementation. These mirror
``vgnc_orm``'s settings tests but assert the **PostgreSQL** defaults mandated
by the spec (``postgresql+psycopg``, port ``5432``, database ``g4public``,
``DB_`` prefix, no charset effect).
"""

import os
from pathlib import Path

import db_common
import pytest


@pytest.fixture(autouse=True)
def _clean_db_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Clear ``DB_*`` env vars for each test and restore them afterwards."""
    for key in list(os.environ):
        if key.startswith("DB_"):
            monkeypatch.delenv(key, raising=False)


def test_database_settings_is_db_common_subclass(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """DatabaseSettings subclasses db_common.DatabaseSettings."""
    monkeypatch.chdir(tmp_path)
    from pg_g4public_orm.core.settings import DatabaseSettings

    assert issubclass(DatabaseSettings, db_common.DatabaseSettings)


def test_database_settings_postgresql_defaults(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Defaults are PostgreSQL: psycopg driver, port 5432, database g4public.

    Regression guard mirroring vgnc-orm: ``DatabaseSettings()`` must be
    instantiable with zero configuration and carry the PG defaults.
    """
    monkeypatch.chdir(tmp_path)
    from pg_g4public_orm.core.settings import DatabaseSettings

    settings = DatabaseSettings()

    assert settings.driver == "postgresql+psycopg"
    assert settings.get_url().drivername == "postgresql+psycopg"
    assert settings.port == 5432, "Default port should be 5432 (PostgreSQL)"
    assert settings.database == "g4public", "Default database should be g4public"
    assert settings.host == "localhost"
    assert settings.pool_size == 5
    assert settings.max_overflow == 10


def test_database_settings_db_prefix_env_override(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The ``DB_`` env prefix populates host/port/database/user/password."""
    monkeypatch.setenv("DB_HOST", "dbhost")
    monkeypatch.setenv("DB_PORT", "5433")
    monkeypatch.setenv("DB_NAME", "otherdb")
    monkeypatch.setenv("DB_USER", "dbuser")
    monkeypatch.setenv("DB_PASSWORD", "dbpass")

    from pg_g4public_orm.core.settings import DatabaseSettings

    settings = DatabaseSettings()

    assert settings.host == "dbhost"
    assert settings.port == 5433
    assert settings.database == "otherdb"
    assert settings.username == "dbuser"
    assert settings.password == "dbpass"


def test_database_settings_db_database_alias_works(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The ``DB_DATABASE`` alias (db-common canonical) also populates database."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("DB_DATABASE", "aliased")

    from pg_g4public_orm.core.settings import DatabaseSettings

    settings = DatabaseSettings()
    assert settings.database == "aliased"


def test_no_charset_effect_on_postgresql_url(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """PG ignores charset: the connection URL must not embed a charset.

    db-common carries an inert ``charset`` field for MySQL; for the
    ``postgresql+psycopg`` driver it must never reach the connection URL.
    """
    monkeypatch.chdir(tmp_path)
    from pg_g4public_orm.core.settings import DatabaseSettings

    settings = DatabaseSettings()
    url = settings.get_url().render_as_string(hide_password=False)

    assert (
        "charset" not in url.lower()
    ), f"PostgreSQL URL must not carry a charset query arg; got: {url}"


def test_sqlite_driver_builds_sqlite_url(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """driver='sqlite' yields an in-memory SQLite URL (used by unit tests)."""
    monkeypatch.chdir(tmp_path)
    from pg_g4public_orm.core.settings import DatabaseSettings

    settings = DatabaseSettings(driver="sqlite")
    assert settings.get_url().drivername == "sqlite"
    assert settings.get_url().database == ":memory:"


def test_database_settings_env_file_loading(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Settings load from a ``.env`` file in the working directory."""
    env_path = tmp_path / ".env"
    env_path.write_text(
        "DB_HOST=envfilehost\n"
        "DB_PORT=5544\n"
        "DB_NAME=envfileg4public\n"
        "DB_USER=envfileuser\n"
        "DB_PASSWORD=envfilepass\n"
    )
    monkeypatch.chdir(tmp_path)

    from pg_g4public_orm.core.settings import DatabaseSettings

    settings = DatabaseSettings()

    assert settings.host == "envfilehost"
    assert settings.port == 5544
    assert settings.database == "envfileg4public"


def test_database_settings_exposed_at_package_root() -> None:
    """``import pg_g4public_orm`` exposes ``DatabaseSettings``."""
    import pg_g4public_orm

    assert hasattr(pg_g4public_orm, "DatabaseSettings")
    assert pg_g4public_orm.DatabaseSettings is not None


def test_url_property_hides_password() -> None:
    """``settings.url`` must never expose the plaintext DB password.

    Guards against a credential leak if a consumer logs or prints the URL.
    The full credential-bearing URL remains available via ``get_url()`` for
    engine construction.
    """
    from pg_g4public_orm.core.settings import DatabaseSettings

    settings = DatabaseSettings(
        username="leakcheck", password="SUPERSECRET", host="db", database="g4public"
    )

    rendered = settings.url

    assert (
        "SUPERSECRET" not in rendered
    ), f"settings.url leaked the password: {rendered!r}"
    assert settings.password == "SUPERSECRET"  # the real value is still present
    # And the credential-bearing URL is still reachable via get_url().
    assert "SUPERSECRET" in settings.get_url().render_as_string(hide_password=False)
