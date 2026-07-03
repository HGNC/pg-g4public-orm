"""``comment`` ORM model — free-text curator comments keyed by HGNC id.

Maps the existing ``g4public.comment`` schema (PostgreSQL). Column types and
nullability are transcribed verbatim from the authoritative Navicat dump
``.ai/specs/pg-g4public.sql``. The ORM reads and writes **data only** — it
never creates, alters, or drops schema objects.

The dump defines **no primary key** and **no unique column** for this table,
so the model declares an **ORM-only** composite primary key on
(``hgnc_id``, ``note``). ``hgnc_id`` is NOT NULL in the dump while ``note`` is
nullable; forcing the composite key emits no DDL and never modifies the
schema. (A docstring caveat per Constraints § Primary-key convention.)
"""

from __future__ import annotations

from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from pg_g4public_orm.core.base import DeclarativeBase


class Comment(DeclarativeBase):
    """Curator comment attached to a gene (one row per gene/note pair).

    ORM-only composite primary key on (``hgnc_id``, ``note``): the dump has no
    usable unique column. ``hgnc_id`` is NOT NULL; ``note`` is nullable
    ``text``.
    """

    __tablename__ = "comment"

    # --- ORM-only composite primary key (no DB PK) ---
    hgnc_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    note: Mapped[str | None] = mapped_column(Text, primary_key=True)
