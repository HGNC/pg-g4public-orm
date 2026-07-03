"""``hcop_orthologs`` ORM model — HCOP pairwise ortholog records.

Maps the existing ``g4public.hcop_orthologs`` schema (PostgreSQL). Column types
and nullability are transcribed verbatim from the authoritative Navicat dump
``.ai/specs/pg-g4public.sql``. The ORM reads and writes **data only** — it
never creates, alters, or drops schema objects (``primary_key=True`` emits no
DDL).

The dump defines **no database primary key** for this table, but
``orth_id`` is NOT NULL ``int8``; per the primary-key convention it is the
forced ORM primary key (emits no DDL). ``class_a``/``class_b`` are plain
``varchar(8)`` in PostgreSQL — **NOT** ``ENUM`` types (this deliberately
diverges from the MySQL sibling ``my-g4public-orm``).
"""

from __future__ import annotations

from sqlalchemy import BigInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from pg_g4public_orm.core.base import DeclarativeBase


class HcopOrthologs(DeclarativeBase):
    """HCOP (HCOP Comparison of Orthology Predictions) pairwise ortholog row.

    ``orth_id`` (``int8`` NOT NULL, no DB PK) is the forced ORM primary key.
    ``taxon_a``/``taxon_b``/``sort_order`` are also ``int8`` -> ``BigInteger``;
    ``class_a``/``class_b`` are plain ``varchar(8)`` (PG — not enums);
    ``name_a``/``name_b``/``text_link_a``/``text_link_b`` are ``text``. The
    NOT NULL columns are ``taxon_a``/``taxon_b``, ``db_id_a``/``db_id_b``,
    ``ensembl_a``/``ensembl_b``, ``support``, ``text_link_a``/``text_link_b``
    and ``sort_order``.
    """

    __tablename__ = "hcop_orthologs"

    # --- Primary key (int8 NOT NULL, no DB PK -> forced ORM key) ---
    orth_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    # --- Taxonomy (int8 -> BigInteger, NOT NULL) ---
    taxon_a: Mapped[int] = mapped_column(BigInteger)
    taxon_b: Mapped[int] = mapped_column(BigInteger)

    # --- Cross-database identifiers ---
    db_id_a: Mapped[str] = mapped_column(String(255))
    db_id_b: Mapped[str] = mapped_column(String(255))
    vgnc_a: Mapped[str | None] = mapped_column(String(15))
    vgnc_b: Mapped[str | None] = mapped_column(String(255))
    ensembl_a: Mapped[str] = mapped_column(String(28))
    ensembl_b: Mapped[str] = mapped_column(String(28))
    entrez_a: Mapped[str | None] = mapped_column(String(28))
    entrez_b: Mapped[str | None] = mapped_column(String(28))

    # --- Symbol + gene names ---
    symbol_a: Mapped[str | None] = mapped_column(String(255))
    symbol_b: Mapped[str | None] = mapped_column(String(255))
    symbol_source_a: Mapped[str | None] = mapped_column(String(128))
    symbol_source_b: Mapped[str | None] = mapped_column(String(128))
    name_a: Mapped[str | None] = mapped_column(Text)
    name_b: Mapped[str | None] = mapped_column(Text)

    # --- Source / locus metadata ---
    source_name_a: Mapped[str | None] = mapped_column(String(128))
    source_name_b: Mapped[str | None] = mapped_column(String(128))
    locus_type_a: Mapped[str | None] = mapped_column(String(255))
    locus_type_b: Mapped[str | None] = mapped_column(String(255))
    locus_source_a: Mapped[str | None] = mapped_column(String(128))
    locus_source_b: Mapped[str | None] = mapped_column(String(128))

    # --- class_a / class_b: plain varchar(8), NOT enum (PG divergence) ---
    class_a: Mapped[str | None] = mapped_column(String(8))
    class_b: Mapped[str | None] = mapped_column(String(8))

    # --- Chromosomes / support / links ---
    chr_a: Mapped[str | None] = mapped_column(String(128))
    chr_b: Mapped[str | None] = mapped_column(String(128))
    support: Mapped[str] = mapped_column(String(255))
    text_link_a: Mapped[str] = mapped_column(Text)
    text_link_b: Mapped[str] = mapped_column(Text)
    sort_order: Mapped[int] = mapped_column(BigInteger)
