"""Repository base class for database operations."""

from typing import Any, TypeVar

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from pg_g4public_orm.core.base import DeclarativeBase

T = TypeVar("T", bound=DeclarativeBase)


class Repository[T: DeclarativeBase]:
    """Abstract base repository with common query methods."""

    def __init__(self, session: Session, model: type[T]) -> None:
        """Initialize repository with session and model.

        Args:
            session: SQLAlchemy session for database operations.
            model: ORM model class this repository manages.
        """
        self._session = session
        self._model = model

    def _execute_scalars(self, stmt: Select[tuple[T]]) -> list[T]:
        """Execute a typed SELECT and return ORM rows."""
        return list(self._session.execute(stmt).scalars().all())

    def get_by_id(self, id: int) -> T | None:
        """Fetch entity by primary key."""
        return self._session.get(self._model, id)

    def list_all(self, limit: int | None = None, offset: int = 0) -> list[T]:
        """List all entities with optional pagination."""
        stmt: Select[tuple[T]] = select(self._model).offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)

        return self._execute_scalars(stmt)

    def filter_by(self, **kwargs: Any) -> list[T]:
        """Filter entities by keyword arguments."""
        stmt: Select[tuple[T]] = select(self._model).filter_by(**kwargs)
        return self._execute_scalars(stmt)

    def add(self, entity: T) -> T:
        """Add entity to session without committing."""
        self._session.add(entity)
        return entity

    def save(self, entity: T) -> T:
        """Add entity to session without committing.

        The owning ``get_readwrite_session()`` context manager controls
        transaction boundaries (commit/rollback), so this repository remains
        commit-agnostic.
        """
        return self.add(entity)

    def delete(self, entity: T) -> None:
        """Stage entity deletion without committing."""
        self._session.delete(entity)
