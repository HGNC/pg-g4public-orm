"""``gene_has_family`` ORM model — junction linking an HGNC gene to a family.

Maps the existing ``g4public.gene_has_family`` schema (PostgreSQL). Column
types, nullability and the composite primary key are transcribed verbatim from
the authoritative Navicat dump ``.ai/specs/pg-g4public.sql``. The ORM reads
and writes **data only** — it never creates, alters, or drops schema objects.

In v1 no ``ForeignKey(...)`` / ``relationship()`` is declared: the join columns
(``hgnc_id``, ``family_id``) are read directly. The real database primary key
and foreign key live on the table; declaring ``primary_key=True`` on the model
emits no DDL and never modifies the schema.
"""

from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from pg_g4public_orm.core.base import DeclarativeBase


class GeneHasFamily(DeclarativeBase):
    """Junction linking an HGNC gene (``hgnc_id``) to a curated family.

    Composite primary key on (``hgnc_id``, ``family_id``); both are NOT NULL
    per the dump. ``url`` and ``custom_sort`` are nullable ``varchar(255)``
    per-resource link metadata.
    """

    __tablename__ = "gene_has_family"

    hgnc_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    family_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    url: Mapped[str | None] = mapped_column(String(255))
    custom_sort: Mapped[str | None] = mapped_column(String(255))
