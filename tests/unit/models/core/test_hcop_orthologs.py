"""Tests for the ``hcop_orthologs`` model.

HCOP (HCOP Comparison of Orthology Predictions) pairwise ortholog rows.

Driven by the authoritative dump ``.ai/specs/pg-g4public.sql`` (the real
Navicat DDL of ``g4public``). These are unit tests asserting SQLAlchemy
metadata (table name, full column set, types, nullability, the forced ORM
primary key on ``orth_id``, the ``class_a``/``class_b`` plain-``varchar``
columns, and the absence of any MySQL dialect kwargs) — no database required.
"""

from __future__ import annotations

import pytest
from sqlalchemy import BigInteger, String, Text, inspect


# ---------------------------------------------------------------------------
# Helpers (mirrors tests/unit/models/core/test_gene_xref_models.py)
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
# HcopOrthologs
# ===========================================================================
@pytest.fixture(scope="module")
def hcop_orthologs():
    """Import the model lazily so collection succeeds before it exists."""
    from pg_g4public_orm.models.core.hcop_orthologs import HcopOrthologs

    return HcopOrthologs


# All 31 ``hcop_orthologs`` columns transcribed verbatim from
# pg-g4public.sql. (The spec's task title rounds this to "30 cols"; the dump
# is authoritative and declares 31 — the dump wins.)
EXPECTED_HCOPY_COLUMNS: dict[str, tuple[type, bool]] = {
    # --- Identifiers / taxonomy (int8 -> BigInteger) ---
    "orth_id": (BigInteger, False),
    "taxon_a": (BigInteger, False),
    "taxon_b": (BigInteger, False),
    # --- Cross-database ids (varchar, most NOT NULL) ---
    "db_id_a": (String, False),
    "db_id_b": (String, False),
    "vgnc_a": (String, True),
    "vgnc_b": (String, True),
    "ensembl_a": (String, False),
    "ensembl_b": (String, False),
    "entrez_a": (String, True),
    "entrez_b": (String, True),
    # --- Symbol + names ---
    "symbol_a": (String, True),
    "symbol_b": (String, True),
    "symbol_source_a": (String, True),
    "symbol_source_b": (String, True),
    "name_a": (Text, True),
    "name_b": (Text, True),
    # --- Source / locus metadata ---
    "source_name_a": (String, True),
    "source_name_b": (String, True),
    "locus_type_a": (String, True),
    "locus_type_b": (String, True),
    "locus_source_a": (String, True),
    "locus_source_b": (String, True),
    # --- class_a / class_b: plain varchar(8), NOT enum (PG divergence) ---
    "class_a": (String, True),
    "class_b": (String, True),
    # --- Chromosomes / support / links ---
    "chr_a": (String, True),
    "chr_b": (String, True),
    "support": (String, False),
    "text_link_a": (Text, False),
    "text_link_b": (Text, False),
    "sort_order": (BigInteger, False),
}

HCOPY_VARCHAR_LENGTHS: dict[str, int] = {
    "db_id_a": 255,
    "db_id_b": 255,
    "vgnc_a": 15,
    "vgnc_b": 255,
    "ensembl_a": 28,
    "ensembl_b": 28,
    "entrez_a": 28,
    "entrez_b": 28,
    "symbol_a": 255,
    "symbol_b": 255,
    "symbol_source_a": 128,
    "symbol_source_b": 128,
    "source_name_a": 128,
    "source_name_b": 128,
    "locus_type_a": 255,
    "locus_type_b": 255,
    "locus_source_a": 128,
    "locus_source_b": 128,
    "class_a": 8,
    "class_b": 8,
    "chr_a": 128,
    "chr_b": 128,
    "support": 255,
}

HCOPY_TEXT_COLUMNS = {"name_a", "name_b", "text_link_a", "text_link_b"}

HCOPY_BIGINT_COLUMNS = {"orth_id", "taxon_a", "taxon_b", "sort_order"}

HCOPY_NOT_NULL_COLUMNS = {
    "orth_id",
    "taxon_a",
    "taxon_b",
    "db_id_a",
    "db_id_b",
    "ensembl_a",
    "ensembl_b",
    "support",
    "text_link_a",
    "text_link_b",
    "sort_order",
}


def test_hcop_orthologs_tablename(hcop_orthologs) -> None:
    """``__tablename__`` must be the exact ``hcop_orthologs``."""
    assert hcop_orthologs.__tablename__ == "hcop_orthologs"


def test_hcop_orthologs_full_column_set(hcop_orthologs) -> None:
    """Every dump column is present and no extra columns are declared."""
    _assert_full_column_set(hcop_orthologs, EXPECTED_HCOPY_COLUMNS)


def test_hcop_orthologs_column_count_matches_dump(hcop_orthologs) -> None:
    """The dump declares exactly 31 columns for ``hcop_orthologs``."""
    assert len(inspect(hcop_orthologs).columns) == 31


