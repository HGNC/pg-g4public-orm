"""``family_new`` ORM model — the central HGNC curated gene family table.

Maps the existing ``g4public.family_new`` schema (PostgreSQL). Column types,
nullability, index names and the sequence-backed primary key are transcribed
verbatim from the authoritative Navicat dump ``.ai/specs/pg-g4public.sql``.
The ORM reads and writes **data only** — it never creates, alters, or drops
schema objects (``primary_key=True`` / ``Sequence(...)`` emit no DDL).
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    DateTime,
    Index,
    Integer,
    Sequence,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from pg_g4public_orm.core.base import DeclarativeBase


class FamilyNew(DeclarativeBase):
    """HGNC curated gene family (one row per family).

    ``id`` is sequence-backed (``family_new_fam_id_seq``) and the real database
    primary key. Declaring ``primary_key=True`` plus ``Sequence(...)`` lets
    inserts return the generated id; it emits no DDL and never modifies the
    schema.
    """

    __tablename__ = "family_new"
    __table_args__ = (
        Index("family_new_id_key", "id", unique=True),
        Index("ind_name", "abbreviation"),
    )

    # --- Primary key (sequence-backed, real DB PK) ---
    id: Mapped[int] = mapped_column(
        Integer, Sequence("family_new_fam_id_seq"), primary_key=True
    )

    # --- Family metadata ---
    abbreviation: Mapped[str | None] = mapped_column(String(50))
    name: Mapped[str | None] = mapped_column(String(150))
    editor: Mapped[str | None] = mapped_column(String(50))
    curator_comment: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str | None] = mapped_column(String(255))
    external_note: Mapped[str | None] = mapped_column(Text)
    pubmed_ids: Mapped[str | None] = mapped_column(Text)
    type: Mapped[str | None] = mapped_column(String(50))
    desc_comment: Mapped[str | None] = mapped_column(Text)
    desc_label: Mapped[str | None] = mapped_column(String(255))
    desc_source: Mapped[str | None] = mapped_column(String(255))
    desc_go: Mapped[str | None] = mapped_column(String(255))
    typical_gene: Mapped[str | None] = mapped_column(String(255))

    # --- Timestamps (timestamp(6) DEFAULT now() in the dump) ---
    date_created: Mapped[datetime | None] = mapped_column(DateTime, default=func.now())
    date_modified: Mapped[datetime | None] = mapped_column(DateTime, default=func.now())
