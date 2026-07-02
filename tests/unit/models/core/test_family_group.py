"""Tests for the family-group models: FamilyNew, FamilyAlias, Hierarchy,
HierarchyClosure.

Driven by the authoritative dump ``.ai/specs/pg-g4public.sql`` (the real
Navicat DDL of ``g4public``). These are unit tests asserting SQLAlchemy
metadata (table names, column sets, types, nullability, primary keys, the
sequence-backed ids, and the declared indexes) — no database required.
"""

from __future__ import annotations

import pytest
from sqlalchemy import DateTime, Integer, Sequence, String, Text, inspect


# ---------------------------------------------------------------------------
# Helpers
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


def _index_names(model) -> set[str]:
    """Return declared index names for the mapped table."""
    return {idx.name for idx in model.__table__.indexes}


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


def _default_sequence_name(col) -> str | None:
    """Return the name of the ``Sequence`` used as a column default, if any.

    SQLAlchemy stores a ``Sequence`` passed positionally to ``mapped_column``
    as the column default. It may be stored directly or wrapped in a
    ``ColumnDefault`` (reachable via ``.arg``).
    """
    default = col.default
    if default is None:
        return None
    for candidate in (default, getattr(default, "arg", None)):
        if isinstance(candidate, Sequence):
            return candidate.name
    return None


# ===========================================================================
# FamilyNew
# ===========================================================================
@pytest.fixture(scope="module")
def family_new():
    """Import the model lazily so collection succeeds before it exists."""
    from pg_g4public_orm.models.core.family_new import FamilyNew

    return FamilyNew


EXPECTED_FAMILY_NEW_COLUMNS: dict[str, tuple[type, bool]] = {
    # (sqlalchemy type class, nullable?) — transcribed from pg-g4public.sql
    "id": (Integer, False),
    "abbreviation": (String, True),
    "name": (String, True),
    "editor": (String, True),
    "curator_comment": (Text, True),
    "status": (String, True),
    "external_note": (Text, True),
    "pubmed_ids": (Text, True),
    "type": (String, True),
    "desc_comment": (Text, True),
    "desc_label": (String, True),
    "desc_source": (String, True),
    "desc_go": (String, True),
    "typical_gene": (String, True),
    "date_created": (DateTime, True),
    "date_modified": (DateTime, True),
}

FAMILY_NEW_VARCHAR_LENGTHS: dict[str, int] = {
    "abbreviation": 50,
    "name": 150,
    "editor": 50,
    "status": 255,
    "type": 50,
    "desc_label": 255,
    "desc_source": 255,
    "desc_go": 255,
    "typical_gene": 255,
}


def test_family_new_tablename(family_new) -> None:
    """``__tablename__`` must be the exact ``family_new``."""
    assert family_new.__tablename__ == "family_new"


def test_family_new_full_column_set(family_new) -> None:
    """Every dump column is present and no extra columns are declared."""
    _assert_full_column_set(family_new, EXPECTED_FAMILY_NEW_COLUMNS)


@pytest.mark.parametrize("column_name", sorted(EXPECTED_FAMILY_NEW_COLUMNS))
def test_family_new_column_types_and_nullability(family_new, column_name: str) -> None:
    """Each column has the right type and nullability per the dump."""
    _assert_column_type_and_nullability(
        family_new, column_name, EXPECTED_FAMILY_NEW_COLUMNS
    )


@pytest.mark.parametrize("column_name", sorted(FAMILY_NEW_VARCHAR_LENGTHS))
def test_family_new_varchar_lengths(family_new, column_name: str) -> None:
    """``varchar(N)`` columns carry the dump's length."""
    col = _column(family_new, column_name)
    assert isinstance(col.type, String), column_name
    assert col.type.length == FAMILY_NEW_VARCHAR_LENGTHS[column_name]


def test_family_new_id_is_primary_key(family_new) -> None:
    """``id`` is the single-column primary key."""
    assert _pk_columns(family_new) == ["id"]


def test_family_new_id_is_not_nullable(family_new) -> None:
    """``id`` is NOT NULL in the dump (it is the PK)."""
    assert _column(family_new, "id").nullable is False


