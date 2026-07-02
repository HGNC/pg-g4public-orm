"""``locus_stats_chr`` ORM model — per-chromosome gene-locus counts.

Maps the existing ``g4public.locus_stats_chr`` schema (PostgreSQL). Column
types and nullability are transcribed verbatim from the authoritative Navicat
dump ``.ai/specs/pg-g4public.sql``. The ORM reads and writes **data only** —
it never creates, alters, or drops schema objects.

The dump defines **no primary key** and **no unique column** for this table,
so the model declares an **ORM-only** composite primary key on (``ls_chr``,
``ls_type``, ``ls_group``, ``ls_source``). These columns are nullable in the
dump, so they are mapped as ``Mapped[... | None]``; forcing the composite key
emits no DDL and never modifies the schema. (A docstring caveat per
Constraints § Primary-key convention.)
"""

from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from pg_g4public_orm.core.base import DeclarativeBase


class LocusStatsChr(DeclarativeBase):
    """Per-chromosome gene-locus counts grouped by type/group/source.

    ORM-only composite primary key on (``ls_chr``, ``ls_type``, ``ls_group``,
    ``ls_source``): the dump has no usable unique column. Note ``ls_count`` is
    ``int4`` here (unlike the ``int8`` in ``locus_stats``) and ``ls_sort`` is
    ``int4`` (unlike the ``text`` in ``locus_stats``) — transcribed faithfully.
    """

    __tablename__ = "locus_stats_chr"

    # --- ORM-only composite primary key (nullable columns; no DB PK) ---
    ls_chr: Mapped[str | None] = mapped_column(String(5), primary_key=True)
    ls_type: Mapped[str | None] = mapped_column(String(50), primary_key=True)
    ls_group: Mapped[str | None] = mapped_column(String(50), primary_key=True)
    ls_source: Mapped[str | None] = mapped_column(String(25), primary_key=True)

    # --- Per-chromosome data ---
    ls_count: Mapped[int | None] = mapped_column(Integer)
    ls_sort: Mapped[int | None] = mapped_column(Integer)
    ls_date: Mapped[str | None] = mapped_column(String(255))
