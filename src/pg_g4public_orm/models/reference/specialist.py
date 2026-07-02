"""``specialist`` ORM model — curated specialist database link.

Maps the existing ``g4public.specialist`` schema (PostgreSQL). Column types,
nullability and the real database primary key are transcribed verbatim from
the authoritative Navicat dump ``.ai/specs/pg-g4public.sql``. The ORM reads
and writes **data only** — it never creates, alters, or drops schema objects
(``primary_key=True`` emits no DDL).
"""

from __future__ import annotations

from sqlalchemy import Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from pg_g4public_orm.core.base import DeclarativeBase


class Specialist(DeclarativeBase):
    """Curated specialist database linked from HGNC gene-family pages.

    ``id`` is a real database primary key (``specialist_pkey``). Declaring
    ``primary_key=True`` emits no DDL and never modifies the schema.
    """

    __tablename__ = "specialist"
    __table_args__ = (Index("specialist_id_key", "id", unique=True),)

    # --- Primary key (real DB PK; not sequence-backed) ---
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # --- Specialist metadata ---
    name: Mapped[str] = mapped_column(String(255))
    address: Mapped[str] = mapped_column(Text)
    url: Mapped[str | None] = mapped_column(String(255))
