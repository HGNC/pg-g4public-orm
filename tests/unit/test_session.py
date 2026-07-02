"""Tests for the db-common session module-function surface (SQLite — no DB).

The additive module-function surface in ``pg_g4public_orm.core.session`` —
``initialize_engine`` / ``get_engine`` / ``get_settings`` /
``get_readwrite_session`` / ``get_readonly_session`` / ``close_all_sessions`` /
``refresh_engine`` — delegates to ``db_common.EngineFactory`` /
``db_common.SessionFactory``. These tests exercise that surface against an
in-memory SQLite engine so no PostgreSQL server is required.

This package has no audit layer, so the read-write session takes no ``user``
argument and never populates ``session.info`` — these tests assert only the
commit/rollback and read-only-rejection contract.
"""

from contextlib import contextmanager

import db_common
import pytest
from sqlalchemy import text


@contextmanager
def _preserve_session_state():
    """Snapshot and restore the module-level session singletons.

    ``initialize_engine`` / ``close_all_sessions`` mutate the process-wide
    ``_engine_factory`` / ``_session_factory`` / ``_global_settings``
    singletons. Restoring them keeps this test module isolated from siblings.
    """
    from pg_g4public_orm.core import session as session_module

    saved = (
        session_module._engine_factory,
        session_module._session_factory,
        session_module._global_settings,
    )
    try:
        yield session_module
    finally:
        # Dispose whatever engine the test created before restoring the
        # snapshot, so in-memory SQLite engines are not leaked to process exit.
        from pg_g4public_orm.core.session import close_all_sessions

        close_all_sessions()
        (
            session_module._engine_factory,
            session_module._session_factory,
            session_module._global_settings,
        ) = saved


def _sqlite_settings():
    """Return a SQLite ``DatabaseSettings`` (no PostgreSQL server required)."""
    from pg_g4public_orm.core.settings import DatabaseSettings

    return DatabaseSettings(driver="sqlite")


class TestReExports:
    """The public exception names are db-common's classes by identity."""

    def test_readonly_session_error_is_db_common(self) -> None:
        from pg_g4public_orm.core.session import ReadOnlySessionError

        assert ReadOnlySessionError is db_common.ReadOnlySessionError

    def test_session_error_is_db_common(self) -> None:
        from pg_g4public_orm.core.session import SessionError

        assert SessionError is db_common.SessionError


class TestHealthCheck:
    """initialize_engine(DatabaseSettings(driver='sqlite')) yields a healthy engine."""

    def test_sqlite_engine_is_healthy(self) -> None:
        from pg_g4public_orm.core.session import initialize_engine

        with _preserve_session_state():
            engine = initialize_engine(_sqlite_settings())
            assert db_common.health_check(engine) is True


class TestNotInitialized:
    """Before initialize_engine, the getters raise SessionError."""

    def test_get_engine_raises_before_init(self) -> None:
        from pg_g4public_orm.core.session import SessionError, get_engine

        with _preserve_session_state():
            with pytest.raises(SessionError):
                get_engine()

    def test_get_settings_raises_before_init(self) -> None:
        from pg_g4public_orm.core.session import SessionError, get_settings

        with _preserve_session_state():
            with pytest.raises(SessionError):
                get_settings()


class TestInitializeEngine:
    """initialize_engine builds the engine via db_common.EngineFactory."""

    def test_returns_sqlite_engine(self) -> None:
        from pg_g4public_orm.core.session import initialize_engine

        with _preserve_session_state():
            engine = initialize_engine(_sqlite_settings())
            assert engine is not None
            assert engine.url.drivername == "sqlite"

    def test_idempotent_returns_same_engine(self) -> None:
        from pg_g4public_orm.core.session import initialize_engine

        with _preserve_session_state():
            engine1 = initialize_engine(_sqlite_settings())
            engine2 = initialize_engine()  # no settings -> reuses cached engine
            assert engine1 is engine2

    def test_get_settings_returns_initialized_settings(self) -> None:
        from pg_g4public_orm.core.session import get_settings, initialize_engine

        with _preserve_session_state():
            settings = _sqlite_settings()
            initialize_engine(settings)
            assert get_settings() is settings


class TestReadWriteSession:
    """get_readwrite_session commits on clean exit, rolls back on exception."""

    def test_select_one(self) -> None:
        from pg_g4public_orm.core.session import (
            get_readwrite_session,
            initialize_engine,
        )

        with _preserve_session_state():
            initialize_engine(_sqlite_settings())
            with get_readwrite_session() as session:
                assert session.execute(text("SELECT 1")).scalar() == 1

    def test_insert_commits_on_clean_exit(self) -> None:
        from pg_g4public_orm.core.session import (
            get_readwrite_session,
            initialize_engine,
        )

        with _preserve_session_state():
            initialize_engine(_sqlite_settings())
            # Create a table and insert inside a read-write session, then exit clean.
            with get_readwrite_session() as session:
                session.execute(
                    text(
                        "CREATE TABLE t_rw (id INTEGER PRIMARY KEY, name TEXT NOT NULL)"
                    )
                )
                session.execute(text("INSERT INTO t_rw (name) VALUES ('alice')"))
            # A subsequent session must see the committed row.
            with get_readwrite_session() as session:
                count = session.execute(
                    text("SELECT COUNT(*) FROM t_rw WHERE name = 'alice'")
                ).scalar()
                assert count == 1


class TestReadOnlySession:
    """get_readonly_session rejects commits but allows reads."""

    def test_commit_raises_readonly_session_error(self) -> None:
        from pg_g4public_orm.core.session import (
            ReadOnlySessionError,
            get_readonly_session,
            initialize_engine,
        )

        with _preserve_session_state():
            initialize_engine(_sqlite_settings())
            with pytest.raises(ReadOnlySessionError):
                with get_readonly_session() as session:
                    session.execute(text("SELECT 1"))
                    session.commit()

    def test_allows_reads(self) -> None:
        from pg_g4public_orm.core.session import (
            get_readonly_session,
            initialize_engine,
        )

        with _preserve_session_state():
            initialize_engine(_sqlite_settings())
            with get_readonly_session() as session:
                assert session.execute(text("SELECT 1")).scalar() == 1


class TestCloseAndRefresh:
    """close_all_sessions resets state; refresh_engine rebuilds the engine."""

    def test_close_resets_singletons(self) -> None:
        from pg_g4public_orm.core.session import (
            close_all_sessions,
            initialize_engine,
        )

        with _preserve_session_state() as session_module:
            initialize_engine(_sqlite_settings())
            assert session_module._engine_factory is not None
            close_all_sessions()
            assert session_module._engine_factory is None
            assert session_module._session_factory is None
            assert session_module._global_settings is None

    def test_refresh_engine_returns_engine(self) -> None:
        from pg_g4public_orm.core.session import (
            initialize_engine,
            refresh_engine,
        )

        with _preserve_session_state():
            initialize_engine(_sqlite_settings())
            new_engine = refresh_engine()
            assert new_engine is not None
            assert new_engine.url.drivername == "sqlite"
