"""Integration repository CRUD round-trip tests against ephemeral PostgreSQL."""

from __future__ import annotations

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from pg_g4public_orm.models import FamilyNew, GeneHasFamily
from pg_g4public_orm.repositories import Repository


@pytest.mark.integration
def test_repository_crud_round_trip_for_family_new(
    loaded_schema_connection,
    postgres_container,
) -> None:
    """Insert/get/update/filter/delete via Repository(session, FamilyNew)."""
    _ = loaded_schema_connection  # ensure schema is loaded for this function

    db_url = postgres_container.get_connection_url().replace(
        "postgresql+psycopg2://", "postgresql+psycopg://"
    )
    engine = create_engine(db_url)

    try:
        with Session(engine) as session:
            repository: Repository[FamilyNew] = Repository(session, FamilyNew)

            created = FamilyNew(abbreviation="T11_FAM", name="Task 11 family")
            repository.add(created)
            session.flush()

            assert created.id is not None
            assert isinstance(created.id, int)

            fetched = repository.get_by_id(created.id)
            assert fetched is not None
            assert fetched.id == created.id
            assert fetched.abbreviation == "T11_FAM"

            fetched.name = "Task 11 family updated"
            repository.save(fetched)
            session.flush()
            session.expire_all()

            updated = repository.get_by_id(created.id)
            assert updated is not None
            assert updated.name == "Task 11 family updated"

            matches = repository.filter_by(abbreviation="T11_FAM")
            assert len(matches) == 1
            assert matches[0].id == created.id

            repository.delete(updated)
            session.flush()
            session.expire_all()

            assert repository.get_by_id(created.id) is None

            session.rollback()
    finally:
        engine.dispose()


@pytest.mark.integration
def test_repository_crud_round_trip_for_junction_model(
    loaded_schema_connection,
    postgres_container,
) -> None:
    """Exercise a junction model repository path using gene_has_family."""
    _ = loaded_schema_connection

    db_url = postgres_container.get_connection_url().replace(
        "postgresql+psycopg2://", "postgresql+psycopg://"
    )
    engine = create_engine(db_url)

    try:
        with Session(engine) as session:
            family_repo: Repository[FamilyNew] = Repository(session, FamilyNew)
            junction_repo: Repository[GeneHasFamily] = Repository(session, GeneHasFamily)

            family = FamilyNew(abbreviation="T11_LINK", name="Task 11 junction family")
            family_repo.add(family)
            session.flush()

            assert family.id is not None

            link = GeneHasFamily(
                hgnc_id=999_999,
                family_id=family.id,
                url="https://example.org/t11",
                custom_sort=1,
            )
            junction_repo.add(link)
            session.flush()

            found = junction_repo.filter_by(hgnc_id=999_999, family_id=family.id)
            assert len(found) == 1
            assert found[0].url == "https://example.org/t11"

            junction_repo.delete(found[0])
            session.flush()

            assert junction_repo.filter_by(hgnc_id=999_999, family_id=family.id) == []

            family_obj = family_repo.get_by_id(family.id)
            assert family_obj is not None
            family_repo.delete(family_obj)
            session.flush()

            session.rollback()
    finally:
        engine.dispose()
