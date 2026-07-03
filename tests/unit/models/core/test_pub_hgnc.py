"""Tests for the ``pub_hgnc`` model (central gene table).

Driven by the authoritative dump ``.ai/specs/pg-g4public.sql`` (the real
Navicat DDL of ``g4public``). These are unit tests asserting SQLAlchemy
metadata (table name, column set, types, nullability, the forced ORM primary
key, and the 8 declared indexes) — no database required.
"""

from __future__ import annotations

from datetime import date

import pytest
from sqlalchemy import Boolean, Date, Integer, String, Text, inspect


@pytest.fixture(scope="module")
def pub_hgnc():
    """Import the model lazily so collection succeeds before it exists."""
    from pg_g4public_orm.models.core.pub_hgnc import PubHgnc

    return PubHgnc


def _mapper(pub_hgnc):
    """Return the SQLAlchemy mapper for ``PubHgnc``."""
    return inspect(pub_hgnc)


def _column(pub_hgnc, column_name: str):
    """Return a mapped column by name."""
    return _mapper(pub_hgnc).columns[column_name]


def _index_names(pub_hgnc) -> set[str]:
    """Return declared index names for the mapped table."""
    return {idx.name for idx in pub_hgnc.__table__.indexes}


def _indexes_by_name(pub_hgnc):
    """Return declared indexes keyed by index name."""
    return {idx.name: idx for idx in pub_hgnc.__table__.indexes}


# ---------------------------------------------------------------------------
# Expected column metadata, transcribed verbatim from pg-g4public.sql.
#   value = (sqlalchemy type class, nullable?)
#   - Every column in the dump lacks NOT NULL, so every column is nullable
#     (PG default). The model must therefore allow None on all columns.
# ---------------------------------------------------------------------------
EXPECTED_COLUMNS: dict[str, tuple[type, bool]] = {
    # --- gene data (gd_*) ---
    "gd_hgnc_id": (Integer, True),
    "gd_app_sym": (String, True),
    "gd_app_sym_sort": (Text, True),
    "gd_app_name": (Text, True),
    "gd_status": (String, True),
    "gd_locus_type": (String, True),
    "gd_prev_sym": (Text, True),
    "gd_prev_name": (Text, True),
    "gd_aliases": (Text, True),
    "gd_name_aliases": (Text, True),
    "gd_pub_chrom_map": (String, True),
    "gd_pub_chrom_map_sort": (String, True),
    "gd_date2app_or_res": (Date, True),
    "gd_date_mod": (Date, True),
    "gd_date_name_change": (Date, True),
    "gd_pub_acc_ids": (Text, True),
    "gd_enz_ids": (Text, True),
    "gd_pub_eg_id": (Integer, True),
    "gd_mgd_id": (Text, True),
    "gd_other_ids": (Text, True),
    "gd_other_ids_list": (Text, True),
    "gd_pubmed_ids": (Text, True),
    "gd_pub_refseq_ids": (Text, True),
    "gd_gene_fam_name": (Text, True),
    "gd_gene_fam_pagename": (Text, True),
    "gd_date_sym_change": (Date, True),
    "gd_record_type": (Text, True),
    "gd_primary_ids": (Text, True),
    "gd_secondary_ids": (Text, True),
    "gd_pub_hseq_id": (String, True),
    "gd_pub_hseq_seq": (Text, True),
    "gd_pub_hseq_molecule": (Text, True),
    "gd_vega_ids": (String, True),
    "gd_lsdb_links": (Text, True),
    "gd_pub_ensembl_id": (String, True),
    "gd_ccds_ids": (Text, True),
    "gd_locus_group": (Text, True),
    "gd_cust_sort": (String, True),
    "gd_gene_fam_links": (Text, True),
    # --- metadata (md_*) ---
    "md_gdb_id": (String, True),
    "md_eg_id": (Integer, True),
    "md_mim_id": (String, True),
    "md_refseq_id": (String, True),
    "md_prot_id": (Text, True),
    "md_ensembl_id": (String, True),
    # (booleans interleaved below)
    "md_vega_id": (String, True),
    "md_rna_central_ids": (Text, True),
    "md_lncipedia": (String, True),
    "md_gtrnadb": (String, True),
    "md_ucsc_id": (String, True),
    "md_rgd_id": (String, True),
    "md_mgd_id": (Text, True),
    "gd_coord": (Text, True),
    "md_agr": (Integer, True),
    "md_alphafold": (Text, True),
}

# Boolean columns (bool in the dump).
BOOLEAN_COLUMNS = {
    "gd_ambiguous",
    "gd_to_review",
    "gd_stable_symbol",
}

# Explicit varchar lengths transcribed from the dump (varchar(N)).
VARCHAR_LENGTHS: dict[str, int] = {
    "gd_app_sym": 50,
    "gd_status": 20,
    "gd_locus_type": 100,
    "gd_pub_chrom_map": 255,
    "gd_pub_chrom_map_sort": 255,
    "gd_pub_hseq_id": 255,
    "gd_vega_ids": 18,
    "gd_pub_ensembl_id": 15,
    "gd_cust_sort": 255,
    "md_gdb_id": 255,
    "md_mim_id": 255,
    "md_refseq_id": 255,
    "md_ensembl_id": 15,
    "md_vega_id": 18,
    "md_lncipedia": 15,
    "md_gtrnadb": 20,
    "md_ucsc_id": 50,
    "md_rgd_id": 50,
}