@pytest.mark.parametrize("column_name", sorted(EXPECTED_HCOPY_COLUMNS))
def test_hcop_orthologs_column_types_and_nullability(
    hcop_orthologs, column_name: str
) -> None:
    """Each column has the right type and nullability per the dump."""
    _assert_column_type_and_nullability(
        hcop_orthologs, column_name, EXPECTED_HCOPY_COLUMNS
    )


@pytest.mark.parametrize("column_name", sorted(HCOPY_BIGINT_COLUMNS))
def test_hcop_orthologs_bigint_columns(hcop_orthologs, column_name: str) -> None:
    """``orth_id``/``taxon_a``/``taxon_b``/``sort_order`` are ``int8`` -> BigInteger."""
    assert isinstance(_column(hcop_orthologs, column_name).type, BigInteger)


@pytest.mark.parametrize("column_name", sorted(HCOPY_TEXT_COLUMNS))
def test_hcop_orthologs_text_columns(hcop_orthologs, column_name: str) -> None:
    """``name_a``/``name_b``/``text_link_*`` are ``text`` per the dump."""
    assert isinstance(_column(hcop_orthologs, column_name).type, Text)


@pytest.mark.parametrize("column_name", sorted(HCOPY_NOT_NULL_COLUMNS))
def test_hcop_orthologs_not_null_columns(hcop_orthologs, column_name: str) -> None:
    """The NOT NULL columns are non-nullable per the dump."""
    assert _column(hcop_orthologs, column_name).nullable is False


@pytest.mark.parametrize("column_name", sorted(HCOPY_VARCHAR_LENGTHS))
def test_hcop_orthologs_varchar_lengths(hcop_orthologs, column_name: str) -> None:
    """``varchar(N)`` columns carry the dump's length."""
    col = _column(hcop_orthologs, column_name)
    assert isinstance(col.type, String), column_name
    assert col.type.length == HCOPY_VARCHAR_LENGTHS[column_name], (
        f"{column_name}: length={col.type.length}, "
        f"expected {HCOPY_VARCHAR_LENGTHS[column_name]}"
    )


def test_hcop_orthologs_orth_id_is_forced_primary_key(hcop_orthologs) -> None:
    """``orth_id`` (NOT NULL bigint, no DB PK) is the forced ORM primary key."""
    assert _pk_columns(hcop_orthologs) == ["orth_id"]
    assert _column(hcop_orthologs, "orth_id").nullable is False


def test_hcop_orthologs_class_a_class_b_are_plain_varchar_not_enum(
    hcop_orthologs,
) -> None:
    """``class_a``/``class_b`` are plain ``varchar(8)`` in PG — NOT enums.

    This deliberately diverges from the MySQL sibling (my-g4public-orm) where
    these columns are MySQL ``ENUM`` types. The PG dump declares them as
    ``varchar(8)``, so they must map to ``String(8)`` and never to an
    ``sqlalchemy.Enum``.
    """
    from sqlalchemy import Enum as SAEnum

    for column_name in ("class_a", "class_b"):
        col = _column(hcop_orthologs, column_name)
        assert isinstance(col.type, String), column_name
        assert col.type.length == 8, column_name
        assert not isinstance(
            col.type, SAEnum
        ), f"{column_name} must NOT be an Enum (PG uses varchar(8))"


def test_hcop_orthologs_has_no_mysql_dialect_kwargs(hcop_orthologs) -> None:
    """A PostgreSQL table carries no ``mysql_charset``/``mysql_collate`` kwargs.

    These MySQL-only dialect options appear on the MySQL sibling's table; the
    PG model must not declare them.
    """
    table_kwargs = hcop_orthologs.__table__.kwargs
    assert "mysql_charset" not in table_kwargs
    assert "mysql_collate" not in table_kwargs


def test_hcop_orthologs_has_no_declared_indexes(hcop_orthologs) -> None:
    """The dump defines no indexes on ``hcop_orthologs`` — the model must not add any."""
    assert {idx.name for idx in hcop_orthologs.__table__.indexes} == set()


def test_hcop_orthologs_is_instantiable(hcop_orthologs) -> None:
    """The model can be instantiated with representative (NOT NULL) data."""
    row = hcop_orthologs(
        orth_id=1,
        taxon_a=9606,
        taxon_b=10090,
        db_id_a="HGNC:5",
        db_id_b="MGI:88031",
        ensembl_a="ENSG00000121410",
        ensembl_b="ENSMUSG00000017167",
        support="of,opb,phyl",
        text_link_a="http://example.org/a",
        text_link_b="http://example.org/b",
        sort_order=1,
        class_a="M",
        class_b="M",
        name_a="alpha-1-B glycoprotein",
        name_b="alpha-1-B glycoprotein",
    )
    assert row.orth_id == 1
    assert row.taxon_a == 9606
    assert row.support == "of,opb,phyl"
    assert row.class_a == "M"
    assert row.name_a == "alpha-1-B glycoprotein"
    assert row.text_link_a == "http://example.org/a"
    assert row.sort_order == 1
