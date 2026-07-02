"""``family_alias`` ORM model — alternate names for HGNC gene families.

Maps the existing ``g4public.family_alias`` schema (PostgreSQL). Column types,
nullability and the sequence-backed primary key are transcribed verbatim from
the authoritative Navicat dump ``.ai/specs/pg-g4public.sql``. The ORM reads and
writes **data only** — it never creates, alters, or drops schema objects.
"""

from __future__ import annotations

from sqlalchemy import Integer, Sequence, String
from sqlalchemy.orm import Mapped, mapped_column

from pg_g4public_orm.core.base import DeclarativeBase


class FamilyAlias(DeclarativeBase):
    """Alternate name (alias) for an HGNC gene family.

    ``id`` is sequence-backed (``family_alias_id_seq``) and the real database
    primary key. ``family_id`` references ``family_new(id)`` — the foreign key
    is **not** modelled in v1 (read the column directly). Declaring
    ``primary_key=True`` plus ``Sequence(...)`` emits no DDL and never modifies
    the schema.
    """

    __tablename__ = "family_alias"

    # --- Primary key (sequence-backed, real DB PK) ---
    id: Mapped[int] = mapped_column(
        Integer, Sequence("family_alias_id_seq"), primary_key=True
    )

    # --- Columns (both NOT NULL in the dump) ---
    family_id: Mapped[int] = mapped_column(Integer)
    alias: Mapped[str] = mapped_column(String(255))
