"""``ensembl2hgnc`` ORM model — Ensembl ↔ HGNC identifier cross-reference.

Maps the existing ``g4public.ensembl2hgnc`` schema (PostgreSQL). Column types
and nullability are transcribed verbatim from the authoritative Navicat dump
``.ai/specs/pg-g4public.sql``. The ORM reads and writes **data only** — it
never creates, alters, or drops schema objects.

The dump defines **no primary key** and **no unique column** for this table,
so the model declares an **ORM-only** composite primary key on
(``e2h_ensembl_gene_id``, ``e2h_hgnc_id``). All three columns are nullable
``varchar(50)`` in the dump; forcing the composite key emits no DDL and never
modifies the schema. (A docstring caveat per Constraints § Primary-key
convention.)
"""

from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from pg_g4public_orm.core.base import DeclarativeBase


class Ensembl2Hgnc(DeclarativeBase):
    """Ensembl gene identifier to HGNC id / approved symbol cross-reference.

    ORM-only composite primary key on (``e2h_ensembl_gene_id``,
    ``e2h_hgnc_id``): the dump has no usable unique column. Every column is
    ``varchar(50)`` and nullable.
    """

    __tablename__ = "ensembl2hgnc"

    # --- ORM-only composite primary key (nullable columns; no DB PK) ---
    e2h_ensembl_gene_id: Mapped[str | None] = mapped_column(
        String(50), primary_key=True
    )
    e2h_hgnc_id: Mapped[str | None] = mapped_column(String(50), primary_key=True)

    # --- Cross-reference details ---
    e2h_app_sym: Mapped[str | None] = mapped_column(String(50))
