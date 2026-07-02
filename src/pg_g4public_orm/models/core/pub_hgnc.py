"""``pub_hgnc`` ORM model — the central public gene table (~58 columns).

Maps the existing ``g4public.pub_hgnc`` schema (PostgreSQL). Column types,
nullability and index names are transcribed verbatim from the authoritative
Navicat dump ``.ai/specs/pg-g4public.sql``. The ORM reads and writes **data
only** — it never creates, alters, or drops schema objects (no
``ForeignKey``/``relationship()`` in v1, and the declared indexes emit no DDL).
"""

from __future__ import annotations

from datetime import date

from sqlalchemy import (
    Boolean,
    Date,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from pg_g4public_orm.core.base import DeclarativeBase


class PubHgnc(DeclarativeBase):
    """Public HGNC gene record (one row per approved gene symbol).

    ``gd_hgnc_id`` is only covered by an index in the database (no real
    ``PRIMARY KEY`` exists on the table), but it is the de-facto key — so the
    ORM forces it as the primary key for identity/lookups. Forcing the PK emits
    no DDL; the schema is never modified.
    """

    __tablename__ = "pub_hgnc"
    __table_args__ = (
        Index("pub_hgnc_gd_app_sym_index", "gd_app_sym"),
        Index("pub_hgnc_gd_hgnc_id_index", "gd_hgnc_id"),
        Index("pub_hgnc_gd_pub_eg_id_index", "gd_pub_eg_id"),
        Index("pub_hgnc_gd_pub_ensembl_id_index", "gd_pub_ensembl_id"),
        Index("pub_hgnc_md_agr_index", "md_agr"),
        Index("pub_hgnc_md_eg_id_index", "md_eg_id"),
        Index("pub_hgnc_md_ensembl_id_index", "md_ensembl_id"),
        Index("pub_hgnc_md_vega_id_index", "md_vega_id"),
    )

    # --- Primary key (de-facto; no DB PK, forced for ORM identity) ---
    gd_hgnc_id: Mapped[int | None] = mapped_column(Integer, primary_key=True)

    # --- Gene data (gd_*) ---
    gd_app_sym: Mapped[str | None] = mapped_column(String(50))
    gd_app_sym_sort: Mapped[str | None] = mapped_column(Text)
    gd_app_name: Mapped[str | None] = mapped_column(Text)
    gd_status: Mapped[str | None] = mapped_column(String(20))
    gd_locus_type: Mapped[str | None] = mapped_column(String(100))
    gd_prev_sym: Mapped[str | None] = mapped_column(Text)
    gd_prev_name: Mapped[str | None] = mapped_column(Text)
    gd_aliases: Mapped[str | None] = mapped_column(Text)
    gd_name_aliases: Mapped[str | None] = mapped_column(Text)
    gd_pub_chrom_map: Mapped[str | None] = mapped_column(String(255))
    gd_pub_chrom_map_sort: Mapped[str | None] = mapped_column(String(255))
    gd_date2app_or_res: Mapped[date | None] = mapped_column(Date)
    gd_date_mod: Mapped[date | None] = mapped_column(Date)
    gd_date_name_change: Mapped[date | None] = mapped_column(Date)
    gd_pub_acc_ids: Mapped[str | None] = mapped_column(Text)
    gd_enz_ids: Mapped[str | None] = mapped_column(Text)
    gd_pub_eg_id: Mapped[int | None] = mapped_column(Integer)
    gd_mgd_id: Mapped[str | None] = mapped_column(Text)
    gd_other_ids: Mapped[str | None] = mapped_column(Text)
    gd_other_ids_list: Mapped[str | None] = mapped_column(Text)
    gd_pubmed_ids: Mapped[str | None] = mapped_column(Text)
    gd_pub_refseq_ids: Mapped[str | None] = mapped_column(Text)
    gd_gene_fam_name: Mapped[str | None] = mapped_column(Text)
    gd_gene_fam_pagename: Mapped[str | None] = mapped_column(Text)
    gd_date_sym_change: Mapped[date | None] = mapped_column(Date)
    gd_record_type: Mapped[str | None] = mapped_column(Text)
    gd_primary_ids: Mapped[str | None] = mapped_column(Text)
    gd_secondary_ids: Mapped[str | None] = mapped_column(Text)
    gd_pub_hseq_id: Mapped[str | None] = mapped_column(String(255))
    gd_pub_hseq_seq: Mapped[str | None] = mapped_column(Text)
    gd_pub_hseq_molecule: Mapped[str | None] = mapped_column(Text)
    gd_vega_ids: Mapped[str | None] = mapped_column(String(18))
    gd_lsdb_links: Mapped[str | None] = mapped_column(Text)
    gd_pub_ensembl_id: Mapped[str | None] = mapped_column(String(15))
    gd_ccds_ids: Mapped[str | None] = mapped_column(Text)
    gd_locus_group: Mapped[str | None] = mapped_column(Text)
    gd_cust_sort: Mapped[str | None] = mapped_column(String(255))
    gd_gene_fam_links: Mapped[str | None] = mapped_column(Text)
    gd_coord: Mapped[str | None] = mapped_column(Text)

    # --- Metadata (md_*) ---
    md_gdb_id: Mapped[str | None] = mapped_column(String(255))
    md_eg_id: Mapped[int | None] = mapped_column(Integer)
    md_mim_id: Mapped[str | None] = mapped_column(String(255))
    md_refseq_id: Mapped[str | None] = mapped_column(String(255))
    md_prot_id: Mapped[str | None] = mapped_column(Text)
    md_ensembl_id: Mapped[str | None] = mapped_column(String(15))
    md_vega_id: Mapped[str | None] = mapped_column(String(18))
    md_rna_central_ids: Mapped[str | None] = mapped_column(Text)
    md_lncipedia: Mapped[str | None] = mapped_column(String(15))
    md_gtrnadb: Mapped[str | None] = mapped_column(String(20))
    md_ucsc_id: Mapped[str | None] = mapped_column(String(50))
    md_rgd_id: Mapped[str | None] = mapped_column(String(50))
    md_mgd_id: Mapped[str | None] = mapped_column(Text)
    md_agr: Mapped[int | None] = mapped_column(Integer)
    md_alphafold: Mapped[str | None] = mapped_column(Text)

    # --- Flags (bool in the dump) ---
    gd_ambiguous: Mapped[bool | None] = mapped_column(Boolean)
    gd_to_review: Mapped[bool | None] = mapped_column(Boolean)
    gd_stable_symbol: Mapped[bool | None] = mapped_column(Boolean)
