"""``external_resource`` ORM model — curated external data resource link.

Maps the existing ``g4public.external_resource`` schema (PostgreSQL). Column
types, nullability, the ``approved`` boolean default and the real database
primary key are transcribed verbatim from the authoritative Navicat dump
``.ai/specs/pg-g4public.sql``. The ORM reads and writes **data only** — it
never creates, alters, or drops schema objects (``primary_key=True`` emits no
DDL).
"""

from __future__ import annotations

from sqlalchemy import Boolean, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from pg_g4public_orm.core.base import DeclarativeBase


class ExternalResource(DeclarativeBase):
    """Curated external data resource linked from HGNC gene-family pages.

    ``id`` is a real database primary key (``external_resource_pkey``).
    Declaring ``primary_key=True`` emits no DDL and never modifies the schema.
    ``approved`` is ``bool NOT NULL DEFAULT false`` per the dump.
    """

    __tablename__ = "external_resource"
    __table_args__ = (Index("external_resource_id_key", "id", unique=True),)

    # --- Primary key (real DB PK; not sequence-backed) ---
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # --- Resource metadata ---
    name: Mapped[str] = mapped_column(String(255))
    url: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(String(255))
    approved: Mapped[bool] = mapped_column(Boolean, default=False)
