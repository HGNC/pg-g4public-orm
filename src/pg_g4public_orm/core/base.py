"""Shared SQLAlchemy declarative base (db-common subclass)."""

import db_common


class DeclarativeBase(db_common.DeclarativeBase):
    """Base class for all pg-g4public-orm ORM models.

    Each model defines its own primary key based on the existing ``g4public``
    schema (the ORM never creates, alters, or drops schema objects).
    """

    __abstract__ = True
