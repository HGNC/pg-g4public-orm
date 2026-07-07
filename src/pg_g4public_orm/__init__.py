"""pg-g4public-orm: SQLAlchemy 2.0 ORM for the PostgreSQL ``g4public`` database.

A synchronous, typed ORM for the HGNC public gene/family data, built on the
shared `db-common <https://github.com/HGNC/db-common>`_ library using the
``postgresql+psycopg`` (psycopg3) driver. The ORM reads and writes **data
only** — it never creates, alters, or drops schema objects.

## Quick start

```python
from pg_g4public_orm import DatabaseSettings, initialize_engine, get_readwrite_session

initialize_engine(DatabaseSettings())  # reads DB_* env vars

with get_readwrite_session() as session:
    ...
```
"""

from __future__ import annotations

import re
from pathlib import Path


def _resolve_version() -> str:
    """Resolve package version from local pyproject, then installed metadata."""
    pyproject = Path(__file__).parent.parent.parent / "pyproject.toml"
    if pyproject.exists():
        version_match = re.search(
            r'^version\s*=\s*["\']([^"\']+)["\']',
            pyproject.read_text(),
            re.MULTILINE,
        )
        return version_match.group(1) if version_match else "0.0.0"

    from importlib.metadata import PackageNotFoundError, version

    try:
        return version("pg-g4public-orm")
    except PackageNotFoundError:  # pragma: no cover - fallback when not installed
        return "0.0.0"


# Read version from pyproject.toml for automatic semantic versioning.
__version__ = _resolve_version()

# Exceptions and capabilities — re-exported from db-common.
from db_common import (  # noqa: E402
    ConfigurationError,
    ConnectionError,
    DatabaseDriver,
    DatabaseError,
    ReadOnlySessionError,
    SessionError,
    health_check,
)

# Core exports (settings + declarative base + session surface).
from pg_g4public_orm.core import (  # noqa: E402
    DatabaseSettings,
    DeclarativeBase,
)
from pg_g4public_orm.core.session import (  # noqa: E402
    close_all_sessions,
    get_engine,
    get_readonly_session,
    get_readwrite_session,
    get_settings,
    initialize_engine,
    refresh_engine,
)

# ORM models — re-exported from submodules.
from pg_g4public_orm.models import (  # noqa: E402
    Cell,
    Comment,
    Ensembl2Hgnc,
    ExternalResource,
    FamilyAlias,
    FamilyHasExternalResource,
    FamilyHasSpecialist,
    FamilyNew,
    Filestore,
    Gencc,
    GeneHasFamily,
    HcopOrthologs,
    Hierarchy,
    HierarchyClosure,
    Import,
    LocusStats,
    LocusStatsChr,
    Mane,
    PubHgnc,
    Specialist,
)

# Repository — re-exported from repositories.
from pg_g4public_orm.repositories import Repository  # noqa: E402

__all__ = [
    "__version__",
    # Core
    "DeclarativeBase",
    "DatabaseSettings",
    # Session module-function surface (over db-common)
    "initialize_engine",
    "get_engine",
    "get_settings",
    "get_readwrite_session",
    "get_readonly_session",
    "close_all_sessions",
    "refresh_engine",
    # Exceptions (re-exported from db-common)
    "DatabaseError",
    "ConfigurationError",
    "ConnectionError",
    "SessionError",
    "ReadOnlySessionError",
    # Capability re-exports (db-common alignment)
    "health_check",
    "DatabaseDriver",
    # Repository
    "Repository",
    # ORM models
    "PubHgnc",
    "FamilyNew",
    "FamilyAlias",
    "Hierarchy",
    "HierarchyClosure",
    "Cell",
    "Filestore",
    "Import",
    "LocusStats",
    "LocusStatsChr",
    "Comment",
    "Gencc",
    "Ensembl2Hgnc",
    "Mane",
    "HcopOrthologs",
    "ExternalResource",
    "Specialist",
    "GeneHasFamily",
    "FamilyHasExternalResource",
    "FamilyHasSpecialist",
]
