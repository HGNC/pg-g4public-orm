"""Tests for ``cell`` and the ``locus_stats`` / ``locus_stats_chr`` models.

Driven by the authoritative dump ``.ai/specs/pg-g4public.sql`` (the real
Navicat DDL of ``g4public``). These are unit tests asserting SQLAlchemy
metadata (table names, column sets, types, nullability, the forced ORM
primary keys, the sequence-backed ``cell_id``, and the ORM-only composite
primary keys) — no database required.
"""

from __future__ import annotations

import pytest
from sqlalchemy import (
    BigInteger,
    Integer,
    Sequence,
    String,
    Text,
    inspect,
)


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
# Cell
# ===========================================================================
@pytest.fixture(scope="module")
def cell():
    """Import the model lazily so collection succeeds before it exists."""
    from pg_g4public_orm.models.core.cell import Cell

    return Cell


EXPECTED_CELL_COLUMNS: dict[str, tuple[type, bool]] = {
    "cell_id": (Integer, False),
    "cell_name": (String, True),
    "cell_alias": (String, True),
    "cell_table": (String, True),
    "cell_permit": (Text, True),
    "cell_view": (Text, True),
    "cell_edit": (Text, True),
    "cell_lint": (Text, True),
    "cell_notes": (Text, True),
    "cell_sort": (Integer, True),
}

CELL_VARCHAR_LENGTHS: dict[str, int] = {
    "cell_name": 255,
    "cell_alias": 255,
    "cell_table": 255,
}


def test_cell_tablename(cell) -> None:
    """``__tablename__`` must be the exact ``cell``."""
    assert cell.__tablename__ == "cell"


def test_cell_full_column_set(cell) -> None:
    """Every dump column is present and no extra columns are declared."""
    _assert_full_column_set(cell, EXPECTED_CELL_COLUMNS)


@pytest.mark.parametrize("column_name", sorted(EXPECTED_CELL_COLUMNS))
def test_cell_column_types_and_nullability(cell, column_name: str) -> None:
    """Each column has the right type and nullability per the dump."""
    _assert_column_type_and_nullability(cell, column_name, EXPECTED_CELL_COLUMNS)


@pytest.mark.parametrize("column_name", sorted(CELL_VARCHAR_LENGTHS))
def test_cell_varchar_lengths(cell, column_name: str) -> None:
    """``varchar(N)`` columns carry the dump's length."""
    col = _column(cell, column_name)
    assert isinstance(col.type, String), column_name
    assert col.type.length == CELL_VARCHAR_LENGTHS[column_name]


def test_cell_cell_id_is_forced_primary_key(cell) -> None:
    """``cell_id`` is the forced ORM PK (no DB primary key exists)."""
    assert _pk_columns(cell) == ["cell_id"]


def test_cell_cell_id_is_not_nullable(cell) -> None:
    """``cell_id`` is NOT NULL in the dump."""
    assert _column(cell, "cell_id").nullable is False


def test_cell_cell_id_uses_sequence(cell) -> None:
    """``cell_id`` is sequence-backed with ``cell_cell_id_seq``."""
    col = _column(cell, "cell_id")
    assert _default_sequence_name(col) == "cell_cell_id_seq"


def test_cell_is_instantiable(cell) -> None:
    """The model can be instantiated with representative data."""
    row = cell(cell_id=1, cell_name="A cell", cell_sort=3)
    assert row.cell_id == 1
    assert row.cell_name == "A cell"
    assert row.cell_sort == 3


# ===========================================================================
# LocusStats
# ===========================================================================
@pytest.fixture(scope="module")
def locus_stats():
    """Import the model lazily so collection succeeds before it exists."""
    from pg_g4public_orm.models.core.locus_stats import LocusStats

    return LocusStats


EXPECTED_LOCUS_STATS_COLUMNS: dict[str, tuple[type, bool]] = {
    "ls_count": (BigInteger, True),
    "ls_type": (String, True),
    "ls_group": (Text, True),
    "ls_source": (Text, True),
    "ls_sort": (Text, True),
    "ls_date": (Text, True),
}


def test_locus_stats_tablename(locus_stats) -> None:
    """``__tablename__`` must be the exact ``locus_stats``."""
    assert locus_stats.__tablename__ == "locus_stats"


def test_locus_stats_full_column_set(locus_stats) -> None:
    """Every dump column is present and no extra columns are declared."""
    _assert_full_column_set(locus_stats, EXPECTED_LOCUS_STATS_COLUMNS)


