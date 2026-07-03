"""``mane`` ORM model — MANE Select/Plus clinical transcript records.

Maps the existing ``g4public.mane`` schema (PostgreSQL). Column types,
nullability, the real database primary key and the declared indexes are
transcribed verbatim from the authoritative Navicat dump
``.ai/specs/pg-g4public.sql``. The ORM reads and writes **data only** — it
never creates, alters, or drops schema objects (``primary_key=True`` and the
declared indexes emit no DDL).

.. note::

   The column ``grch38_chr_starnd`` is a **real typo in the source schema**
   (should be ``grch38_chr_strand``). The model MUST use the exact misspelled
   name or the schema-drift guard (T11) fails. Never "fix" it.
"""

from __future__ import annotations

from sqlalchemy import Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from pg_g4public_orm.core.base import DeclarativeBase


class Mane(DeclarativeBase):
    """MANE (Matched Annotation from NCBI and EBI) transcript record.

    ``id`` is a real database primary key (``mane_pk``). ``ensembl_gene``,
    ``refseq_nuc_acc``, ``ensembl_nuc_acc`` and ``mane_status`` are NOT NULL in
    the dump; the remaining columns are nullable. The misspelled
    ``grch38_chr_starnd`` is ``varchar(1)`` per the source schema.
    """

    __tablename__ = "mane"
    __table_args__ = (
        Index("mane_ensembl_gene_idx", "ensembl_gene"),
        Index("mane_ncbi_gene_idx", "ncbi_gene_id"),
    )

    # --- Primary key (real DB PK; not sequence-backed) ---
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # --- Identifiers ---
    ncbi_gene_id: Mapped[int] = mapped_column(Integer)
    ensembl_gene: Mapped[str] = mapped_column(String(20))
    hgnc_id: Mapped[int | None] = mapped_column(Integer)

    # --- Gene labels ---
    symbol: Mapped[str | None] = mapped_column(String(50))
    gene_name: Mapped[str | None] = mapped_column(Text)

    # --- Transcript accessions ---
    refseq_nuc_acc: Mapped[str] = mapped_column(String(20))
    refseq_prot_acc: Mapped[str | None] = mapped_column(String(20))
    ensembl_nuc_acc: Mapped[str] = mapped_column(String(20))
    ensembl_prot_acc: Mapped[str | None] = mapped_column(String(20))

    # --- Status + coordinates ---
    mane_status: Mapped[str] = mapped_column(String(30))
    grch38_chr: Mapped[str | None] = mapped_column(String(15))
    grch38_chr_start: Mapped[int | None] = mapped_column(Integer)
    grch38_chr_end: Mapped[int | None] = mapped_column(Integer)
    # NOTE: literal source-schema typo "starnd" — preserved verbatim, do NOT fix.
    grch38_chr_starnd: Mapped[str | None] = mapped_column(String(1))
