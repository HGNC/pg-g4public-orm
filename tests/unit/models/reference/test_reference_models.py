"""Tests for the reference models: ``ExternalResource`` and ``Specialist``.

Driven by the authoritative dump ``.ai/specs/pg-g4public.sql`` (the real
Navicat DDL of ``g4public``). These are unit tests asserting SQLAlchemy
metadata (table names, column sets, types, nullability, the real database
primary keys, the ``approved`` boolean default, and the declared unique
indexes) — no database required.
"""

from __future__ import annotations

import pytest
from sqlalchemy import Boolean, Integer, String, Text, inspect


# ---------------------------------------------------------------------------
# Helpers (mirrors tests/unit/models/core/test_family_group.py)
# ---------------------------------------------------------------------------
def _column(model, column_name: str):
    """Return a mapped column by name."""
    return inspect(model).columns[column_name]


def _column_names(model) -> set[str]:
    """Return mapped column names for a model."""
    return set(inspect(model).columns.keys())


def _assert_full_column_set(
    model, expected_columns: dict[str, tuple[type, bool]]
) -> None:
    """Assert model has exactly the expected column names."""
    assert _column_names(model) == set(expected_columns)


def _pk_columns(model) -> list[str]:
    """Return the ordered primary-key column names for a model."""
    return [c.name for c in inspect(model).primary_key]


def _indexes_by_name(model) -> dict[str, object]:
    """Return declared table indexes keyed by index name."""
    return {idx.name: idx for idx in model.__table__.indexes}


def _assert_column_type_and_nullability(
    model, column_name: str, expected_columns: dict[str, tuple[type, bool]]
) -> None:
    """Assert mapped column type and nullability against expected metadata."""
    col = _column(model, column_name)
    expected_type, expected_nullable = expected_columns[column_name]
    assert isinstance(col.type, expected_type), (
        f"{column_name}: expected {expected_type.__name__}, "
        f"got {type(col.type).__name__}"
    )
    assert (
        col.nullable is expected_nullable
    ), f"{column_name}: nullable={col.nullable}, expected {expected_nullable}"


# ===========================================================================
# ExternalResource
# ===========================================================================
@pytest.fixture(scope="module")
def external_resource():
    """Import the model lazily so collection succeeds before it exists."""
    from pg_g4public_orm.models.reference.external_resource import ExternalResource

    return ExternalResource


EXPECTED_EXTERNAL_RESOURCE_COLUMNS: dict[str, tuple[type, bool]] = {
    "id": (Integer, False),
    "name": (String, False),
    "url": (String, False),
    "description": (String, True),
    "approved": (Boolean, False),
}

EXTERNAL_RESOURCE_VARCHAR_LENGTHS: dict[str, int] = {
    "name": 255,
    "url": 255,
    "description": 255,
}


def test_external_resource_tablename(external_resource) -> None:
    """``__tablename__`` must be the exact ``external_resource``."""
    assert external_resource.__tablename__ == "external_resource"


def test_external_resource_full_column_set(external_resource) -> None:
    """Every dump column is present and no extra columns are declared."""
    _assert_full_column_set(external_resource, EXPECTED_EXTERNAL_RESOURCE_COLUMNS)


@pytest.mark.parametrize("column_name", sorted(EXPECTED_EXTERNAL_RESOURCE_COLUMNS))
def test_external_resource_column_types_and_nullability(
    external_resource, column_name: str
) -> None:
    """Each column has the right type and nullability per the dump."""
    _assert_column_type_and_nullability(
        external_resource, column_name, EXPECTED_EXTERNAL_RESOURCE_COLUMNS
    )


@pytest.mark.parametrize("column_name", sorted(EXTERNAL_RESOURCE_VARCHAR_LENGTHS))
def test_external_resource_varchar_lengths(external_resource, column_name: str) -> None:
    """``varchar(N)`` columns carry the dump's length."""
    col = _column(external_resource, column_name)
    assert isinstance(col.type, String), column_name
    assert col.type.length == EXTERNAL_RESOURCE_VARCHAR_LENGTHS[column_name]


def test_external_resource_id_is_primary_key(external_resource) -> None:
    """``id`` is the single-column primary key (real DB PK)."""
    assert _pk_columns(external_resource) == ["id"]