def test_family_new_id_uses_sequence(family_new) -> None:
    """``id`` is sequence-backed with ``family_new_fam_id_seq``."""
    col = _column(family_new, "id")
    assert _default_sequence_name(col) == "family_new_fam_id_seq"


def test_family_new_timestamps_default_now(family_new) -> None:
    """``date_created``/``date_modified`` are DateTime with a now() default."""
    for column_name in ("date_created", "date_modified"):
        col = _column(family_new, column_name)
        assert isinstance(col.type, DateTime), column_name
        assert col.default is not None, f"{column_name} must have a default"


def test_family_new_index_ind_name(family_new) -> None:
    """The ``ind_name`` index is declared (called out in the spec)."""
    assert "ind_name" in _index_names(family_new)


def test_family_new_index_ind_name_targets_abbreviation(family_new) -> None:
    """``ind_name`` covers ``abbreviation``."""
    idx = _indexes_by_name(family_new)["ind_name"]
    assert [c.name for c in idx.columns] == ["abbreviation"]


def test_family_new_id_key_unique_index(family_new) -> None:
    """The ``family_new_id_key`` unique index on ``id`` is declared."""
    indexes = _indexes_by_name(family_new)
    assert "family_new_id_key" in indexes
    assert [c.name for c in indexes["family_new_id_key"].columns] == ["id"]
    assert indexes["family_new_id_key"].unique is True


def test_family_new_is_instantiable(family_new) -> None:
    """The model can be instantiated with representative data."""
    fam = family_new(id=1, abbreviation="ABCD", name="A family", status="Approved")
    assert fam.id == 1
    assert fam.abbreviation == "ABCD"


# ===========================================================================
# FamilyAlias
# ===========================================================================
@pytest.fixture(scope="module")
def family_alias():
    """Import the model lazily so collection succeeds before it exists."""
    from pg_g4public_orm.models.core.family_alias import FamilyAlias

    return FamilyAlias


EXPECTED_FAMILY_ALIAS_COLUMNS: dict[str, tuple[type, bool]] = {
    "id": (Integer, False),
    "family_id": (Integer, False),
    "alias": (String, False),
}


def test_family_alias_tablename(family_alias) -> None:
    """``__tablename__`` must be the exact ``family_alias``."""
    assert family_alias.__tablename__ == "family_alias"


def test_family_alias_full_column_set(family_alias) -> None:
    """Every dump column is present and no extra columns are declared."""
    _assert_full_column_set(family_alias, EXPECTED_FAMILY_ALIAS_COLUMNS)


@pytest.mark.parametrize("column_name", sorted(EXPECTED_FAMILY_ALIAS_COLUMNS))
def test_family_alias_column_types_and_nullability(
    family_alias, column_name: str
) -> None:
    """Each column has the right type and nullability per the dump."""
    _assert_column_type_and_nullability(
        family_alias, column_name, EXPECTED_FAMILY_ALIAS_COLUMNS
    )


def test_family_alias_alias_is_varchar_255(family_alias) -> None:
    """``alias`` is varchar(255) NOT NULL."""
    col = _column(family_alias, "alias")
    assert isinstance(col.type, String)
    assert col.type.length == 255


def test_family_alias_id_is_primary_key(family_alias) -> None:
    """``id`` is the single-column primary key."""
    assert _pk_columns(family_alias) == ["id"]


def test_family_alias_id_uses_sequence(family_alias) -> None:
    """``id`` is sequence-backed with ``family_alias_id_seq``."""
    col = _column(family_alias, "id")
    assert _default_sequence_name(col) == "family_alias_id_seq"


def test_family_alias_is_instantiable(family_alias) -> None:
    """The model can be instantiated with representative data."""
    alias = family_alias(id=1, family_id=5, alias="Some Alias")
    assert alias.alias == "Some Alias"
    assert alias.family_id == 5


