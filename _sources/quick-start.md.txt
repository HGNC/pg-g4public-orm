# Quick start

## Initialize the engine

```python
from pg_g4public_orm import DatabaseSettings, initialize_engine

initialize_engine(DatabaseSettings())  # reads DB_* env vars
```

`DatabaseSettings()` honours the PostgreSQL defaults
(`driver=postgresql+psycopg`, `port=5432`, `database=g4public`); override any
field via the matching `DB_*` environment variable.

## Read / write with a repository

```python
from pg_g4public_orm import (
    Repository,
    FamilyNew,
    get_readwrite_session,
)

with get_readwrite_session() as session:
    families = Repository(session, FamilyNew)
    family = families.get_by_id(1)               # read by primary key
    rows = families.list_all(limit=25)           # paginated list
    hits = families.filter_by(abbreviation="Kinase")  # equality filter

    new = families.add(FamilyNew(abbreviation="New family"))  # create
    families.save(new)                                        # update
    families.delete(new)                                      # delete
```

`Repository(session, FamilyNew)` works against any of the 20 model classes.
The example uses `FamilyNew.abbreviation` (the family short name; indexed in
the schema as `ind_name`).

## Read-only sessions

```python
from pg_g4public_orm import get_readonly_session

with get_readonly_session() as session:
    ...  # commit()/flush-to-DB raise ReadOnlySessionError here
```

A read-only session proxies the underlying SQLAlchemy `Session` but raises
`ReadOnlySessionError` on any operation that would persist changes, guarding
ad-hoc read workloads.

## Top-level imports

All 20 ORM models, the generic `Repository`, the session module-function
surface, and the re-exported `db-common` exceptions / capabilities are
importable directly from the top-level `pg_g4public_orm` package:

```python
import pg_g4public_orm

print(pg_g4public_orm.__version__)
```

See {doc}`api/index` for the complete autodoc'd reference.
