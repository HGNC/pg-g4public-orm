"""``gencc`` ORM model — Gene Curation Coalition disease-gene assertions.

Maps the existing ``g4public.gencc`` schema (PostgreSQL). Column types and
nullability are transcribed verbatim from the authoritative Navicat dump
``.ai/specs/pg-g4public.sql``. The ORM reads and writes **data only** — it
never creates, alters, or drops schema objects.

The dump defines **no primary key** and **no unique column** for this table,
so the model declares an **ORM-only** composite primary key on (``uuid``,
``hgnc_id``, ``disease_id``). Note ``uuid`` is **nullable** ``varchar`` in the
dump (not a real, reliable key); forcing the composite key emits no DDL and
never modifies the schema. (A docstring caveat per Constraints § Primary-key
convention.)
"""

from __future__ import annotations

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from pg_g4public_orm.core.base import DeclarativeBase


class Gencc(DeclarativeBase):
    """GenCC disease-gene curation record (gene ↔ disease assertion).

    ORM-only composite primary key on (``uuid``, ``hgnc_id``, ``disease_id``):
    the dump has no usable unique column. Be aware ``uuid`` is nullable
    ``varchar``; ``disease_title`` is ``text``; ``omim_id`` is ``int4``.
    """

    __tablename__ = "gencc"

    # --- ORM-only composite primary key (nullable columns; no DB PK) ---
    uuid: Mapped[str | None] = mapped_column(String, primary_key=True)
    hgnc_id: Mapped[int | None] = mapped_column(Integer, primary_key=True)
    disease_id: Mapped[str | None] = mapped_column(String, primary_key=True)

    # --- Disease assertion details ---
    disease_title: Mapped[str | None] = mapped_column(Text)
    omim_id: Mapped[int | None] = mapped_column(Integer)
