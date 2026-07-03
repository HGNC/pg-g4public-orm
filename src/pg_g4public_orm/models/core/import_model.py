"""``import`` ORM model — import job metadata.

Maps the existing ``g4public.import`` schema (PostgreSQL). Column types,
nullability, the sequence-backed ``imp_id`` and the forced ORM primary key
are transcribed verbatim from the authoritative Navicat dump
``.ai/specs/pg-g4public.sql``. The ORM reads and writes **data only** — it
never creates, alters, or drops schema objects (``primary_key=True`` /
``Sequence(...)`` emit no DDL).
"""

from __future__ import annotations

from sqlalchemy import Boolean, Integer, Sequence, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from pg_g4public_orm.core.base import DeclarativeBase


class Import(DeclarativeBase):
    """Import job metadata for tracking data imports.

    ``imp_id`` is sequence-backed (``import_imp_id_seq``) and NOT NULL, but the
    dump defines **no database primary key** for this table. Declaring
    ``primary_key=True`` plus ``Sequence(...)`` forces an ORM-level key so
    inserts return the generated id; it emits no DDL and never modifies the
    schema.
    """

    __tablename__ = "import"

    # --- Primary key (sequence-backed; no DB PK) ---
    imp_id: Mapped[int] = mapped_column(
        Integer, Sequence("import_imp_id_seq"), primary_key=True, nullable=False
    )

    # --- Import metadata ---
    imp_source: Mapped[str | None] = mapped_column(Text)
    imp_tbl: Mapped[str | None] = mapped_column(String(255))
    imp_name: Mapped[str | None] = mapped_column(String(255))
    imp_data_type: Mapped[str | None] = mapped_column(Text)
    imp_index: Mapped[bool | None] = mapped_column(Boolean)
    imp_permit: Mapped[str | None] = mapped_column(Text)
    imp_notes: Mapped[str | None] = mapped_column(Text)
    imp_sort: Mapped[int | None] = mapped_column(Integer)
