"""Tests for the generic ``Repository[T]`` CRUD base.

These tests use a mocked SQLAlchemy ``Session`` (stdlib ``unittest.mock``)
and assert repository methods route through the expected session APIs while
remaining commit-agnostic.
"""

from unittest.mock import MagicMock

from sqlalchemy.orm import Mapped, Session, mapped_column

from pg_g4public_orm.core.base import DeclarativeBase
from pg_g4public_orm.repositories.base import Repository


class RepoModel(DeclarativeBase):
    """Minimal mapped model for repository unit tests."""

    __tablename__ = "test_model_repository"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str | None] = mapped_column(nullable=True)
    active: Mapped[bool | None] = mapped_column(nullable=True)


def _make_repo() -> tuple[MagicMock, Repository[RepoModel]]:
    """Create a repository wired to a mocked ``Session``."""
    session = MagicMock(spec=Session)
    return session, Repository(session, RepoModel)


def _mock_execute_result(items: list[RepoModel]) -> MagicMock:
    """Build a ``Session.execute`` mock result with scalar rows."""
    result = MagicMock()
    result.scalars.return_value.all.return_value = items
    return result


def test_get_by_id_routes_through_session_get() -> None:
    """``get_by_id`` must call ``session.get(model, id)``."""
    session, repo = _make_repo()

    value = repo.get_by_id(123)

    session.get.assert_called_once_with(RepoModel, 123)
    assert value is session.get.return_value


def test_list_all_routes_through_execute_with_limit_and_offset() -> None:
    """``list_all(limit, offset)`` must issue a SELECT via ``session.execute``."""
    session, repo = _make_repo()
    expected = [RepoModel(id=1)]
    session.execute.return_value = _mock_execute_result(expected)

    rows = repo.list_all(limit=10, offset=5)

    assert rows == expected
    session.execute.assert_called_once()
    stmt = session.execute.call_args.args[0]

    assert stmt.column_descriptions[0]["entity"] is RepoModel
    sql = str(stmt.compile(compile_kwargs={"literal_binds": True}))
    assert "FROM test_model_repository" in sql
    assert "LIMIT 10" in sql
    assert "OFFSET 5" in sql


def test_filter_by_routes_through_execute_with_kwargs() -> None:
    """``filter_by`` must issue a filtered SELECT via ``session.execute``."""
    session, repo = _make_repo()
    expected = [RepoModel(id=2)]
    session.execute.return_value = _mock_execute_result(expected)

    rows = repo.filter_by(name="test", active=True)

    assert rows == expected
    session.execute.assert_called_once()
    stmt = session.execute.call_args.args[0]

    assert stmt.column_descriptions[0]["entity"] is RepoModel
    sql = str(stmt.compile(compile_kwargs={"literal_binds": True}))
    assert "test_model_repository.name = 'test'" in sql
    assert "test_model_repository.active = true" in sql


def test_add_calls_session_add_and_returns_entity() -> None:
    """``add`` must call ``session.add`` and return the same entity."""
    session, repo = _make_repo()
    entity = RepoModel(id=7)

    returned = repo.add(entity)

    session.add.assert_called_once_with(entity)
    assert returned is entity


def test_save_is_commit_agnostic_and_stages_entity() -> None:
    """``save`` must stage entity via ``add`` and never call ``commit``."""
    session, repo = _make_repo()
    entity = RepoModel(id=8)

    returned = repo.save(entity)

    session.add.assert_called_once_with(entity)
    session.commit.assert_not_called()
    assert returned is entity


def test_delete_calls_session_delete_without_committing() -> None:
    """``delete`` must call ``session.delete`` and not call ``commit``."""
    session, repo = _make_repo()
    entity = RepoModel(id=9)

    repo.delete(entity)

    session.delete.assert_called_once_with(entity)
    session.commit.assert_not_called()
