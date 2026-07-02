"""Tests for the association (junction) models: ``GeneHasFamily``,
``FamilyHasExternalResource``, ``FamilyHasSpecialist``.

Driven by the authoritative dump ``.ai/specs/pg-g4public.sql`` (the real
Navicat DDL of ``g4public``). These are unit tests asserting SQLAlchemy
metadata (table names, column sets, types, nullability, the NOT NULL join
columns, the composite primary keys, and the ``varchar`` lengths on
``gene_has_family``) — no database required.
"""

from __future__ import annotations

import pytest
from sqlalchemy import Integer, String, inspect


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
# GeneHasFamily
# ===========================================================================
@pytest.fixture(scope="module")
def gene_has_family():
    """Import the model lazily so collection succeeds before it exists."""
    from pg_g4public_orm.models.association.gene_has_family import GeneHasFamily

    return GeneHasFamily


EXPECTED_GENE_HAS_FAMILY_COLUMNS: dict[str, tuple[type, bool]] = {
    "hgnc_id": (Integer, False),
    "family_id": (Integer, False),
    "url": (String, True),
    "custom_sort": (String, True),
}

GENE_HAS_FAMILY_VARCHAR_LENGTHS: dict[str, int] = {
    "url": 255,
    "custom_sort": 255,
}


def test_gene_has_family_tablename(gene_has_family) -> None:
    """``__tablename__`` must be the exact ``gene_has_family``."""
    assert gene_has_family.__tablename__ == "gene_has_family"


def test_gene_has_family_full_column_set(gene_has_family) -> None:
    """Every dump column is present and no extra columns are declared."""
    _assert_full_column_set(gene_has_family, EXPECTED_GENE_HAS_FAMILY_COLUMNS)


@pytest.mark.parametrize("column_name", sorted(EXPECTED_GENE_HAS_FAMILY_COLUMNS))
def test_gene_has_family_column_types_and_nullability(
    gene_has_family, column_name: str
) -> None:
    """Each column has the right type and nullability per the dump."""
    _assert_column_type_and_nullability(
        gene_has_family, column_name, EXPECTED_GENE_HAS_FAMILY_COLUMNS
    )


@pytest.mark.parametrize("column_name", sorted(GENE_HAS_FAMILY_VARCHAR_LENGTHS))
def test_gene_has_family_varchar_lengths(gene_has_family, column_name: str) -> None:
    """``url``/``custom_sort`` are varchar(255) per the dump."""
    col = _column(gene_has_family, column_name)
    assert isinstance(col.type, String), column_name
    assert col.type.length == GENE_HAS_FAMILY_VARCHAR_LENGTHS[column_name]


def test_gene_has_family_composite_pk(gene_has_family) -> None:
    """Composite primary key on (hgnc_id, family_id) — real DB PK."""
    assert _pk_columns(gene_has_family) == ["hgnc_id", "family_id"]


def test_gene_has_family_join_cols_are_not_nullable(gene_has_family) -> None:
    """Both join columns (``hgnc_id``, ``family_id``) are NOT NULL per the dump."""
    assert _column(gene_has_family, "hgnc_id").nullable is False
    assert _column(gene_has_family, "family_id").nullable is False


def test_gene_has_family_is_instantiable(gene_has_family) -> None:
    """The model can be instantiated with representative data."""
    row = gene_has_family(
        hgnc_id=1234, family_id=5, url="https://example.org", custom_sort="A"
    )
    assert row.hgnc_id == 1234
    assert row.family_id == 5
    assert row.url == "https://example.org"
    assert row.custom_sort == "A"


# ===========================================================================
# FamilyHasExternalResource
# ===========================================================================
@pytest.fixture(scope="module")
def family_has_external_resource():
    """Import the model lazily so collection succeeds before it exists."""
    from pg_g4public_orm.models.association.family_has_external_resource import (
        FamilyHasExternalResource,
    )

    return FamilyHasExternalResource


EXPECTED_FAMILY_HAS_EXTERNAL_RESOURCE_COLUMNS: dict[str, tuple[type, bool]] = {
    "family_id": (Integer, False),
    "ext_id": (Integer, False),
}


