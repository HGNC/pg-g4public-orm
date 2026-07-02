"""``hierarchy`` ORM model — parent/child edges of the gene-family hierarchy.

Maps the existing ``g4public.hierarchy`` schema (PostgreSQL). Column types,
nullability and the composite primary key are transcribed verbatim from the
authoritative Navicat dump ``.ai/specs/pg-g4public.sql``. The ORM reads and
writes **data only** — it never creates, alters, or drops schema objects.
"""

from __future__ import annotations

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from pg_g4public_orm.core.base import DeclarativeBase


class Hierarchy(DeclarativeBase):
    """Parent/child edge in the HGNC gene-family hierarchy.

    Composite primary key on (``parent_fam_id``, ``child_fam_id``); both
    reference ``family_new(id)`` (the foreign keys are **not** modelled in v1).
    The database constraint is misspelled ``heirarchy_pkey`` — that is
    irrelevant to the model. Forcing the ORM composite PK emits no DDL and never
    modifies the schema.
    """

    __tablename__ = "hierarchy"

    parent_fam_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    child_fam_id: Mapped[int] = mapped_column(Integer, primary_key=True)
