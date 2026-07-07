# pg-g4public-orm

SQLAlchemy 2.0 ORM for the PostgreSQL `g4public` database (HGNC public
gene/family data). Synchronous only, built on the shared
[`db-common`](https://github.com/HGNC/db-common) library using the
`postgresql+psycopg` (psycopg3) driver.

> The ORM reads and writes **data only** — it never creates, alters, or drops
> schema objects.

```{toctree}
:maxdepth: 2
:caption: Contents

installation
quick-start
api/index
```

## Overview

`pg-g4public-orm` provides a typed, synchronous SQLAlchemy 2.0 ORM that maps
the **existing** PostgreSQL `g4public` schema and gives full row-level CRUD
(create / read / update / delete data). It is the PostgreSQL sibling of
`my-g4public-orm` (which targets MySQL), and mirrors the established
`vgnc_orm`-on-`db-common` integration shape.

## Features

- **20 curated ORM models** mapping the `g4public` PostgreSQL schema (genes,
  families, hierarchy, HCOP orthologs, GenCC, MANE, etc.).
- **Generic `Repository[T]`** providing create / read / update / delete over a
  SQLAlchemy `Session`.
- **Session module-function surface** (`initialize_engine`,
  `get_readwrite_session`, `get_readonly_session`, `close_all_sessions`, ...)
  delegating to `db-common`.
- **PostgreSQL-native type mapping** — `bool`, `int4` / `int8` (`BigInteger`),
  `varchar(N)`, `text`, `date`, `timestamp` — driven by the authoritative
  Navicat schema dump.

## Safety

The ORM never calls `metadata.create_all()`, Alembic, or any DDL against the
real database, and it does not declare `ForeignKey(...)` or `relationship()`
in v1 (columns are read directly, consistent with `my-g4public-orm`). A
marked-`integration` schema-drift guard reflects an ephemeral PostgreSQL
container and asserts the declared model metadata matches the live schema
(columns / types / nullability / primary keys / indexes / foreign keys).

Head to {doc}`installation` to get started, then {doc}`quick-start`, or browse
the {doc}`api/index` for the full autodoc'd API reference.
