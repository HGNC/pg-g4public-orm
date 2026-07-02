"""``hierarchy_closure`` ORM model — transitive closure of the family hierarchy.

Maps the existing ``g4public.hierarchy_closure`` schema (PostgreSQL). Column
types, nullability, the ``distance`` default and the three-column composite
primary key are transcribed verbatim from the authoritative Navicat dump
``.ai/specs/pg-g4public.sql``. The ORM reads and writes **data only** — it
never creates, alters, or drops schema objects.
"""

from __future__ import annotations

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from pg_g4public_orm.core.base import DeclarativeBase


class HierarchyClosure(DeclarativeBase):
    """Transitive closure of the HGNC gene-family hierarchy.

    Three-column composite primary key on (``parent_fam_id``, ``child_fam_id``,
    ``distance``). ``distance`` is the hop count between the parent and child
    and defaults to ``0`` (matching the dump's ``DEFAULT 0``). Forcing the ORM
    composite PK emits no DDL and never modifies the schema.
    """

    __tablename__ = "hierarchy_closure"

    parent_fam_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    child_fam_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    distance: Mapped[int] = mapped_column(Integer, default=0, primary_key=True)