# ===========================================================================
# Hierarchy
# ===========================================================================
@pytest.fixture(scope="module")
def hierarchy():
    """Import the model lazily so collection succeeds before it exists."""
    from pg_g4public_orm.models.core.hierarchy import Hierarchy

    return Hierarchy


EXPECTED_HIERARCHY_COLUMNS: dict[str, tuple[type, bool]] = {
    "parent_fam_id": (Integer, False),
    "child_fam_id": (Integer, False),
}


def test_hierarchy_tablename(hierarchy) -> None:
    """``__tablename__`` must be the exact ``hierarchy``."""
    assert hierarchy.__tablename__ == "hierarchy"


def test_hierarchy_full_column_set(hierarchy) -> None:
    """Every dump column is present and no extra columns are declared."""
    _assert_full_column_set(hierarchy, EXPECTED_HIERARCHY_COLUMNS)


@pytest.mark.parametrize("column_name", sorted(EXPECTED_HIERARCHY_COLUMNS))
def test_hierarchy_column_types_and_nullability(hierarchy, column_name: str) -> None:
    """Both columns are NOT NULL int4 per the dump."""
    _assert_column_type_and_nullability(
        hierarchy, column_name, EXPECTED_HIERARCHY_COLUMNS
    )


def test_hierarchy_composite_pk(hierarchy) -> None:
    """Composite primary key on (parent_fam_id, child_fam_id)."""
    assert _pk_columns(hierarchy) == ["parent_fam_id", "child_fam_id"]


def test_hierarchy_is_instantiable(hierarchy) -> None:
    """The model can be instantiated with representative data."""
    edge = hierarchy(parent_fam_id=1, child_fam_id=2)
    assert edge.parent_fam_id == 1
    assert edge.child_fam_id == 2


# ===========================================================================
# HierarchyClosure
# ===========================================================================
@pytest.fixture(scope="module")
def hierarchy_closure():
    """Import the model lazily so collection succeeds before it exists."""
    from pg_g4public_orm.models.core.hierarchy_closure import HierarchyClosure

    return HierarchyClosure


EXPECTED_HIERARCHY_CLOSURE_COLUMNS: dict[str, tuple[type, bool]] = {
    "parent_fam_id": (Integer, False),
    "child_fam_id": (Integer, False),
    "distance": (Integer, False),
}


def test_hierarchy_closure_tablename(hierarchy_closure) -> None:
    """``__tablename__`` must be the exact ``hierarchy_closure``."""
    assert hierarchy_closure.__tablename__ == "hierarchy_closure"


def test_hierarchy_closure_full_column_set(hierarchy_closure) -> None:
    """Every dump column is present and no extra columns are declared."""
    _assert_full_column_set(hierarchy_closure, EXPECTED_HIERARCHY_CLOSURE_COLUMNS)


@pytest.mark.parametrize("column_name", sorted(EXPECTED_HIERARCHY_CLOSURE_COLUMNS))
def test_hierarchy_closure_column_types_and_nullability(
    hierarchy_closure, column_name: str
) -> None:
    """All three columns are NOT NULL int4 per the dump."""
    _assert_column_type_and_nullability(
        hierarchy_closure, column_name, EXPECTED_HIERARCHY_CLOSURE_COLUMNS
    )


def test_hierarchy_closure_three_column_composite_pk(hierarchy_closure) -> None:
    """Three-column composite primary key (parent_fam_id, child_fam_id, distance)."""
    assert _pk_columns(hierarchy_closure) == [
        "parent_fam_id",
        "child_fam_id",
        "distance",
    ]


def test_hierarchy_closure_distance_defaults_to_zero(hierarchy_closure) -> None:
    """``distance`` has a server/python default of 0 (matching ``DEFAULT 0``)."""
    col = _column(hierarchy_closure, "distance")
    assert col.default is not None
    # The default renders to 0 (ColumnDefault.arg == 0).
    assert col.default.arg == 0


def test_hierarchy_closure_is_instantiable(hierarchy_closure) -> None:
    """The model can be instantiated with representative data."""
    row = hierarchy_closure(parent_fam_id=1, child_fam_id=3, distance=2)
    assert row.distance == 2
