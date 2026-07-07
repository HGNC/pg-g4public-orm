# pg-g4public-orm

SQLAlchemy 2.0 ORM for the PostgreSQL `g4public` database (HGNC public
gene/family data). Synchronous only, built on the shared
[`db-common`](https://github.com/HGNC/db-common) library using the
`postgresql+psycopg` (psycopg3) driver.

> The ORM reads and writes **data only** — it never creates, alters, or drops
> schema objects.

## Quick start

```python
from pg_g4public_orm import (
    DatabaseSettings,
    Repository,
    FamilyNew,
    initialize_engine,
    get_readwrite_session,
)

initialize_engine(DatabaseSettings())  # reads DB_* env vars

with get_readwrite_session() as session:
    families = Repository(session, FamilyNew)
    family = families.get_by_id(1)        # read
    new = families.add(FamilyNew(...))    # create
    families.save(new)                    # update
    families.delete(new)                  # delete
```

All 20 ORM models, the generic `Repository`, the session module-function
surface, and the re-exported `db-common` exceptions/capabilities are importable
directly from the top-level `pg_g4public_orm` package.

## Configuration

Settings are read from `DB_`-prefixed environment variables (or a `.env` file).
PostgreSQL defaults: `driver=postgresql+psycopg`, `port=5432`,
`database=g4public`. See [`.env.example`](.env.example).
