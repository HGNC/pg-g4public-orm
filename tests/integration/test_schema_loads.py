"""Integration tests for loading the Navicat schema dump into ephemeral PostgreSQL."""

import pytest

CURATED_TABLES = {
    "cell",
    "comment",
    "ensembl2hgnc",
    "external_resource",
    "family_alias",
    "family_has_external_resource",
    "family_has_specialist",
    "family_new",
    "filestore",
    "gencc",
    "gene_has_family",
    "hcop_orthologs",
    "hierarchy",
    "hierarchy_closure",
    "import",
    "locus_stats",
    "locus_stats_chr",
    "mane",
    "pub_hgnc",
    "specialist",
}


@pytest.mark.integration
def test_schema_loads_curated_table_set(loaded_schema_connection):
    """The dump should load cleanly and expose exactly the 20 curated tables."""
    with loaded_schema_connection.cursor() as cursor:
        cursor.execute("""
            SELECT tablename
            FROM pg_tables
            WHERE schemaname = 'public'
              AND tablename IN (
                'cell', 'comment', 'ensembl2hgnc', 'external_resource', 'family_alias',
                'family_has_external_resource', 'family_has_specialist', 'family_new',
                'filestore', 'gencc', 'gene_has_family', 'hcop_orthologs', 'hierarchy',
                'hierarchy_closure', 'import', 'locus_stats', 'locus_stats_chr', 'mane',
                'pub_hgnc', 'specialist'
              )
            """)
        tables = {row[0] for row in cursor.fetchall()}

    assert tables == CURATED_TABLES


@pytest.mark.integration
def test_owner_lines_are_stripped_before_execution(owner_stripped_schema_sql):
    """Preprocessed SQL should not contain OWNER TO clauses."""
    assert "OWNER TO" not in owner_stripped_schema_sql
