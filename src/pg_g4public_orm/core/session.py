"""SQLAlchemy session management (module-function style over db-common).

The public surface — :func:`initialize_engine`, :func:`get_engine`,
:func:`get_settings`, :func:`get_readwrite_session`,
:func:`get_readonly_session`, :func:`close_all_sessions`,
:func:`refresh_engine` — delegates engine/session creation to
``db_common.EngineFactory`` / ``db_common.SessionFactory``. Read-write sessions
commit on clean exit and roll back on exception; read-only sessions raise
:class:`ReadOnlySessionError` on commit. The "not initialized" errors collapse
onto :class:`SessionError` (a ``db_common.DatabaseError`` subclass).

``ReadOnlySessionError`` / ``SessionError`` are re-exported from ``db_common``
so the public symbol names are stable.

This package has no audit layer, so (unlike genew4) the session wrappers do not
populate ``session.info``.
"""

from collections.abc import Generator
from contextlib import contextmanager

import db_common
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from pg_g4public_orm.core.settings import DatabaseSettings

# -- db-common exception re-exports (public names) ---------------------------
# ReadOnlySessionError / SessionError are re-exported from db-common so the
# public symbol names are stable; the "not initialized" errors collapse onto
# SessionError.
ReadOnlySessionError = db_common.ReadOnlySessionError
SessionError = db_common.SessionError

# -- Module-level singletons ------------------------------------------------
# Created by initialize_engine and reset by close_all_sessions. Tests
# save/restore these to isolate state.
_engine_factory: db_common.EngineFactory | None = None
_session_factory: db_common.SessionFactory | None = None
_global_settings: DatabaseSettings | None = None


def initialize_engine(settings: DatabaseSettings | None = None) -> Engine:
    """Initialize the global database engine.

    Builds and caches the ``EngineFactory`` / ``SessionFactory`` singletons.
    Idempotent: a second call returns the already-cached engine.

    Args:
        settings: Optional :class:`DatabaseSettings`. If ``None``, loads from
            environment via ``DatabaseSettings()``.

    Returns:
        The initialized SQLAlchemy :class:`~sqlalchemy.engine.Engine`.
    """
    global _engine_factory, _session_factory, _global_settings

    if _engine_factory is not None:
        return _engine_factory.get_engine()

    if settings is None:
        settings = DatabaseSettings()

    _global_settings = settings
    _engine_factory = db_common.EngineFactory(settings)
    _session_factory = db_common.SessionFactory(_engine_factory)

    return _engine_factory.get_engine()


def get_engine() -> Engine:
    """Get the global database engine.

    Returns:
        The SQLAlchemy :class:`~sqlalchemy.engine.Engine` instance.

    Raises:
        SessionError: If the engine has not been initialized.
    """
    if _engine_factory is None:
        raise SessionError(
            "Database engine not initialized. Call initialize_engine() first."
        )
    return _engine_factory.get_engine()


def get_settings() -> DatabaseSettings:
    """Get the global database settings.

    Returns:
        The :class:`DatabaseSettings` instance.

    Raises:
        SessionError: If settings have not been initialized.
    """
    if _global_settings is None:
        raise SessionError(
            "Database settings not initialized. Call initialize_engine() first."
        )
    return _global_settings


def _require_session_factory() -> db_common.SessionFactory:
    """Return the global SessionFactory, raising SessionError if uninitialized.

    Shared by :func:`get_readwrite_session` and :func:`get_readonly_session`,
    which both need the factory (and both surface the same "engine not
    initialized" error when it is absent).
    """
    if _session_factory is None:
        raise SessionError(
            "Database engine not initialized. Call initialize_engine() first."
        )
    return _session_factory


@contextmanager
def get_readwrite_session() -> Generator[Session]:
    """Create a session for read-write operations.

    The session is obtained from db-common's
    :meth:`db_common.SessionFactory.get_session`, which commits on clean exit
    and rolls back on exception. This package has no audit layer, so no
    ``session.info`` is populated.

    Yields:
        A SQLAlchemy :class:`~sqlalchemy.orm.Session`.

    Example:
        >>> with get_readwrite_session() as session:
        ...     gene = session.get(SomeModel, 1)
    """
    session_factory = _require_session_factory()
    with session_factory.get_session() as session:
        yield session


@contextmanager
def get_readonly_session() -> Generator[Session]:
    """Create a read-only session for database queries.

    The session is obtained from db-common's
    :meth:`db_common.SessionFactory.get_readonly_session`, whose
    ``before_commit`` hook raises :class:`ReadOnlySessionError` on any commit
    attempt. This package has no audit layer, so no ``session.info`` is
    populated.

    Yields:
        A SQLAlchemy :class:`~sqlalchemy.orm.Session` for read-only database
        operations.

    Raises:
        ReadOnlySessionError: If a commit is attempted.
    """
    session_factory = _require_session_factory()
    with session_factory.get_readonly_session() as session:
        yield session


def close_all_sessions() -> None:
    """Close all database sessions and dispose of the engine.

    Resets the module-level ``EngineFactory`` / ``SessionFactory`` singletons so
    the next :func:`initialize_engine` call rebuilds them. Safe to call when
    already uninitialized.
    """
    global _engine_factory, _session_factory, _global_settings

    if _session_factory is not None:
        _session_factory.close_all_sessions()

    if _engine_factory is not None:
        _engine_factory.dispose()

    _engine_factory = None
    _session_factory = None
    _global_settings = None


def refresh_engine() -> Engine:
    """Recreate the database engine with the current settings.

    Useful when database configuration has changed and a reconnect with new
    parameters is required.

    Returns:
        The newly created SQLAlchemy :class:`~sqlalchemy.engine.Engine`.

    Raises:
        SessionError: If no settings are available (engine was never
            initialized).
    """
    if _global_settings is None:
        raise SessionError("Cannot refresh: no settings available.")

    # Capture settings before close_all_sessions clears the singleton.
    settings = _global_settings
    close_all_sessions()
    return initialize_engine(settings)
