"""``cell`` ORM model — editable HGNC data "cell" configuration.

Maps the existing ``g4public.cell`` schema (PostgreSQL). Column types,
nullability, the sequence-backed ``cell_id`` and the forced ORM primary key
are transcribed verbatim from the authoritative Navicat dump
``.ai/specs/pg-g4public.sql``. The ORM reads and writes **data only** — it
never creates, alters, or drops schema objects (``primary_key=True`` /
``Sequence(...)`` emit no DDL).
"""

from __future__ import annotations

from sqlalchemy import Integer, Sequence, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from pg_g4public_orm.core.base import DeclarativeBase


class Cell(DeclarativeBase):
    """Editable data "cell" (column metadata for the HGNC editing interface).

    ``cell_id`` is sequence-backed (``cell_cell_id_seq``) and NOT NULL, but the
    dump defines **no database primary key** for this table. Declaring
    ``primary_key=True`` plus ``Sequence(...)`` forces an ORM-level key so
    inserts return the generated id; it emits no DDL and never modifies the
    schema.
    """

    __tablename__ = "cell"

    # --- Primary key (sequence-backed; no DB PK) ---
    cell_id: Mapped[int] = mapped_column(
        Integer, Sequence("cell_cell_id_seq"), primary_key=True
    )

    # --- Cell metadata ---
    cell_name: Mapped[str | None] = mapped_column(String(255))
    cell_alias: Mapped[str | None] = mapped_column(String(255))
    cell_table: Mapped[str | None] = mapped_column(String(255))
    cell_permit: Mapped[str | None] = mapped_column(Text)
    cell_view: Mapped[str | None] = mapped_column(Text)
    cell_edit: Mapped[str | None] = mapped_column(Text)
    cell_lint: Mapped[str | None] = mapped_column(Text)
    cell_notes: Mapped[str | None] = mapped_column(Text)
    cell_sort: Mapped[int | None] = mapped_column(Integer)