def test_family_has_external_resource_tablename(
    family_has_external_resource,
) -> None:
    """``__tablename__`` must be the exact ``family_has_external_resource``."""
    assert family_has_external_resource.__tablename__ == "family_has_external_resource"


def test_family_has_external_resource_full_column_set(
    family_has_external_resource,
) -> None:
    """Every dump column is present and no extra columns are declared."""
    _assert_full_column_set(
        family_has_external_resource,
        EXPECTED_FAMILY_HAS_EXTERNAL_RESOURCE_COLUMNS,
    )


@pytest.mark.parametrize(
    "column_name", sorted(EXPECTED_FAMILY_HAS_EXTERNAL_RESOURCE_COLUMNS)
)
def test_family_has_external_resource_column_types_and_nullability(
    family_has_external_resource, column_name: str
) -> None:
    """Each column has the right type and nullability per the dump."""
    _assert_column_type_and_nullability(
        family_has_external_resource,
        column_name,
        EXPECTED_FAMILY_HAS_EXTERNAL_RESOURCE_COLUMNS,
    )


def test_family_has_external_resource_composite_pk(
    family_has_external_resource,
) -> None:
    """Composite primary key on (family_id, ext_id) — real DB PK."""
    assert _pk_columns(family_has_external_resource) == ["family_id", "ext_id"]


def test_family_has_external_resource_join_cols_are_not_nullable(
    family_has_external_resource,
) -> None:
    """Both join columns (``family_id``, ``ext_id``) are NOT NULL per the dump."""
    assert _column(family_has_external_resource, "family_id").nullable is False
    assert _column(family_has_external_resource, "ext_id").nullable is False


def test_family_has_external_resource_is_instantiable(
    family_has_external_resource,
) -> None:
    """The model can be instantiated with representative data."""
    row = family_has_external_resource(family_id=1, ext_id=2)
    assert row.family_id == 1
    assert row.ext_id == 2


# ===========================================================================
# FamilyHasSpecialist
# ===========================================================================
@pytest.fixture(scope="module")
def family_has_specialist():
    """Import the model lazily so collection succeeds before it exists."""
    from pg_g4public_orm.models.association.family_has_specialist import (
        FamilyHasSpecialist,
    )

    return FamilyHasSpecialist


EXPECTED_FAMILY_HAS_SPECIALIST_COLUMNS: dict[str, tuple[type, bool]] = {
    "fam_id": (Integer, False),
    "specialist_id": (Integer, False),
}


def test_family_has_specialist_tablename(family_has_specialist) -> None:
    """``__tablename__`` must be the exact ``family_has_specialist``."""
    assert family_has_specialist.__tablename__ == "family_has_specialist"


def test_family_has_specialist_full_column_set(family_has_specialist) -> None:
    """Every dump column is present and no extra columns are declared."""
    _assert_full_column_set(
        family_has_specialist, EXPECTED_FAMILY_HAS_SPECIALIST_COLUMNS
    )


@pytest.mark.parametrize("column_name", sorted(EXPECTED_FAMILY_HAS_SPECIALIST_COLUMNS))
def test_family_has_specialist_column_types_and_nullability(
    family_has_specialist, column_name: str
) -> None:
    """Each column has the right type and nullability per the dump."""
    _assert_column_type_and_nullability(
        family_has_specialist,
        column_name,
        EXPECTED_FAMILY_HAS_SPECIALIST_COLUMNS,
    )


def test_family_has_specialist_composite_pk(family_has_specialist) -> None:
    """Composite primary key on (fam_id, specialist_id) — real DB PK."""
    assert _pk_columns(family_has_specialist) == ["fam_id", "specialist_id"]


def test_family_has_specialist_join_cols_are_not_nullable(
    family_has_specialist,
) -> None:
    """Both join columns (``fam_id``, ``specialist_id``) are NOT NULL per the dump."""
    assert _column(family_has_specialist, "fam_id").nullable is False
    assert _column(family_has_specialist, "specialist_id").nullable is False


def test_family_has_specialist_is_instantiable(family_has_specialist) -> None:
    """The model can be instantiated with representative data."""
    row = family_has_specialist(fam_id=1, specialist_id=2)
    assert row.fam_id == 1
    assert row.specialist_id == 2