# All 8 indexes declared on pub_hgnc in the dump, by name.
EXPECTED_INDEXES = {
    "pub_hgnc_gd_app_sym_index",
    "pub_hgnc_gd_hgnc_id_index",
    "pub_hgnc_gd_pub_eg_id_index",
    "pub_hgnc_gd_pub_ensembl_id_index",
    "pub_hgnc_md_agr_index",
    "pub_hgnc_md_eg_id_index",
    "pub_hgnc_md_ensembl_id_index",
    "pub_hgnc_md_vega_id_index",
}


def test_tablename_is_pub_hgnc(pub_hgnc) -> None:
    """``__tablename__`` must be the exact ``pub_hgnc``."""
    assert pub_hgnc.__tablename__ == "pub_hgnc"


def test_full_column_set_matches_dump(pub_hgnc) -> None:
    """Every dump column is present and no extra columns are declared."""
    columns = set(_mapper(pub_hgnc).columns.keys())
    expected = set(EXPECTED_COLUMNS) | BOOLEAN_COLUMNS
    missing = expected - columns
    extra = columns - expected
    assert not missing, f"missing columns: {sorted(missing)}"
    assert not extra, f"unexpected extra columns: {sorted(extra)}"


def test_column_count_matches_dump(pub_hgnc) -> None:
    """Column count must match the dump's 58 columns."""
    assert len(_mapper(pub_hgnc).columns) == len(EXPECTED_COLUMNS) + len(
        BOOLEAN_COLUMNS
    )


@pytest.mark.parametrize("column_name", sorted(EXPECTED_COLUMNS))
def test_column_types_and_nullability(pub_hgnc, column_name: str) -> None:
    """Each non-boolean column has the right Python type and is nullable."""
    col = _column(pub_hgnc, column_name)
    expected_type, expected_nullable = EXPECTED_COLUMNS[column_name]
    assert isinstance(col.type, expected_type), (
        f"{column_name}: expected {expected_type.__name__}, "
        f"got {type(col.type).__name__}"
    )
    assert (
        col.nullable is expected_nullable
    ), f"{column_name}: nullable={col.nullable}, expected {expected_nullable}"


@pytest.mark.parametrize("column_name", sorted(BOOLEAN_COLUMNS))
def test_boolean_columns(pub_hgnc, column_name: str) -> None:
    """``gd_ambiguous``/``gd_to_review``/``gd_stable_symbol`` are Boolean."""
    col = _column(pub_hgnc, column_name)
    assert isinstance(
        col.type, Boolean
    ), f"{column_name}: expected Boolean, got {type(col.type).__name__}"
    assert col.nullable is True, f"{column_name} must be nullable"


@pytest.mark.parametrize("column_name", sorted(VARCHAR_LENGTHS))
def test_varchar_lengths(pub_hgnc, column_name: str) -> None:
    """``varchar(N)`` columns carry the dump's length."""
    col = _column(pub_hgnc, column_name)
    assert isinstance(col.type, String), column_name
    assert col.type.length == VARCHAR_LENGTHS[column_name], (
        f"{column_name}: length={col.type.length}, "
        f"expected {VARCHAR_LENGTHS[column_name]}"
    )


@pytest.mark.parametrize(
    "column_name",
    [
        "gd_date2app_or_res",
        "gd_date_mod",
        "gd_date_name_change",
        "gd_date_sym_change",
    ],
)
def test_date_columns(pub_hgnc, column_name: str) -> None:
    """Date columns map to ``Date``."""
    col = _column(pub_hgnc, column_name)
    assert isinstance(col.type, Date), column_name
    assert col.type.python_type is date


@pytest.mark.parametrize("column_name", ["gd_pub_eg_id", "md_eg_id", "md_agr"])
def test_integer_columns(pub_hgnc, column_name: str) -> None:
    """``int4`` columns map to ``Integer``."""
    col = _column(pub_hgnc, column_name)
    assert isinstance(col.type, Integer), column_name


@pytest.mark.parametrize("column_name", ["md_prot_id", "gd_aliases"])
def test_text_columns(pub_hgnc, column_name: str) -> None:
    """``text`` columns map to ``Text``."""
    col = _column(pub_hgnc, column_name)
    assert isinstance(col.type, Text), column_name


def test_gd_hgnc_id_is_forced_orm_primary_key(pub_hgnc) -> None:
    """``gd_hgnc_id`` is the forced ORM PK (only an index in the DB)."""
    pk_columns = [c.name for c in _mapper(pub_hgnc).primary_key]
    assert pk_columns == ["gd_hgnc_id"]


def test_all_eight_indexes_declared_by_name(pub_hgnc) -> None:
    """All 8 documented indexes are declared, by name."""
    missing = EXPECTED_INDEXES - _index_names(pub_hgnc)
    assert not missing, f"missing indexes: {sorted(missing)}"


def test_exactly_eight_indexes(pub_hgnc) -> None:
    """No extra indexes beyond the 8 documented ones."""
    extra = _index_names(pub_hgnc) - EXPECTED_INDEXES
    assert not extra, f"unexpected extra indexes: {sorted(extra)}"


def test_md_agr_index_targets_md_agr(pub_hgnc) -> None:
    """``pub_hgnc_md_agr_index`` (called out in the spec) covers ``md_agr``."""
    idx = _indexes_by_name(pub_hgnc)["pub_hgnc_md_agr_index"]
    assert [c.name for c in idx.columns] == ["md_agr"]


def test_model_is_instantiable(pub_hgnc) -> None:
    """The model can be instantiated with representative data."""
    gene = pub_hgnc(gd_hgnc_id=1, gd_app_sym="A1BG", gd_ambiguous=True)
    assert gene.gd_hgnc_id == 1
    assert gene.gd_app_sym == "A1BG"
    assert gene.gd_ambiguous is True
