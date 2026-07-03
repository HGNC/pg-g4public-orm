"""Tests for the gene cross-reference + transcript models.

Models covered: ``comment``, ``gencc``, ``ensembl2hgnc``, ``mane``.

Driven by the authoritative dump ``.ai/specs/pg-g4public.sql`` (the real
Navicat DDL of ``g4public``). These are unit tests asserting SQLAlchemy
metadata (table names, column sets, types, nullability, the forced ORM
composite / database primary keys, and the declared indexes) — no database
required.
"""

from __future__ import annotations

import pytest
from sqlalchemy import Integer, String, Text, inspect


# ---------------------------------------------------------------------------
# Helpers (mirrors tests/unit/models/core/test_cell_and_stats.py)
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
    """Return declared index names for a model's mapped table."""
    return {idx.name for idx in model.__table__.indexes}


def _indexes_by_name(model):
    """Return declared indexes keyed by index name."""
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
# Comment
# ===========================================================================
@pytest.fixture(scope="module")
def comment():
    """Import the model lazily so collection succeeds before it exists."""
    from pg_g4public_orm.models.core.comment import Comment

    return Comment


EXPECTED_COMMENT_COLUMNS: dict[str, tuple[type, bool]] = {
    "hgnc_id": (Integer, False),
    "note": (Text, True),
}


def test_comment_tablename(comment) -> None:
    """``__tablename__`` must be the exact ``comment``."""
    assert comment.__tablename__ == "comment"


def test_comment_full_column_set(comment) -> None:
    """Every dump column is present and no extra columns are declared."""
    _assert_full_column_set(comment, EXPECTED_COMMENT_COLUMNS)


@pytest.mark.parametrize("column_name", sorted(EXPECTED_COMMENT_COLUMNS))
def test_comment_column_types_and_nullability(comment, column_name: str) -> None:
    """Each column has the right type and nullability per the dump."""
    _assert_column_type_and_nullability(comment, column_name, EXPECTED_COMMENT_COLUMNS)


def test_comment_hgnc_id_is_not_nullable(comment) -> None:
    """``hgnc_id`` is NOT NULL in the dump."""
    assert _column(comment, "hgnc_id").nullable is False


def test_comment_note_is_nullable(comment) -> None:
    """``note`` is nullable ``text`` in the dump."""
    assert _column(comment, "note").nullable is True


def test_comment_composite_pk(comment) -> None:
    """ORM-only composite PK on (hgnc_id, note) — no usable unique column."""
    assert _pk_columns(comment) == ["hgnc_id", "note"]


def test_comment_is_instantiable(comment) -> None:
    """The model can be instantiated with representative data."""
    row = comment(hgnc_id=1234, note="A curator note")
    assert row.hgnc_id == 1234
    assert row.note == "A curator note"


# ===========================================================================
# GenCC
# ===========================================================================
@pytest.fixture(scope="module")
def gencc():
    """Import the model lazily so collection succeeds before it exists."""
    from pg_g4public_orm.models.core.gencc import Gencc

    return Gencc


EXPECTED_GENCC_COLUMNS: dict[str, tuple[type, bool]] = {
    "uuid": (String, True),
    "hgnc_id": (Integer, True),
    "disease_id": (String, True),
    "disease_title": (Text, True),
    "omim_id": (Integer, True),
}


def test_gencc_tablename(gencc) -> None:
    """``__tablename__`` must be the exact ``gencc``."""
    assert gencc.__tablename__ == "gencc"


def test_gencc_full_column_set(gencc) -> None:
    """Every dump column is present and no extra columns are declared."""
    _assert_full_column_set(gencc, EXPECTED_GENCC_COLUMNS)


@pytest.mark.parametrize("column_name", sorted(EXPECTED_GENCC_COLUMNS))
def test_gencc_column_types_and_nullability(gencc, column_name: str) -> None:
    """Each column has the right type and nullability per the dump."""
    _assert_column_type_and_nullability(gencc, column_name, EXPECTED_GENCC_COLUMNS)


def test_gencc_uuid_is_nullable_varchar(gencc) -> None:
    """``uuid`` is nullable, unbounded ``varchar`` per the dump."""
    col = _column(gencc, "uuid")
    assert isinstance(col.type, String)
    assert col.type.length is None
    assert col.nullable is True


def test_gencc_disease_title_is_text(gencc) -> None:
    """``disease_title`` is ``text`` per the dump."""
    col = _column(gencc, "disease_title")
    assert isinstance(col.type, Text)


def test_gencc_composite_pk(gencc) -> None:
    """ORM-only composite PK on (uuid, hgnc_id, disease_id)."""
    assert _pk_columns(gencc) == ["uuid", "hgnc_id", "disease_id"]


def test_gencc_is_instantiable(gencc) -> None:
    """The model can be instantiated with representative data."""
    row = gencc(uuid="abc-123", hgnc_id=1, disease_id="MONDO:0007254")
    assert row.uuid == "abc-123"
    assert row.hgnc_id == 1