@pytest.mark.parametrize("column_name", sorted(EXPECTED_LOCUS_STATS_COLUMNS))
def test_locus_stats_column_types_and_nullability(
    locus_stats, column_name: str
) -> None:
    """Each column has the right type and nullability per the dump."""
    _assert_column_type_and_nullability(
        locus_stats, column_name, EXPECTED_LOCUS_STATS_COLUMNS
    )


def test_locus_stats_ls_count_is_biginteger(locus_stats) -> None:
    """``ls_count`` is ``int8`` → ``BigInteger`` per the dump."""
    col = _column(locus_stats, "ls_count")
    assert isinstance(col.type, BigInteger)


def test_locus_stats_ls_type_is_unbounded_varchar(locus_stats) -> None:
    """``ls_type`` is ``varchar`` with no length in the dump."""
    col = _column(locus_stats, "ls_type")
    assert isinstance(col.type, String)
    assert col.type.length is None


def test_locus_stats_composite_pk(locus_stats) -> None:
    """ORM-only composite PK on (ls_type, ls_group, ls_source)."""
    assert _pk_columns(locus_stats) == ["ls_type", "ls_group", "ls_source"]


def test_locus_stats_is_instantiable(locus_stats) -> None:
    """The model can be instantiated with representative data."""
    row = locus_stats(ls_count=42, ls_type="protein_coding", ls_group="g")
    assert row.ls_count == 42
    assert row.ls_type == "protein_coding"


# ===========================================================================
# LocusStatsChr
# ===========================================================================
@pytest.fixture(scope="module")
def locus_stats_chr():
    """Import the model lazily so collection succeeds before it exists."""
    from pg_g4public_orm.models.core.locus_stats_chr import LocusStatsChr

    return LocusStatsChr


EXPECTED_LOCUS_STATS_CHR_COLUMNS: dict[str, tuple[type, bool]] = {
    "ls_chr": (String, True),
    "ls_count": (Integer, True),
    "ls_type": (String, True),
    "ls_group": (String, True),
    "ls_source": (String, True),
    "ls_sort": (Integer, True),
    "ls_date": (String, True),
}

LOCUS_STATS_CHR_VARCHAR_LENGTHS: dict[str, int] = {
    "ls_chr": 5,
    "ls_type": 50,
    "ls_group": 50,
    "ls_source": 25,
    "ls_date": 255,
}


def test_locus_stats_chr_tablename(locus_stats_chr) -> None:
    """``__tablename__`` must be the exact ``locus_stats_chr``."""
    assert locus_stats_chr.__tablename__ == "locus_stats_chr"


def test_locus_stats_chr_full_column_set(locus_stats_chr) -> None:
    """Every dump column is present and no extra columns are declared."""
    _assert_full_column_set(locus_stats_chr, EXPECTED_LOCUS_STATS_CHR_COLUMNS)


@pytest.mark.parametrize("column_name", sorted(EXPECTED_LOCUS_STATS_CHR_COLUMNS))
def test_locus_stats_chr_column_types_and_nullability(
    locus_stats_chr, column_name: str
) -> None:
    """Each column has the right type and nullability per the dump."""
    _assert_column_type_and_nullability(
        locus_stats_chr, column_name, EXPECTED_LOCUS_STATS_CHR_COLUMNS
    )


@pytest.mark.parametrize("column_name", sorted(LOCUS_STATS_CHR_VARCHAR_LENGTHS))
def test_locus_stats_chr_varchar_lengths(locus_stats_chr, column_name: str) -> None:
    """``varchar(N)`` columns carry the dump's length."""
    col = _column(locus_stats_chr, column_name)
    assert isinstance(col.type, String), column_name
    assert col.type.length == LOCUS_STATS_CHR_VARCHAR_LENGTHS[column_name]


def test_locus_stats_chr_ls_count_is_integer_not_biginteger(
    locus_stats_chr,
) -> None:
    """``ls_count`` is ``int4`` (not bigint) in ``locus_stats_chr``."""
    col = _column(locus_stats_chr, "ls_count")
    assert isinstance(col.type, Integer)
    assert not isinstance(col.type, BigInteger)


def test_locus_stats_chr_composite_pk(locus_stats_chr) -> None:
    """ORM-only composite PK on (ls_chr, ls_type, ls_group, ls_source)."""
    assert _pk_columns(locus_stats_chr) == [
        "ls_chr",
        "ls_type",
        "ls_group",
        "ls_source",
    ]


def test_locus_stats_chr_is_instantiable(locus_stats_chr) -> None:
    """The model can be instantiated with representative data."""
    row = locus_stats_chr(ls_chr="1", ls_count=10, ls_type="gene", ls_sort=2)
    assert row.ls_chr == "1"
    assert row.ls_count == 10
