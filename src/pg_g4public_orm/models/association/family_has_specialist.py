"""``family_has_specialist`` ORM model — family ↔ specialist link.

Maps the existing ``g4public.family_has_specialist`` schema (PostgreSQL). Column
types, nullability and the composite primary key are transcribed verbatim from
the authoritative Navicat dump ``.ai/specs/pg-g4public.sql``. The ORM reads and
writes **data only** — it never creates, alters, or drops schema objects.

In v1 no ``ForeignKey(...)`` / ``relationship()`` is declared: the join columns
(``fam_id``, ``specialist_id``) are read directly. The real database primary key
and foreign keys live on the table; declaring ``primary_key=True`` on the model
emits no DDL and never modifies the schema.
"""

from __future__ import annotations

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from pg_g4public_orm.core.base import DeclarativeBase


class FamilyHasSpecialist(DeclarativeBase):
    """Junction linking a curated family to a specialist page.

    Composite primary key on (``fam_id``, ``specialist_id``); both are NOT NULL
    per the dump.
    """

    __tablename__ = "family_has_specialist"

    fam_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    specialist_id: Mapped[int] = mapped_column(Integer, primary_key=True)
