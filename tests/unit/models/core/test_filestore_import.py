"""Tests for ``filestore`` and ``import`` core models.

These tests validate SQLAlchemy metadata against the authoritative PostgreSQL
DDL in ``.ai/specs/pg-g4public.sql``: table names, full column sets,
column types/nullability, forced ORM primary keys, and sequence-backed ids.
"""

from __future__ import annotations

import pytest
from sqlalchemy import BigInteger, Boolean, Integer, Sequence, String, Text, inspect


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _column(model, column_name: str):
    """Return a mapped column by name."""
    return inspect(model).columns[column_name]


def _assert_full_column_set(
    model, expected_columns: dict[str, tuple[type, bool]]
) -> None:
    """Assert model has exactly the expected column names."""
    assert set(inspect(model).columns.keys()) == set(expected_columns)


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
    """Return sequence name used as a column default, if present."""
    default = col.default
    if default is None:
        return None
    for candidate in (default, getattr(default, "arg", None)):
        if isinstance(candidate, Sequence):
            return candidate.name
    return None


def _assert_varchar_length(model, column_name: str, expected_length: int) -> None:
    """Assert a ``varchar(N)`` column has the expected ``N`` length."""
    col = _column(model, column_name)
    assert isinstance(col.type, String), column_name
    assert col.type.length == expected_length


# ===========================================================================
# Filestore
# ===========================================================================
@pytest.fixture(scope="module")
def filestore():
    """Import the model lazily so collection succeeds before it exists."""
    from pg_g4public_orm.models.core.filestore import Filestore

    return Filestore


EXPECTED_FILESTORE_COLUMNS: dict[str, tuple[type, bool]] = {
    "line_id": (BigInteger, False),
    "filename": (String, True),
    "line": (Text, True),
}

FILESTORE_VARCHAR_LENGTHS: dict[str, int] = {
    "filename": 255,
}


def test_filestore_tablename(filestore) -> None:
    """``__tablename__`` must match the dump exactly."""
    assert filestore.__tablename__ == "filestore"


def test_filestore_full_column_set(filestore) -> None:
    """Every dump column is present and no extra columns are declared."""
    _assert_full_column_set(filestore, EXPECTED_FILESTORE_COLUMNS)


@pytest.mark.parametrize("column_name", sorted(EXPECTED_FILESTORE_COLUMNS))
def test_filestore_column_types_and_nullability(
    filestore, column_name: str
) -> None:
    """Each column has the right type and nullability per the dump."""
    _assert_column_type_and_nullability(
        filestore, column_name, EXPECTED_FILESTORE_COLUMNS
    )


@pytest.mark.parametrize("column_name", sorted(FILESTORE_VARCHAR_LENGTHS))
def test_filestore_varchar_lengths(filestore, column_name: str) -> None:
    """``varchar(N)`` columns carry the dump's declared length."""
    _assert_varchar_length(
        filestore, column_name, FILESTORE_VARCHAR_LENGTHS[column_name]
    )


def test_filestore_line_id_is_forced_primary_key(filestore) -> None:
    """``line_id`` is the forced ORM PK (no DB primary key exists)."""
    assert _pk_columns(filestore) == ["line_id"]


def test_filestore_line_id_uses_sequence(filestore) -> None:
    """``line_id`` is sequence-backed by ``filestore_line_id_seq``."""
    col = _column(filestore, "line_id")
    assert _default_sequence_name(col) == "filestore_line_id_seq"


def test_filestore_is_instantiable(filestore) -> None:
    """The model can be instantiated with representative data."""
    row = filestore(line_id=1, filename="sample.txt", line="alpha")
    assert row.line_id == 1
    assert row.filename == "sample.txt"
    assert row.line == "alpha"


# ===========================================================================
# Import
# ===========================================================================
@pytest.fixture(scope="module")
def import_model():
    """Import the model lazily so collection succeeds before it exists."""
    from pg_g4public_orm.models.core.import_model import Import

    return Import


EXPECTED_IMPORT_COLUMNS: dict[str, tuple[type, bool]] = {
    "imp_id": (Integer, False),
    "imp_source": (Text, True),
    "imp_tbl": (String, True),
    "imp_name": (String, True),
    "imp_data_type": (Text, True),
    "imp_index": (Boolean, True),
    "imp_permit": (Text, True),
    "imp_notes": (Text, True),
    "imp_sort": (Integer, True),
}

IMPORT_VARCHAR_LENGTHS: dict[str, int] = {
    "imp_tbl": 255,
    "imp_name": 255,
}


def test_import_tablename(import_model) -> None:
    """``__tablename__`` must match the dump exactly."""
    assert import_model.__tablename__ == "import"


def test_import_full_column_set(import_model) -> None:
    """Every dump column is present and no extra columns are declared."""
    _assert_full_column_set(import_model, EXPECTED_IMPORT_COLUMNS)


@pytest.mark.parametrize("column_name", sorted(EXPECTED_IMPORT_COLUMNS))
def test_import_column_types_and_nullability(import_model, column_name: str) -> None:
    """Each column has the right type and nullability per the dump."""
    _assert_column_type_and_nullability(
        import_model, column_name, EXPECTED_IMPORT_COLUMNS
    )


@pytest.mark.parametrize("column_name", sorted(IMPORT_VARCHAR_LENGTHS))
def test_import_varchar_lengths(import_model, column_name: str) -> None:
    """``varchar(N)`` columns carry the dump's declared length."""
    _assert_varchar_length(
        import_model, column_name, IMPORT_VARCHAR_LENGTHS[column_name]
    )


def test_import_imp_id_is_forced_primary_key(import_model) -> None:
    """``imp_id`` is the forced ORM PK (no DB primary key exists)."""
    assert _pk_columns(import_model) == ["imp_id"]


def test_import_imp_id_uses_sequence(import_model) -> None:
    """``imp_id`` is sequence-backed by ``import_imp_id_seq``."""
    col = _column(import_model, "imp_id")
    assert _default_sequence_name(col) == "import_imp_id_seq"


def test_import_is_instantiable(import_model) -> None:
    """The model can be instantiated with representative data."""
    row = import_model(imp_id=1, imp_source="src", imp_tbl="tbl", imp_name="name")
    assert row.imp_id == 1
    assert row.imp_source == "src"
    assert row.imp_tbl == "tbl"
    assert row.imp_name == "name"
