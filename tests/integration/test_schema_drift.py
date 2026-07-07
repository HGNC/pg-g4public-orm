"""Integration schema-drift guard for ORM-vs-PostgreSQL fidelity."""

from __future__ import annotations

from collections.abc import Iterable

import pytest
from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
    DateTime,
    Integer,
    String,
    Text,
    create_engine,
    inspect,
)

from pg_g4public_orm.core.base import DeclarativeBase
from pg_g4public_orm.models import (
    Cell,
    Comment,
    Ensembl2Hgnc,
    ExternalResource,
    FamilyAlias,
    FamilyHasExternalResource,
    FamilyHasSpecialist,
    FamilyNew,
    Filestore,
    Gencc,
    GeneHasFamily,
    HcopOrthologs,
    Hierarchy,
    HierarchyClosure,
    Import,
    LocusStats,
    LocusStatsChr,
    Mane,
    PubHgnc,
    Specialist,
)

ALL_MODELS: tuple[type[DeclarativeBase], ...] = (
    Cell,
    Comment,
    Ensembl2Hgnc,
    ExternalResource,
    FamilyAlias,
    FamilyHasExternalResource,
    FamilyHasSpecialist,
    FamilyNew,
    Filestore,
    Gencc,
    GeneHasFamily,
    HcopOrthologs,
    Hierarchy,
    HierarchyClosure,
    Import,
    LocusStats,
    LocusStatsChr,
    Mane,
    PubHgnc,
    Specialist,
)

EXPECTED_MODEL_PRIMARY_KEYS: dict[str, tuple[str, ...]] = {
    "cell": ("cell_id",),
    "comment": ("hgnc_id", "note"),
    "ensembl2hgnc": ("e2h_ensembl_gene_id", "e2h_hgnc_id"),
    "external_resource": ("id",),
    "family_alias": ("id",),
    "family_has_external_resource": ("family_id", "ext_id"),
    "family_has_specialist": ("fam_id", "specialist_id"),
    "family_new": ("id",),
    "filestore": ("line_id",),
    "gencc": ("uuid", "hgnc_id", "disease_id"),
    "gene_has_family": ("hgnc_id", "family_id"),
    "hcop_orthologs": ("orth_id",),
    "hierarchy": ("parent_fam_id", "child_fam_id"),
    "hierarchy_closure": ("parent_fam_id", "child_fam_id", "distance"),
    "import": ("imp_id",),
    "locus_stats": ("ls_type", "ls_group", "ls_source"),
    "locus_stats_chr": ("ls_chr", "ls_type", "ls_group", "ls_source"),
    "mane": ("id",),
    "pub_hgnc": ("gd_hgnc_id",),
    "specialist": ("id",),
}

EXPECTED_DB_PRIMARY_KEYS: dict[str, tuple[str, ...]] = {
    "external_resource": ("id",),
    "family_alias": ("id",),
    "family_has_external_resource": ("family_id", "ext_id"),
    "family_has_specialist": ("fam_id", "specialist_id"),
    "family_new": ("id",),
    "gene_has_family": ("hgnc_id", "family_id"),
    "hierarchy": ("parent_fam_id", "child_fam_id"),
    "hierarchy_closure": ("parent_fam_id", "child_fam_id", "distance"),
    "mane": ("id",),
    "specialist": ("id",),
}

EXPECTED_FOREIGN_KEYS: dict[
    str,
    set[tuple[str, tuple[str, ...], str, tuple[str, ...]]],
] = {
    "family_alias": {
        ("fk_family_alias_family_new_1", ("family_id",), "family_new", ("id",)),
    },
    "family_has_external_resource": {
        (
            "fk_family_has_external_resource_external_resource_1",
            ("ext_id",),
            "external_resource",
            ("id",),
        ),
        (
            "fk_family_has_external_resource_family_new_1",
            ("family_id",),
            "family_new",
            ("id",),
        ),
    },
    "family_has_specialist": {
        (
            "fk_family_has_specialist_family_new_1",
            ("fam_id",),
            "family_new",
            ("id",),
        ),
        (
            "fk_family_has_specialist_specialist_1",
            ("specialist_id",),
            "specialist",
            ("id",),
        ),
    },
    "gene_has_family": {
        ("fk_gene_has_family_family_new_1", ("family_id",), "family_new", ("id",)),
    },
    "hierarchy": {
        (
            "fk_hierarchy_family_new_1",
            ("parent_fam_id",),
            "family_new",
            ("id",),
        ),
        (
            "fk_hierarchy_family_new_2",
            ("child_fam_id",),
            "family_new",
            ("id",),
        ),
    },
    "hierarchy_closure": {
        (
            "fk_hierarchy_closure_family_new_1",
            ("parent_fam_id",),
            "family_new",
            ("id",),
        ),
        (
            "fk_hierarchy_closure_family_new_2",
            ("child_fam_id",),
            "family_new",
            ("id",),
        ),
    },
}


