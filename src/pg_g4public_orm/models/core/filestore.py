"""``filestore`` ORM model — file content storage.

Maps the existing ``g4public.filestore`` schema (PostgreSQL). Column types,
nullability, the sequence-backed ``line_id`` and the forced ORM primary key
are transcribed verbatim from the authoritative Navicat dump
``.ai/specs/pg-g4public.sql``. The ORM reads and writes **data only** — it
never creates, alters, or drops schema objects (``primary_key=True`` /
``Sequence(...)`` emit no DDL).
"""

from __future__ import annotations

from sqlalchemy import BigInteger, Integer, Sequence, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from pg_g4public_orm.core.base import DeclarativeBase


class Filestore(DeclarativeBase):
    """File content storage with line-level granularity.

    ``line_id`` is sequence-backed (``filestore_line_id_seq``) and NOT NULL, but the
    dump defines **no database primary key** for this table. Declaring
    ``primary_key=True`` plus ``Sequence(...)`` forces an ORM-level key so
    inserts return the generated id; it emits no DDL and never modifies the
    schema.
    """

    __tablename__ = "filestore"

    # --- Primary key (sequence-backed; no DB PK) ---
    line_id: Mapped[int] = mapped_column(
        BigInteger, Sequence("filestore_line_id_seq"), primary_key=True, nullable=False
    )

    # --- File content ---
    filename: Mapped[str | None] = mapped_column(String(255))
    line: Mapped[str | None] = mapped_column(Text)