# ===========================================================================
# Ensembl2Hgnc
# ===========================================================================
@pytest.fixture(scope="module")
def ensembl2hgnc():
    """Import the model lazily so collection succeeds before it exists."""
    from pg_g4public_orm.models.core.ensembl2hgnc import Ensembl2Hgnc

    return Ensembl2Hgnc


EXPECTED_ENSEMBL2HGNC_COLUMNS: dict[str, tuple[type, bool]] = {
    "e2h_hgnc_id": (String, True),
    "e2h_app_sym": (String, True),
    "e2h_ensembl_gene_id": (String, True),
}

ENSEMBL2HGNC_VARCHAR_LENGTHS: dict[str, int] = {
    "e2h_hgnc_id": 50,
    "e2h_app_sym": 50,
    "e2h_ensembl_gene_id": 50,
}


def test_ensembl2hgnc_tablename(ensembl2hgnc) -> None:
    """``__tablename__`` must be the exact ``ensembl2hgnc``."""
    assert ensembl2hgnc.__tablename__ == "ensembl2hgnc"


def test_ensembl2hgnc_full_column_set(ensembl2hgnc) -> None:
    """Every dump column is present and no extra columns are declared."""
    _assert_full_column_set(ensembl2hgnc, EXPECTED_ENSEMBL2HGNC_COLUMNS)


@pytest.mark.parametrize("column_name", sorted(EXPECTED_ENSEMBL2HGNC_COLUMNS))
def test_ensembl2hgnc_column_types_and_nullability(
    ensembl2hgnc, column_name: str
) -> None:
    """Each column has the right type and nullability per the dump."""
    _assert_column_type_and_nullability(
        ensembl2hgnc, column_name, EXPECTED_ENSEMBL2HGNC_COLUMNS
    )


@pytest.mark.parametrize("column_name", sorted(ENSEMBL2HGNC_VARCHAR_LENGTHS))
def test_ensembl2hgnc_varchar_lengths(ensembl2hgnc, column_name: str) -> None:
    """``varchar(N)`` columns carry the dump's length (all 50)."""
    col = _column(ensembl2hgnc, column_name)
    assert isinstance(col.type, String), column_name
    assert col.type.length == ENSEMBL2HGNC_VARCHAR_LENGTHS[column_name]


def test_ensembl2hgnc_e2h_hgnc_id_is_string_50(ensembl2hgnc) -> None:
    """``e2h_hgnc_id`` is ``varchar(50)`` (spec calls this out explicitly)."""
    col = _column(ensembl2hgnc, "e2h_hgnc_id")
    assert isinstance(col.type, String)
    assert col.type.length == 50


def test_ensembl2hgnc_composite_pk(ensembl2hgnc) -> None:
    """ORM-only composite PK on (e2h_ensembl_gene_id, e2h_hgnc_id)."""
    assert _pk_columns(ensembl2hgnc) == ["e2h_ensembl_gene_id", "e2h_hgnc_id"]


def test_ensembl2hgnc_is_instantiable(ensembl2hgnc) -> None:
    """The model can be instantiated with representative data."""
    row = ensembl2hgnc(
        e2h_hgnc_id="HGNC:5", e2h_app_sym="A1BG", e2h_ensembl_gene_id="ENSG00000121410"
    )
    assert row.e2h_hgnc_id == "HGNC:5"
    assert row.e2h_ensembl_gene_id == "ENSG00000121410"


# ===========================================================================
# Mane
# ===========================================================================
@pytest.fixture(scope="module")
def mane():
    """Import the model lazily so collection succeeds before it exists."""
    from pg_g4public_orm.models.core.mane import Mane

    return Mane


# All 15 mane columns transcribed verbatim from pg-g4public.sql.
EXPECTED_MANE_COLUMNS: dict[str, tuple[type, bool]] = {
    "ncbi_gene_id": (Integer, False),
    "ensembl_gene": (String, False),
    "hgnc_id": (Integer, True),
    "symbol": (String, True),
    "gene_name": (Text, True),
    "refseq_nuc_acc": (String, False),
    "refseq_prot_acc": (String, True),
    "ensembl_nuc_acc": (String, False),
    "ensembl_prot_acc": (String, True),
    "mane_status": (String, False),
    "grch38_chr": (String, True),
    "grch38_chr_start": (Integer, True),
    "grch38_chr_end": (Integer, True),
    "grch38_chr_starnd": (String, True),
    "id": (Integer, False),
}

MANE_VARCHAR_LENGTHS: dict[str, int] = {
    "ensembl_gene": 20,
    "symbol": 50,
    "refseq_nuc_acc": 20,
    "refseq_prot_acc": 20,
    "ensembl_nuc_acc": 20,
    "ensembl_prot_acc": 20,
    "mane_status": 30,
    "grch38_chr": 15,
    "grch38_chr_starnd": 1,
}