def _normalize_type(column_type: object) -> tuple[str, int | None]:
    if isinstance(column_type, Text):
        return ("text", None)
    if isinstance(column_type, BigInteger):
        return ("bigint", None)
    if isinstance(column_type, Integer):
        return ("integer", None)
    if isinstance(column_type, Boolean):
        return ("boolean", None)
    if isinstance(column_type, DateTime):
        return ("timestamp", None)
    if isinstance(column_type, Date):
        return ("date", None)
    if isinstance(column_type, String):
        return ("varchar", column_type.length)
    return (type(column_type).__name__.lower(), None)


def _pk_cols(model: type[DeclarativeBase]) -> tuple[str, ...]:
    return tuple(column.name for column in model.__table__.primary_key.columns)


def _index_names(model: type[DeclarativeBase]) -> set[str]:
    return {index.name for index in model.__table__.indexes if index.name is not None}


def _column_names(model: type[DeclarativeBase]) -> set[str]:
    return {column.name for column in model.__table__.columns}


def _fk_signature(
    rows: Iterable[dict[str, object]],
) -> set[tuple[str, tuple[str, ...], str, tuple[str, ...]]]:
    signatures: set[tuple[str, tuple[str, ...], str, tuple[str, ...]]] = set()
    for row in rows:
        signatures.add(
            (
                str(row["name"]),
                tuple(row["constrained_columns"]),
                str(row["referred_table"]),
                tuple(row["referred_columns"]),
            )
        )
    return signatures


@pytest.mark.integration
def test_schema_drift_against_reflected_postgres_schema(
    loaded_schema_connection,
    postgres_container,
) -> None:
    """Every model must match reflected table columns/types/nullability/PK/indexes."""
    _ = loaded_schema_connection  # ensures schema is loaded for this test function

    db_url = postgres_container.get_connection_url().replace(
        "postgresql+psycopg2://", "postgresql+psycopg://"
    )
    engine = create_engine(db_url)

    try:
        inspector = inspect(engine)

        for model in ALL_MODELS:
            table_name = model.__tablename__

            db_columns = {
                row["name"]: row
                for row in inspector.get_columns(table_name, schema="public")
            }
            model_columns = {column.name: column for column in model.__table__.columns}

            assert set(db_columns) == _column_names(model), (
                f"column-name drift in {table_name}: "
                f"db={sorted(db_columns)} model={sorted(model_columns)}"
            )

            for column_name, model_column in model_columns.items():
                reflected = db_columns[column_name]

                assert reflected["nullable"] == model_column.nullable, (
                    f"nullability drift in {table_name}.{column_name}: "
                    f"db={reflected['nullable']} model={model_column.nullable}"
                )

                db_type = _normalize_type(reflected["type"])
                model_type = _normalize_type(model_column.type)
                assert db_type == model_type, (
                    f"type drift in {table_name}.{column_name}: "
                    f"db={db_type} model={model_type}"
                )

            reflected_pk = tuple(
                inspector.get_pk_constraint(table_name, schema="public").get(
                    "constrained_columns", []
                )
            )
            expected_db_pk = EXPECTED_DB_PRIMARY_KEYS.get(table_name, ())
            assert reflected_pk == expected_db_pk, (
                f"DB PK drift in {table_name}: "
                f"db={reflected_pk} expected={expected_db_pk}"
            )

            expected_model_pk = EXPECTED_MODEL_PRIMARY_KEYS[table_name]
            assert _pk_cols(model) == expected_model_pk, (
                f"model PK drift in {table_name}: "
                f"model={_pk_cols(model)} expected={expected_model_pk}"
            )

            reflected_indexes = {
                index["name"]
                for index in inspector.get_indexes(table_name, schema="public")
            }
            assert reflected_indexes == _index_names(model), (
                f"index-name drift in {table_name}: "
                f"db={sorted(reflected_indexes)} model={sorted(_index_names(model))}"
            )
    finally:
        engine.dispose()


@pytest.mark.integration
def test_reflected_foreign_keys_match_expected_10_constraints(
    loaded_schema_connection,
    postgres_container,
) -> None:
    """The reflected curated schema must expose the expected 10 FK constraints."""
    _ = loaded_schema_connection

    db_url = postgres_container.get_connection_url().replace(
        "postgresql+psycopg2://", "postgresql+psycopg://"
    )
    engine = create_engine(db_url)

    try:
        inspector = inspect(engine)

        reflected_by_table: dict[
            str,
            set[tuple[str, tuple[str, ...], str, tuple[str, ...]]],
        ] = {}
        total = 0

        for table_name in sorted({model.__tablename__ for model in ALL_MODELS}):
            reflected = _fk_signature(
                inspector.get_foreign_keys(table_name, schema="public")
            )
            if reflected:
                reflected_by_table[table_name] = reflected
                total += len(reflected)

        assert reflected_by_table == EXPECTED_FOREIGN_KEYS
        assert total == 10
    finally:
        engine.dispose()
