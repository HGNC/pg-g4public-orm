"""``family_has_external_resource`` ORM model — family ↔ external resource link.

Maps the existing ``g4public.family_has_external_resource`` schema (PostgreSQL).
Column types, nullability and the composite primary key are transcribed verbatim
from the authoritative Navicat dump ``.ai/specs/pg-g4public.sql``. The ORM reads
and writes **data only** — it never creates, alters, or drops schema objects.

In v1 no ``ForeignKey(...)`` / ``relationship()`` is declared: the join columns
(``family_id``, ``ext_id``) are read directly. The real database primary key and
foreign keys live on the table; declaring ``primary_key=True`` on the model
emits no DDL and never modifies the schema.
"""

from __future__ import annotations

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from pg_g4public_orm.core.base import DeclarativeBase


class FamilyHasExternalResource(DeclarativeBase):
    """Junction linking a curated family to an external resource.

    Composite primary key on (``family_id``, ``ext_id``); both are NOT NULL per
    the dump.
    """

    __tablename__ = "family_has_external_resource"

    family_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ext_id: Mapped[int] = mapped_column(Integer, primary_key=True)