# Columns called out as NOT NULL in the dump (besides the PK id).
MANE_NOT_NULL_COLUMNS = {
    "ncbi_gene_id",
    "ensembl_gene",
    "refseq_nuc_acc",
    "ensembl_nuc_acc",
    "mane_status",
    "id",
}

EXPECTED_MANE_INDEXES = {
    "mane_ensembl_gene_idx",
    "mane_ncbi_gene_idx",
}


def test_mane_tablename(mane) -> None:
    """``__tablename__`` must be the exact ``mane``."""
    assert mane.__tablename__ == "mane"


def test_mane_full_column_set(mane) -> None:
    """Every dump column is present and no extra columns are declared."""
    _assert_full_column_set(mane, EXPECTED_MANE_COLUMNS)


def test_mane_column_count_is_15(mane) -> None:
    """``mane`` has exactly 15 columns per the dump."""
    assert len(inspect(mane).columns) == 15


@pytest.mark.parametrize("column_name", sorted(EXPECTED_MANE_COLUMNS))
def test_mane_column_types_and_nullability(mane, column_name: str) -> None:
    """Each column has the right type and nullability per the dump."""
    _assert_column_type_and_nullability(mane, column_name, EXPECTED_MANE_COLUMNS)


@pytest.mark.parametrize("column_name", sorted(MANE_NOT_NULL_COLUMNS))
def test_mane_not_null_columns(mane, column_name: str) -> None:
    """The NOT NULL columns (incl. PK) are non-nullable per the dump."""
    assert _column(mane, column_name).nullable is False


@pytest.mark.parametrize("column_name", sorted(MANE_VARCHAR_LENGTHS))
def test_mane_varchar_lengths(mane, column_name: str) -> None:
    """``varchar(N)`` columns carry the dump's length."""
    col = _column(mane, column_name)
    assert isinstance(col.type, String), column_name
    assert col.type.length == MANE_VARCHAR_LENGTHS[column_name], (
        f"{column_name}: length={col.type.length}, "
        f"expected {MANE_VARCHAR_LENGTHS[column_name]}"
    )


def test_mane_grch38_chr_starnd_typo_column(mane) -> None:
    """The literal typo column ``grch38_chr_starnd`` is ``varchar(1)``.

    The source schema misspells "strand" as "starnd"; the model MUST use the
    exact misspelled name or the drift guard fails. Never "fix" it.
    """
    assert "grch38_chr_starnd" in _column_names(mane)
    assert "grch38_chr_strand" not in _column_names(mane)
    col = _column(mane, "grch38_chr_starnd")
    assert isinstance(col.type, String)
    assert col.type.length == 1


def test_mane_id_is_primary_key(mane) -> None:
    """``id`` is the database primary key (``mane_pk``) per the dump."""
    assert _pk_columns(mane) == ["id"]


def test_mane_id_is_not_nullable(mane) -> None:
    """``id`` is NOT NULL in the dump."""
    assert _column(mane, "id").nullable is False


def test_mane_declares_both_indexes_by_name(mane) -> None:
    """Both documented indexes are declared, by name."""
    missing = EXPECTED_MANE_INDEXES - _index_names(mane)
    assert not missing, f"missing indexes: {sorted(missing)}"


def test_mane_no_extra_indexes(mane) -> None:
    """No indexes beyond the 2 documented ones."""
    extra = _index_names(mane) - EXPECTED_MANE_INDEXES
    assert not extra, f"unexpected extra indexes: {sorted(extra)}"


def test_mane_ensembl_gene_idx_targets_ensembl_gene(mane) -> None:
    """``mane_ensembl_gene_idx`` covers the ``ensembl_gene`` column."""
    idx = _indexes_by_name(mane)["mane_ensembl_gene_idx"]
    assert [c.name for c in idx.columns] == ["ensembl_gene"]


def test_mane_ncbi_gene_idx_targets_ncbi_gene_id(mane) -> None:
    """``mane_ncbi_gene_idx`` covers the ``ncbi_gene_id`` column."""
    idx = _indexes_by_name(mane)["mane_ncbi_gene_idx"]
    assert [c.name for c in idx.columns] == ["ncbi_gene_id"]


def test_mane_is_instantiable(mane) -> None:
    """The model can be instantiated with representative (NOT NULL) data."""
    row = mane(
        id=1,
        ncbi_gene_id=1,
        ensembl_gene="ENSG00000121410",
        refseq_nuc_acc="NM_001206",
        ensembl_nuc_acc="ENST00000295531",
        mane_status="MANE Select",
        grch38_chr_starnd="+",
    )
    assert row.id == 1
    assert row.ensembl_gene == "ENSG00000121410"
    assert row.mane_status == "MANE Select"
    assert row.grch38_chr_starnd == "+"
