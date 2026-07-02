"""``locus_stats`` ORM model — aggregate gene-locus counts by type/group/source.

Maps the existing ``g4public.locus_stats`` schema (PostgreSQL). Column types
and nullability are transcribed verbatim from the authoritative Navicat dump
``.ai/specs/pg-g4public.sql``. The ORM reads and writes **data only** — it
never creates, alters, or drops schema objects.

The dump defines **no primary key** and **no unique column** for this table, so
the model declares an **ORM-only** composite primary key on
(``ls_type``, ``ls_group``, ``ls_source``). These columns are nullable in the
dump, so they are mapped as ``Mapped[... | None]``; forcing the composite key
emits no DDL and never modifies the schema. (A docstring caveat per
Constraints § Primary-key convention.)
"""

from __future__ import annotations

from sqlalchemy import BigInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from pg_g4public_orm.core.base import DeclarativeBase


class LocusStats(DeclarativeBase):
    """Aggregate gene-locus counts grouped by type/group/source.

    ORM-only composite primary key on (``ls_type``, ``ls_group``,
    ``ls_source``): the dump has no usable unique column. ``ls_count`` is
    ``int8`` → ``BigInteger``; ``ls_type`` is unbounded ``varchar``; the
    remaining text columns are ``Text``.
    """

    __tablename__ = "locus_stats"

    # --- ORM-only composite primary key (nullable columns; no DB PK) ---
    ls_type: Mapped[str | None] = mapped_column(String, primary_key=True)
    ls_group: Mapped[str | None] = mapped_column(Text, primary_key=True)
    ls_source: Mapped[str | None] = mapped_column(Text, primary_key=True)

    # --- Aggregate data ---
    ls_count: Mapped[int | None] = mapped_column(BigInteger)
    ls_sort: Mapped[str | None] = mapped_column(Text)
    ls_date: Mapped[str | None] = mapped_column(Text)