def test_external_resource_id_is_not_nullable(external_resource) -> None:
    """``id`` is NOT NULL in the dump."""
    assert _column(external_resource, "id").nullable is False


def test_external_resource_approved_is_boolean_not_null_default_false(
    external_resource,
) -> None:
    """``approved`` is ``bool NOT NULL DEFAULT false`` per the dump."""
    col = _column(external_resource, "approved")
    assert isinstance(col.type, Boolean)
    assert col.nullable is False
    assert col.default is not None, "approved must have a DEFAULT false"
    # ColumnDefault.arg holds the literal default expression → False.
    assert col.default.arg is False


def test_external_resource_name_and_url_are_not_nullable(
    external_resource,
) -> None:
    """``name`` and ``url`` are NOT NULL per the dump."""
    assert _column(external_resource, "name").nullable is False
    assert _column(external_resource, "url").nullable is False


def test_external_resource_id_key_unique_index(external_resource) -> None:
    """The ``external_resource_id_key`` unique index on ``id`` is declared."""
    indexes = _indexes_by_name(external_resource)
    assert "external_resource_id_key" in indexes
    assert [c.name for c in indexes["external_resource_id_key"].columns] == ["id"]
    assert indexes["external_resource_id_key"].unique is True


def test_external_resource_is_instantiable(external_resource) -> None:
    """The model can be instantiated with representative data."""
    resource = external_resource(
        id=1, name="ClinGen", url="https://example.org", approved=True
    )
    assert resource.id == 1
    assert resource.approved is True


# ===========================================================================
# Specialist
# ===========================================================================
@pytest.fixture(scope="module")
def specialist():
    """Import the model lazily so collection succeeds before it exists."""
    from pg_g4public_orm.models.reference.specialist import Specialist

    return Specialist


EXPECTED_SPECIALIST_COLUMNS: dict[str, tuple[type, bool]] = {
    "id": (Integer, False),
    "name": (String, False),
    "address": (Text, False),
    "url": (String, True),
}

SPECIALIST_VARCHAR_LENGTHS: dict[str, int] = {
    "name": 255,
    "url": 255,
}


def test_specialist_tablename(specialist) -> None:
    """``__tablename__`` must be the exact ``specialist``."""
    assert specialist.__tablename__ == "specialist"


def test_specialist_full_column_set(specialist) -> None:
    """Every dump column is present and no extra columns are declared."""
    _assert_full_column_set(specialist, EXPECTED_SPECIALIST_COLUMNS)


@pytest.mark.parametrize("column_name", sorted(EXPECTED_SPECIALIST_COLUMNS))
def test_specialist_column_types_and_nullability(specialist, column_name: str) -> None:
    """Each column has the right type and nullability per the dump."""
    _assert_column_type_and_nullability(
        specialist, column_name, EXPECTED_SPECIALIST_COLUMNS
    )


@pytest.mark.parametrize("column_name", sorted(SPECIALIST_VARCHAR_LENGTHS))
def test_specialist_varchar_lengths(specialist, column_name: str) -> None:
    """``varchar(N)`` columns carry the dump's length."""
    col = _column(specialist, column_name)
    assert isinstance(col.type, String), column_name
    assert col.type.length == SPECIALIST_VARCHAR_LENGTHS[column_name]


def test_specialist_id_is_primary_key(specialist) -> None:
    """``id`` is the single-column primary key (real DB PK)."""
    assert _pk_columns(specialist) == ["id"]


def test_specialist_name_and_address_are_not_nullable(specialist) -> None:
    """``name`` and ``address`` are NOT NULL per the dump."""
    assert _column(specialist, "name").nullable is False
    assert _column(specialist, "address").nullable is False


def test_specialist_id_key_unique_index(specialist) -> None:
    """The ``specialist_id_key`` unique index on ``id`` is declared."""
    indexes = _indexes_by_name(specialist)
    assert "specialist_id_key" in indexes
    assert [c.name for c in indexes["specialist_id_key"].columns] == ["id"]
    assert indexes["specialist_id_key"].unique is True


def test_specialist_is_instantiable(specialist) -> None:
    """The model can be instantiated with representative data."""
    spec = specialist(id=1, name="A specialist", address="123 Example St")
    assert spec.name == "A specialist"
    assert spec.address == "123 Example St"
