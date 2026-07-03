/*
 Navicat PostgreSQL Dump SQL

 Source Server         : GCP - HGNC
 Source Server Type    : PostgreSQL
 Source Server Version : 180001 (180001)
 Source Host           : 34.147.243.58:5432
 Source Catalog        : g4public
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 180001 (180001)
 File Encoding         : 65001

 Date: 30/06/2026 15:57:25
*/


-- ----------------------------
-- Type structure for fam_status
-- ----------------------------
DROP TYPE IF EXISTS "public"."fam_status";
CREATE TYPE "public"."fam_status" AS ENUM (
  'exported',
  'internal'
);
ALTER TYPE "public"."fam_status" OWNER TO "genew";

-- ----------------------------
-- Type structure for fam_type
-- ----------------------------
DROP TYPE IF EXISTS "public"."fam_type";
CREATE TYPE "public"."fam_type" AS ENUM (
  'homology',
  'function',
  'other'
);
ALTER TYPE "public"."fam_type" OWNER TO "genew";

-- ----------------------------
-- Sequence structure for cell_cell_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."cell_cell_id_seq";
CREATE SEQUENCE "public"."cell_cell_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;
ALTER SEQUENCE "public"."cell_cell_id_seq" OWNER TO "genew";

-- ----------------------------
-- Sequence structure for family_alias_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."family_alias_id_seq";
CREATE SEQUENCE "public"."family_alias_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;
ALTER SEQUENCE "public"."family_alias_id_seq" OWNER TO "genew";

-- ----------------------------
-- Sequence structure for family_new_fam_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."family_new_fam_id_seq";
CREATE SEQUENCE "public"."family_new_fam_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;
ALTER SEQUENCE "public"."family_new_fam_id_seq" OWNER TO "genew";

-- ----------------------------
-- Sequence structure for filestore_line_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."filestore_line_id_seq";
CREATE SEQUENCE "public"."filestore_line_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;
ALTER SEQUENCE "public"."filestore_line_id_seq" OWNER TO "genew";

-- ----------------------------
-- Sequence structure for import_imp_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."import_imp_id_seq";
CREATE SEQUENCE "public"."import_imp_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;
ALTER SEQUENCE "public"."import_imp_id_seq" OWNER TO "genew";

-- ----------------------------
-- Sequence structure for key_tbl_fld_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."key_tbl_fld_id_seq";
CREATE SEQUENCE "public"."key_tbl_fld_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;
ALTER SEQUENCE "public"."key_tbl_fld_id_seq" OWNER TO "genew";

-- ----------------------------
-- Table structure for cell
-- ----------------------------
DROP TABLE IF EXISTS "public"."cell";
CREATE TABLE "public"."cell" (
  "cell_id" int4 NOT NULL DEFAULT nextval('cell_cell_id_seq'::regclass),
  "cell_name" varchar(255) COLLATE "pg_catalog"."default",
  "cell_alias" varchar(255) COLLATE "pg_catalog"."default",
  "cell_table" varchar(255) COLLATE "pg_catalog"."default",
  "cell_permit" text COLLATE "pg_catalog"."default",
  "cell_view" text COLLATE "pg_catalog"."default",
  "cell_edit" text COLLATE "pg_catalog"."default",
  "cell_lint" text COLLATE "pg_catalog"."default",
  "cell_notes" text COLLATE "pg_catalog"."default",
  "cell_sort" int4
)
;
ALTER TABLE "public"."cell" OWNER TO "genew";

-- ----------------------------
-- Table structure for comment
-- ----------------------------
DROP TABLE IF EXISTS "public"."comment";
CREATE TABLE "public"."comment" (
  "hgnc_id" int4 NOT NULL,
  "note" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."comment" OWNER TO "genew";

-- ----------------------------
-- Table structure for date_test
-- ----------------------------
DROP TABLE IF EXISTS "public"."date_test";
CREATE TABLE "public"."date_test" (
  "foo" varchar(100) COLLATE "pg_catalog"."default",
  "bar" date
)
;
ALTER TABLE "public"."date_test" OWNER TO "genew";

-- ----------------------------
-- Table structure for delme2
-- ----------------------------
DROP TABLE IF EXISTS "public"."delme2";
CREATE TABLE "public"."delme2" (
  "gd_hgnc_id" int4,
  "gd_app_sym" varchar(255) COLLATE "pg_catalog"."default",
  "gd_app_sym_sort" text COLLATE "pg_catalog"."default",
  "gd_app_name" text COLLATE "pg_catalog"."default",
  "gd_status" varchar(300) COLLATE "pg_catalog"."default",
  "gd_locus_type" text COLLATE "pg_catalog"."default",
  "gd_prev_sym" text COLLATE "pg_catalog"."default",
  "gd_prev_name" text COLLATE "pg_catalog"."default",
  "gd_aliases" text COLLATE "pg_catalog"."default",
  "gd_name_aliases" text COLLATE "pg_catalog"."default",
  "gd_pub_chrom_map" varchar(255) COLLATE "pg_catalog"."default",
  "gd_pub_chrom_map_sort" varchar(255) COLLATE "pg_catalog"."default",
  "gd_date2app_or_res" date,
  "gd_date_mod" date,
  "gd_date_name_change" date,
  "gd_pub_acc_ids" text COLLATE "pg_catalog"."default",
  "gd_enz_ids" text COLLATE "pg_catalog"."default",
  "gd_pub_eg_id" int4,
  "gd_mgd_id" varchar(255) COLLATE "pg_catalog"."default",
  "gd_other_ids" text COLLATE "pg_catalog"."default",
  "gd_other_ids_list" text COLLATE "pg_catalog"."default",
  "gd_pubmed_ids" text COLLATE "pg_catalog"."default",
  "gd_pub_refseq_ids" text COLLATE "pg_catalog"."default",
  "gd_gene_fam_name" text COLLATE "pg_catalog"."default",
  "gd_date_sym_change" date,
  "md_gdb_id" varchar(255) COLLATE "pg_catalog"."default",
  "md_eg_id" int4,
  "md_mim_id" varchar(255) COLLATE "pg_catalog"."default",
  "md_refseq_id" varchar(255) COLLATE "pg_catalog"."default",
  "md_prot_id" varchar(255) COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."delme2" OWNER TO "genew";

-- ----------------------------
-- Table structure for delme_update
-- ----------------------------
DROP TABLE IF EXISTS "public"."delme_update";
CREATE TABLE "public"."delme_update" (
  "ls_chr" varchar(5) COLLATE "pg_catalog"."default",
  "ls_count" int4,
  "ls_type" varchar(50) COLLATE "pg_catalog"."default",
  "ls_group" varchar(50) COLLATE "pg_catalog"."default",
  "ls_source" varchar(25) COLLATE "pg_catalog"."default",
  "ls_sort" int4,
  "ls_date" varchar(255) COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."delme_update" OWNER TO "genew";

-- ----------------------------
-- Table structure for ensembl2hgnc
-- ----------------------------
DROP TABLE IF EXISTS "public"."ensembl2hgnc";
CREATE TABLE "public"."ensembl2hgnc" (
  "e2h_hgnc_id" varchar(50) COLLATE "pg_catalog"."default",
  "e2h_app_sym" varchar(50) COLLATE "pg_catalog"."default",
  "e2h_ensembl_gene_id" varchar(50) COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."ensembl2hgnc" OWNER TO "genew";
COMMENT ON TABLE "public"."ensembl2hgnc" IS 'ensembl2hgnc created by /home/genew/Genew4_maintain/make_genew4_download.pl. Sat Jun 23 05:44:38 2007';

-- ----------------------------
-- Table structure for external_resource
-- ----------------------------
DROP TABLE IF EXISTS "public"."external_resource";
CREATE TABLE "public"."external_resource" (
  "id" int4 NOT NULL,
  "name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "url" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "description" varchar(255) COLLATE "pg_catalog"."default",
  "approved" bool NOT NULL DEFAULT false
)
;
ALTER TABLE "public"."external_resource" OWNER TO "genew";

-- ----------------------------
-- Table structure for family_alias
-- ----------------------------
DROP TABLE IF EXISTS "public"."family_alias";
CREATE TABLE "public"."family_alias" (
  "id" int4 NOT NULL DEFAULT nextval('family_alias_id_seq'::regclass),
  "family_id" int4 NOT NULL,
  "alias" varchar(255) COLLATE "pg_catalog"."default" NOT NULL
)
;
ALTER TABLE "public"."family_alias" OWNER TO "genew";

-- ----------------------------
-- Table structure for family_has_external_resource
-- ----------------------------
DROP TABLE IF EXISTS "public"."family_has_external_resource";
CREATE TABLE "public"."family_has_external_resource" (
  "family_id" int4 NOT NULL,
  "ext_id" int4 NOT NULL
)
;
ALTER TABLE "public"."family_has_external_resource" OWNER TO "genew";

-- ----------------------------
-- Table structure for family_has_specialist
-- ----------------------------
DROP TABLE IF EXISTS "public"."family_has_specialist";
CREATE TABLE "public"."family_has_specialist" (
  "fam_id" int4 NOT NULL,
  "specialist_id" int4 NOT NULL
)
;
ALTER TABLE "public"."family_has_specialist" OWNER TO "genew";

-- ----------------------------
-- Table structure for family_new
-- ----------------------------
DROP TABLE IF EXISTS "public"."family_new";
CREATE TABLE "public"."family_new" (
  "id" int4 NOT NULL DEFAULT nextval('family_new_fam_id_seq'::regclass),
  "abbreviation" varchar(50) COLLATE "pg_catalog"."default",
  "name" varchar(150) COLLATE "pg_catalog"."default",
  "editor" varchar(50) COLLATE "pg_catalog"."default",
  "curator_comment" text COLLATE "pg_catalog"."default",
  "status" varchar(255) COLLATE "pg_catalog"."default",
  "external_note" text COLLATE "pg_catalog"."default",
  "pubmed_ids" text COLLATE "pg_catalog"."default",
  "type" varchar(50) COLLATE "pg_catalog"."default",
  "desc_comment" text COLLATE "pg_catalog"."default",
  "desc_label" varchar(255) COLLATE "pg_catalog"."default",
  "desc_source" varchar(255) COLLATE "pg_catalog"."default",
  "desc_go" varchar(255) COLLATE "pg_catalog"."default",
  "typical_gene" varchar(255) COLLATE "pg_catalog"."default",
  "date_created" timestamp(6) DEFAULT now(),
  "date_modified" timestamp(6) DEFAULT now()
)
;
ALTER TABLE "public"."family_new" OWNER TO "genew";

-- ----------------------------
-- Table structure for filestore
-- ----------------------------
DROP TABLE IF EXISTS "public"."filestore";
CREATE TABLE "public"."filestore" (
  "line_id" int8 NOT NULL DEFAULT nextval('filestore_line_id_seq'::regclass),
  "filename" varchar(255) COLLATE "pg_catalog"."default",
  "line" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."filestore" OWNER TO "genew";

-- ----------------------------
-- Table structure for gencc
-- ----------------------------
DROP TABLE IF EXISTS "public"."gencc";
CREATE TABLE "public"."gencc" (
  "uuid" varchar COLLATE "pg_catalog"."default",
  "hgnc_id" int4,
  "disease_id" varchar COLLATE "pg_catalog"."default",
  "disease_title" text COLLATE "pg_catalog"."default",
  "omim_id" int4
)
;
ALTER TABLE "public"."gencc" OWNER TO "genew";

-- ----------------------------
-- Table structure for gene_has_family
-- ----------------------------
DROP TABLE IF EXISTS "public"."gene_has_family";
CREATE TABLE "public"."gene_has_family" (
  "hgnc_id" int4 NOT NULL,
  "family_id" int4 NOT NULL,
  "url" varchar(255) COLLATE "pg_catalog"."default",
  "custom_sort" varchar(255) COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."gene_has_family" OWNER TO "genew";

-- ----------------------------
-- Table structure for hcop_orthologs
-- ----------------------------
DROP TABLE IF EXISTS "public"."hcop_orthologs";
CREATE TABLE "public"."hcop_orthologs" (
  "orth_id" int8 NOT NULL,
  "taxon_a" int8 NOT NULL,
  "taxon_b" int8 NOT NULL,
  "db_id_a" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "db_id_b" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "vgnc_a" varchar(15) COLLATE "pg_catalog"."default",
  "vgnc_b" varchar(255) COLLATE "pg_catalog"."default",
  "ensembl_a" varchar(28) COLLATE "pg_catalog"."default" NOT NULL,
  "ensembl_b" varchar(28) COLLATE "pg_catalog"."default" NOT NULL,
  "entrez_a" varchar(28) COLLATE "pg_catalog"."default",
  "entrez_b" varchar(28) COLLATE "pg_catalog"."default",
  "symbol_a" varchar(255) COLLATE "pg_catalog"."default",
  "symbol_b" varchar(255) COLLATE "pg_catalog"."default",
  "symbol_source_a" varchar(128) COLLATE "pg_catalog"."default",
  "symbol_source_b" varchar(128) COLLATE "pg_catalog"."default",
  "name_a" text COLLATE "pg_catalog"."default",
  "name_b" text COLLATE "pg_catalog"."default",
  "source_name_a" varchar(128) COLLATE "pg_catalog"."default",
  "source_name_b" varchar(128) COLLATE "pg_catalog"."default",
  "locus_type_a" varchar(255) COLLATE "pg_catalog"."default",
  "locus_type_b" varchar(255) COLLATE "pg_catalog"."default",
  "locus_source_a" varchar(128) COLLATE "pg_catalog"."default",
  "locus_source_b" varchar(128) COLLATE "pg_catalog"."default",
  "class_a" varchar(8) COLLATE "pg_catalog"."default",
  "class_b" varchar(8) COLLATE "pg_catalog"."default",
  "chr_a" varchar(128) COLLATE "pg_catalog"."default",
  "chr_b" varchar(128) COLLATE "pg_catalog"."default",
  "support" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "text_link_a" text COLLATE "pg_catalog"."default" NOT NULL,
  "text_link_b" text COLLATE "pg_catalog"."default" NOT NULL,
  "sort_order" int8 NOT NULL
)
;
ALTER TABLE "public"."hcop_orthologs" OWNER TO "genew";

-- ----------------------------
-- Table structure for hgnc_adv
-- ----------------------------
DROP TABLE IF EXISTS "public"."hgnc_adv";
CREATE TABLE "public"."hgnc_adv" (
  "hf_app_sym" varchar(50) COLLATE "pg_catalog"."default",
  "hf_app_name" text COLLATE "pg_catalog"."default",
  "hf_hgnc_id" int4,
  "hf_col" varchar(50) COLLATE "pg_catalog"."default",
  "hf_col_alias" text COLLATE "pg_catalog"."default",
  "hf_data" varchar(255) COLLATE "pg_catalog"."default",
  "hf_display" text COLLATE "pg_catalog"."default",
  "hf_score_mod" int4,
  "hf_chr" varchar(255) COLLATE "pg_catalog"."default",
  "hf_trunc" varchar(255) COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."hgnc_adv" OWNER TO "genew";

-- ----------------------------
-- Table structure for hgnc_field
-- ----------------------------
DROP TABLE IF EXISTS "public"."hgnc_field";
CREATE TABLE "public"."hgnc_field" (
  "hf_app_sym" varchar(50) COLLATE "pg_catalog"."default",
  "hf_app_name" text COLLATE "pg_catalog"."default",
  "hf_hgnc_id" int4,
  "hf_col" varchar(50) COLLATE "pg_catalog"."default",
  "hf_col_alias" text COLLATE "pg_catalog"."default",
  "hf_data" varchar(255) COLLATE "pg_catalog"."default",
  "hf_display" text COLLATE "pg_catalog"."default",
  "hf_score_mod" int4,
  "hf_chr" varchar(255) COLLATE "pg_catalog"."default",
  "hf_trunc" varchar(10) COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."hgnc_field" OWNER TO "genew";
COMMENT ON TABLE "public"."hgnc_field" IS 'hgnc_field created by /nas/misc/hgnc/genew/Genew4_maintain/make_quick_search.pl. Wed Feb  5 11:40:14 2014 ';

-- ----------------------------
-- Table structure for hierarchy
-- ----------------------------
DROP TABLE IF EXISTS "public"."hierarchy";
CREATE TABLE "public"."hierarchy" (
  "parent_fam_id" int4 NOT NULL,
  "child_fam_id" int4 NOT NULL
)
;
ALTER TABLE "public"."hierarchy" OWNER TO "genew";

-- ----------------------------
-- Table structure for hierarchy_closure
-- ----------------------------
DROP TABLE IF EXISTS "public"."hierarchy_closure";
CREATE TABLE "public"."hierarchy_closure" (
  "parent_fam_id" int4 NOT NULL,
  "child_fam_id" int4 NOT NULL,
  "distance" int4 NOT NULL DEFAULT 0
)
;
ALTER TABLE "public"."hierarchy_closure" OWNER TO "genew";

-- ----------------------------
-- Table structure for import
-- ----------------------------
DROP TABLE IF EXISTS "public"."import";
CREATE TABLE "public"."import" (
  "imp_id" int4 NOT NULL DEFAULT nextval('import_imp_id_seq'::regclass),
  "imp_source" text COLLATE "pg_catalog"."default",
  "imp_tbl" varchar(255) COLLATE "pg_catalog"."default",
  "imp_name" varchar(255) COLLATE "pg_catalog"."default",
  "imp_data_type" text COLLATE "pg_catalog"."default",
  "imp_index" bool,
  "imp_permit" text COLLATE "pg_catalog"."default",
  "imp_notes" text COLLATE "pg_catalog"."default",
  "imp_sort" int4
)
;
ALTER TABLE "public"."import" OWNER TO "genew";

-- ----------------------------
-- Table structure for key_tbl
-- ----------------------------
DROP TABLE IF EXISTS "public"."key_tbl";
CREATE TABLE "public"."key_tbl" (
  "old_tbl" text COLLATE "pg_catalog"."default",
  "new_tbl" text COLLATE "pg_catalog"."default",
  "old_col" text COLLATE "pg_catalog"."default",
  "new_col" text COLLATE "pg_catalog"."default",
  "comment" text COLLATE "pg_catalog"."default",
  "used_by" text COLLATE "pg_catalog"."default",
  "col_alias" text COLLATE "pg_catalog"."default",
  "data_from" text COLLATE "pg_catalog"."default",
  "tbl_alias" text COLLATE "pg_catalog"."default",
  "data_type" text COLLATE "pg_catalog"."default",
  "import" text COLLATE "pg_catalog"."default",
  "fld_id" int4 NOT NULL DEFAULT nextval(('key_tbl_fld_id_seq'::text)::regclass),
  "id_col" varchar(255) COLLATE "pg_catalog"."default",
  "owner" varchar(255) COLLATE "pg_catalog"."default",
  "longview" text COLLATE "pg_catalog"."default",
  "shortview" text COLLATE "pg_catalog"."default",
  "edit" text COLLATE "pg_catalog"."default",
  "lint" text COLLATE "pg_catalog"."default",
  "lock" varchar(255) COLLATE "pg_catalog"."default",
  "form" varchar(255) COLLATE "pg_catalog"."default",
  "data_mod" text COLLATE "pg_catalog"."default",
  "start_value" text COLLATE "pg_catalog"."default",
  "alias_mod" text COLLATE "pg_catalog"."default",
  "memo" text COLLATE "pg_catalog"."default",
  "notes" text COLLATE "pg_catalog"."default",
  "wiki_link" text COLLATE "pg_catalog"."default",
  "search" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."key_tbl" OWNER TO "genew";

-- ----------------------------
-- Table structure for locus_stats
-- ----------------------------
DROP TABLE IF EXISTS "public"."locus_stats";
CREATE TABLE "public"."locus_stats" (
  "ls_count" int8,
  "ls_type" varchar COLLATE "pg_catalog"."default",
  "ls_group" text COLLATE "pg_catalog"."default",
  "ls_source" text COLLATE "pg_catalog"."default",
  "ls_sort" text COLLATE "pg_catalog"."default",
  "ls_date" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."locus_stats" OWNER TO "genew";

-- ----------------------------
-- Table structure for locus_stats_chr
-- ----------------------------
DROP TABLE IF EXISTS "public"."locus_stats_chr";
CREATE TABLE "public"."locus_stats_chr" (
  "ls_chr" varchar(5) COLLATE "pg_catalog"."default",
  "ls_count" int4,
  "ls_type" varchar(50) COLLATE "pg_catalog"."default",
  "ls_group" varchar(50) COLLATE "pg_catalog"."default",
  "ls_source" varchar(25) COLLATE "pg_catalog"."default",
  "ls_sort" int4,
  "ls_date" varchar(255) COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."locus_stats_chr" OWNER TO "genew";

-- ----------------------------
-- Table structure for mane
-- ----------------------------
DROP TABLE IF EXISTS "public"."mane";
CREATE TABLE "public"."mane" (
  "ncbi_gene_id" int4 NOT NULL,
  "ensembl_gene" varchar(20) COLLATE "pg_catalog"."default" NOT NULL,
  "hgnc_id" int4,
  "symbol" varchar(50) COLLATE "pg_catalog"."default",
  "gene_name" text COLLATE "pg_catalog"."default",
  "refseq_nuc_acc" varchar(20) COLLATE "pg_catalog"."default" NOT NULL,
  "refseq_prot_acc" varchar(20) COLLATE "pg_catalog"."default",
  "ensembl_nuc_acc" varchar(20) COLLATE "pg_catalog"."default" NOT NULL,
  "ensembl_prot_acc" varchar(20) COLLATE "pg_catalog"."default",
  "mane_status" varchar(30) COLLATE "pg_catalog"."default" NOT NULL,
  "grch38_chr" varchar(15) COLLATE "pg_catalog"."default",
  "grch38_chr_start" int4,
  "grch38_chr_end" int4,
  "grch38_chr_starnd" varchar(1) COLLATE "pg_catalog"."default",
  "id" int4 NOT NULL
)
;
ALTER TABLE "public"."mane" OWNER TO "genew";

-- ----------------------------
-- Table structure for otter_ccds_hgnc
-- ----------------------------
DROP TABLE IF EXISTS "public"."otter_ccds_hgnc";
CREATE TABLE "public"."otter_ccds_hgnc" (
  "och_ccds_id" varchar(50) COLLATE "pg_catalog"."default",
  "och_vega_gene_id" varchar(50) COLLATE "pg_catalog"."default",
  "och_hgnc_id" int4
)
;
ALTER TABLE "public"."otter_ccds_hgnc" OWNER TO "genew";

-- ----------------------------
-- Table structure for pub_hgnc
-- ----------------------------
DROP TABLE IF EXISTS "public"."pub_hgnc";
CREATE TABLE "public"."pub_hgnc" (
  "gd_hgnc_id" int4,
  "gd_app_sym" varchar(50) COLLATE "pg_catalog"."default",
  "gd_app_sym_sort" text COLLATE "pg_catalog"."default",
  "gd_app_name" text COLLATE "pg_catalog"."default",
  "gd_status" varchar(20) COLLATE "pg_catalog"."default",
  "gd_locus_type" varchar(100) COLLATE "pg_catalog"."default",
  "gd_prev_sym" text COLLATE "pg_catalog"."default",
  "gd_prev_name" text COLLATE "pg_catalog"."default",
  "gd_aliases" text COLLATE "pg_catalog"."default",
  "gd_name_aliases" text COLLATE "pg_catalog"."default",
  "gd_pub_chrom_map" varchar(255) COLLATE "pg_catalog"."default",
  "gd_pub_chrom_map_sort" varchar(255) COLLATE "pg_catalog"."default",
  "gd_date2app_or_res" date,
  "gd_date_mod" date,
  "gd_date_name_change" date,
  "gd_pub_acc_ids" text COLLATE "pg_catalog"."default",
  "gd_enz_ids" text COLLATE "pg_catalog"."default",
  "gd_pub_eg_id" int4,
  "gd_mgd_id" text COLLATE "pg_catalog"."default",
  "gd_other_ids" text COLLATE "pg_catalog"."default",
  "gd_other_ids_list" text COLLATE "pg_catalog"."default",
  "gd_pubmed_ids" text COLLATE "pg_catalog"."default",
  "gd_pub_refseq_ids" text COLLATE "pg_catalog"."default",
  "gd_gene_fam_name" text COLLATE "pg_catalog"."default",
  "gd_gene_fam_pagename" text COLLATE "pg_catalog"."default",
  "gd_date_sym_change" date,
  "gd_record_type" text COLLATE "pg_catalog"."default",
  "gd_primary_ids" text COLLATE "pg_catalog"."default",
  "gd_secondary_ids" text COLLATE "pg_catalog"."default",
  "gd_pub_hseq_id" varchar(255) COLLATE "pg_catalog"."default",
  "gd_pub_hseq_seq" text COLLATE "pg_catalog"."default",
  "gd_pub_hseq_molecule" text COLLATE "pg_catalog"."default",
  "gd_vega_ids" varchar(18) COLLATE "pg_catalog"."default",
  "gd_lsdb_links" text COLLATE "pg_catalog"."default",
  "gd_pub_ensembl_id" varchar(15) COLLATE "pg_catalog"."default",
  "gd_ccds_ids" text COLLATE "pg_catalog"."default",
  "gd_locus_group" text COLLATE "pg_catalog"."default",
  "gd_cust_sort" varchar(255) COLLATE "pg_catalog"."default",
  "gd_gene_fam_links" text COLLATE "pg_catalog"."default",
  "md_gdb_id" varchar(255) COLLATE "pg_catalog"."default",
  "md_eg_id" int4,
  "md_mim_id" varchar(255) COLLATE "pg_catalog"."default",
  "md_refseq_id" varchar(255) COLLATE "pg_catalog"."default",
  "md_prot_id" text COLLATE "pg_catalog"."default",
  "md_ensembl_id" varchar(15) COLLATE "pg_catalog"."default",
  "gd_ambiguous" bool,
  "md_vega_id" varchar(18) COLLATE "pg_catalog"."default",
  "gd_to_review" bool,
  "md_rna_central_ids" text COLLATE "pg_catalog"."default",
  "md_lncipedia" varchar(15) COLLATE "pg_catalog"."default",
  "md_gtrnadb" varchar(20) COLLATE "pg_catalog"."default",
  "gd_stable_symbol" bool,
  "md_ucsc_id" varchar(50) COLLATE "pg_catalog"."default",
  "md_rgd_id" varchar(50) COLLATE "pg_catalog"."default",
  "md_mgd_id" text COLLATE "pg_catalog"."default",
  "gd_coord" text COLLATE "pg_catalog"."default",
  "md_agr" int4,
  "md_alphafold" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."pub_hgnc" OWNER TO "genew";

-- ----------------------------
-- Table structure for pub_hgnc_backup
-- ----------------------------
DROP TABLE IF EXISTS "public"."pub_hgnc_backup";
CREATE TABLE "public"."pub_hgnc_backup" (
  "gd_hgnc_id" int4,
  "gd_app_sym" varchar(255) COLLATE "pg_catalog"."default",
  "gd_app_sym_sort" text COLLATE "pg_catalog"."default",
  "gd_app_name" text COLLATE "pg_catalog"."default",
  "gd_status" varchar(300) COLLATE "pg_catalog"."default",
  "gd_locus_type" text COLLATE "pg_catalog"."default",
  "gd_prev_sym" text COLLATE "pg_catalog"."default",
  "gd_prev_name" text COLLATE "pg_catalog"."default",
  "gd_aliases" text COLLATE "pg_catalog"."default",
  "gd_name_aliases" text COLLATE "pg_catalog"."default",
  "gd_pub_chrom_map" varchar(255) COLLATE "pg_catalog"."default",
  "gd_pub_chrom_map_sort" varchar(255) COLLATE "pg_catalog"."default",
  "gd_date2app_or_res" date,
  "gd_date_mod" date,
  "gd_date_name_change" date,
  "gd_pub_acc_ids" text COLLATE "pg_catalog"."default",
  "gd_enz_ids" text COLLATE "pg_catalog"."default",
  "gd_pub_eg_id" int4,
  "gd_mgd_id" varchar(255) COLLATE "pg_catalog"."default",
  "gd_other_ids" text COLLATE "pg_catalog"."default",
  "gd_other_ids_list" text COLLATE "pg_catalog"."default",
  "gd_pubmed_ids" text COLLATE "pg_catalog"."default",
  "gd_pub_refseq_ids" text COLLATE "pg_catalog"."default",
  "gd_gene_fam_name" text COLLATE "pg_catalog"."default",
  "gd_date_sym_change" date,
  "gd_record_type" text COLLATE "pg_catalog"."default",
  "gd_primary_ids" text COLLATE "pg_catalog"."default",
  "gd_secondary_ids" text COLLATE "pg_catalog"."default",
  "gd_pub_hseq_id" varchar(20) COLLATE "pg_catalog"."default",
  "gd_pub_hseq_seq" text COLLATE "pg_catalog"."default",
  "gd_pub_hseq_molecule" text COLLATE "pg_catalog"."default",
  "md_gdb_id" varchar(255) COLLATE "pg_catalog"."default",
  "md_eg_id" int4,
  "md_mim_id" varchar(255) COLLATE "pg_catalog"."default",
  "md_refseq_id" varchar(255) COLLATE "pg_catalog"."default",
  "md_prot_id" varchar(255) COLLATE "pg_catalog"."default",
  "md_ensembl_id" varchar(50) COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."pub_hgnc_backup" OWNER TO "genew";

-- ----------------------------
-- Table structure for pub_hgnc_hir
-- ----------------------------
DROP TABLE IF EXISTS "public"."pub_hgnc_hir";
CREATE TABLE "public"."pub_hgnc_hir" (
  "gd_hgnc_id" int4,
  "gd_app_sym" varchar(255) COLLATE "pg_catalog"."default",
  "gd_app_sym_sort" text COLLATE "pg_catalog"."default",
  "gd_app_name" text COLLATE "pg_catalog"."default",
  "gd_status" varchar(300) COLLATE "pg_catalog"."default",
  "gd_locus_type" text COLLATE "pg_catalog"."default",
  "gd_prev_sym" text COLLATE "pg_catalog"."default",
  "gd_prev_name" text COLLATE "pg_catalog"."default",
  "gd_aliases" text COLLATE "pg_catalog"."default",
  "gd_name_aliases" text COLLATE "pg_catalog"."default",
  "gd_pub_chrom_map" varchar(255) COLLATE "pg_catalog"."default",
  "gd_pub_chrom_map_sort" varchar(255) COLLATE "pg_catalog"."default",
  "gd_date2app_or_res" date,
  "gd_date_mod" date,
  "gd_date_name_change" date,
  "gd_pub_acc_ids" text COLLATE "pg_catalog"."default",
  "gd_enz_ids" text COLLATE "pg_catalog"."default",
  "gd_pub_eg_id" int4,
  "gd_mgd_id" varchar(255) COLLATE "pg_catalog"."default",
  "gd_other_ids" text COLLATE "pg_catalog"."default",
  "gd_other_ids_list" text COLLATE "pg_catalog"."default",
  "gd_pubmed_ids" text COLLATE "pg_catalog"."default",
  "gd_pub_refseq_ids" text COLLATE "pg_catalog"."default",
  "gd_gene_fam_name" text COLLATE "pg_catalog"."default",
  "gd_date_sym_change" date,
  "gd_record_type" text COLLATE "pg_catalog"."default",
  "gd_primary_ids" text COLLATE "pg_catalog"."default",
  "gd_secondary_ids" text COLLATE "pg_catalog"."default",
  "gd_pub_hseq_id" varchar(20) COLLATE "pg_catalog"."default",
  "gd_pub_hseq_seq" text COLLATE "pg_catalog"."default",
  "gd_pub_hseq_molecule" text COLLATE "pg_catalog"."default",
  "md_gdb_id" varchar(255) COLLATE "pg_catalog"."default",
  "md_eg_id" int4,
  "md_mim_id" varchar(255) COLLATE "pg_catalog"."default",
  "md_refseq_id" varchar(255) COLLATE "pg_catalog"."default",
  "md_prot_id" varchar(255) COLLATE "pg_catalog"."default",
  "md_ensembl_id" varchar(50) COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."pub_hgnc_hir" OWNER TO "genew";
COMMENT ON TABLE "public"."pub_hgnc_hir" IS 'pub_hgnc_update created by tmp.pl. Thu Aug  9 12:21:47 2007';

-- ----------------------------
-- Table structure for pub_hgnc_oddness
-- ----------------------------
DROP TABLE IF EXISTS "public"."pub_hgnc_oddness";
CREATE TABLE "public"."pub_hgnc_oddness" (
  "gd_hgnc_id" int4,
  "gd_app_sym" varchar(255) COLLATE "pg_catalog"."default",
  "gd_app_sym_sort" text COLLATE "pg_catalog"."default",
  "gd_app_name" text COLLATE "pg_catalog"."default",
  "gd_status" varchar(300) COLLATE "pg_catalog"."default",
  "gd_locus_type" text COLLATE "pg_catalog"."default",
  "gd_prev_sym" text COLLATE "pg_catalog"."default",
  "gd_prev_name" text COLLATE "pg_catalog"."default",
  "gd_aliases" text COLLATE "pg_catalog"."default",
  "gd_name_aliases" text COLLATE "pg_catalog"."default",
  "gd_pub_chrom_map" varchar(255) COLLATE "pg_catalog"."default",
  "gd_pub_chrom_map_sort" varchar(255) COLLATE "pg_catalog"."default",
  "gd_date2app_or_res" date,
  "gd_date_mod" date,
  "gd_date_name_change" date,
  "gd_pub_acc_ids" text COLLATE "pg_catalog"."default",
  "gd_enz_ids" text COLLATE "pg_catalog"."default",
  "gd_pub_eg_id" int4,
  "gd_mgd_id" varchar(255) COLLATE "pg_catalog"."default",
  "gd_other_ids" text COLLATE "pg_catalog"."default",
  "gd_other_ids_list" text COLLATE "pg_catalog"."default",
  "gd_pubmed_ids" text COLLATE "pg_catalog"."default",
  "gd_pub_refseq_ids" text COLLATE "pg_catalog"."default",
  "gd_gene_fam_name" text COLLATE "pg_catalog"."default",
  "gd_date_sym_change" date,
  "gd_record_type" text COLLATE "pg_catalog"."default",
  "gd_primary_ids" text COLLATE "pg_catalog"."default",
  "gd_secondary_ids" text COLLATE "pg_catalog"."default",
  "gd_pub_hseq_id" varchar(20) COLLATE "pg_catalog"."default",
  "gd_pub_hseq_seq" text COLLATE "pg_catalog"."default",
  "gd_pub_hseq_molecule" text COLLATE "pg_catalog"."default",
  "gd_vega_ids" text COLLATE "pg_catalog"."default",
  "gd_lsdb_links" text COLLATE "pg_catalog"."default",
  "md_gdb_id" varchar(255) COLLATE "pg_catalog"."default",
  "md_eg_id" int4,
  "md_mim_id" varchar(255) COLLATE "pg_catalog"."default",
  "md_refseq_id" varchar(255) COLLATE "pg_catalog"."default",
  "md_prot_id" varchar(255) COLLATE "pg_catalog"."default",
  "md_ensembl_id" varchar(50) COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."pub_hgnc_oddness" OWNER TO "genew";

-- ----------------------------
-- Table structure for pub_hgnc_pred
-- ----------------------------
DROP TABLE IF EXISTS "public"."pub_hgnc_pred";
CREATE TABLE "public"."pub_hgnc_pred" (
  "gd_hgnc_id" int4,
  "gd_app_sym" varchar(255) COLLATE "pg_catalog"."default",
  "gd_app_sym_sort" text COLLATE "pg_catalog"."default",
  "gd_app_name" text COLLATE "pg_catalog"."default",
  "gd_status" varchar(300) COLLATE "pg_catalog"."default",
  "gd_locus_type" text COLLATE "pg_catalog"."default",
  "gd_prev_sym" text COLLATE "pg_catalog"."default",
  "gd_prev_name" text COLLATE "pg_catalog"."default",
  "gd_aliases" text COLLATE "pg_catalog"."default",
  "gd_name_aliases" text COLLATE "pg_catalog"."default",
  "gd_pub_chrom_map" varchar(255) COLLATE "pg_catalog"."default",
  "gd_pub_chrom_map_sort" varchar(255) COLLATE "pg_catalog"."default",
  "gd_date2app_or_res" date,
  "gd_date_mod" date,
  "gd_date_name_change" date,
  "gd_pub_acc_ids" text COLLATE "pg_catalog"."default",
  "gd_enz_ids" text COLLATE "pg_catalog"."default",
  "gd_pub_eg_id" int4,
  "gd_mgd_id" varchar(255) COLLATE "pg_catalog"."default",
  "gd_other_ids" text COLLATE "pg_catalog"."default",
  "gd_other_ids_list" text COLLATE "pg_catalog"."default",
  "gd_pubmed_ids" text COLLATE "pg_catalog"."default",
  "gd_pub_refseq_ids" text COLLATE "pg_catalog"."default",
  "gd_gene_fam_name" text COLLATE "pg_catalog"."default",
  "gd_date_sym_change" date,
  "gd_pub_hseq_id" varchar(20) COLLATE "pg_catalog"."default",
  "gd_pub_hseq_seq" text COLLATE "pg_catalog"."default",
  "md_gdb_id" varchar(255) COLLATE "pg_catalog"."default",
  "md_eg_id" int4,
  "md_mim_id" varchar(255) COLLATE "pg_catalog"."default",
  "md_refseq_id" varchar(255) COLLATE "pg_catalog"."default",
  "md_prot_id" varchar(255) COLLATE "pg_catalog"."default",
  "md_ensembl_id" varchar(50) COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."pub_hgnc_pred" OWNER TO "genew";
COMMENT ON TABLE "public"."pub_hgnc_pred" IS 'pub_hgnc_pred_update created by make_g4public.dev.pl. Mon Jun 18 11:49:50 2007';

-- ----------------------------
-- Table structure for pub_hgnc_working
-- ----------------------------
DROP TABLE IF EXISTS "public"."pub_hgnc_working";
CREATE TABLE "public"."pub_hgnc_working" (
  "gd_hgnc_id" int4,
  "gd_app_sym" varchar(255) COLLATE "pg_catalog"."default",
  "gd_app_sym_sort" text COLLATE "pg_catalog"."default",
  "gd_app_name" text COLLATE "pg_catalog"."default",
  "gd_status" varchar(300) COLLATE "pg_catalog"."default",
  "gd_locus_type" text COLLATE "pg_catalog"."default",
  "gd_prev_sym" text COLLATE "pg_catalog"."default",
  "gd_prev_name" text COLLATE "pg_catalog"."default",
  "gd_aliases" text COLLATE "pg_catalog"."default",
  "gd_name_aliases" text COLLATE "pg_catalog"."default",
  "gd_pub_chrom_map" varchar(255) COLLATE "pg_catalog"."default",
  "gd_pub_chrom_map_sort" varchar(255) COLLATE "pg_catalog"."default",
  "gd_date2app_or_res" date,
  "gd_date_mod" date,
  "gd_date_name_change" date,
  "gd_pub_acc_ids" text COLLATE "pg_catalog"."default",
  "gd_enz_ids" text COLLATE "pg_catalog"."default",
  "gd_pub_eg_id" int4,
  "gd_mgd_id" varchar(255) COLLATE "pg_catalog"."default",
  "gd_other_ids" text COLLATE "pg_catalog"."default",
  "gd_other_ids_list" text COLLATE "pg_catalog"."default",
  "gd_pubmed_ids" text COLLATE "pg_catalog"."default",
  "gd_pub_refseq_ids" text COLLATE "pg_catalog"."default",
  "gd_gene_fam_name" text COLLATE "pg_catalog"."default",
  "gd_date_sym_change" date,
  "gd_record_type" text COLLATE "pg_catalog"."default",
  "gd_primary_ids" text COLLATE "pg_catalog"."default",
  "gd_secondary_ids" text COLLATE "pg_catalog"."default",
  "gd_pub_hseq_id" varchar(20) COLLATE "pg_catalog"."default",
  "gd_pub_hseq_seq" text COLLATE "pg_catalog"."default",
  "gd_pub_hseq_molecule" text COLLATE "pg_catalog"."default",
  "md_gdb_id" varchar(255) COLLATE "pg_catalog"."default",
  "md_eg_id" int4,
  "md_mim_id" varchar(255) COLLATE "pg_catalog"."default",
  "md_refseq_id" varchar(255) COLLATE "pg_catalog"."default",
  "md_prot_id" varchar(255) COLLATE "pg_catalog"."default",
  "md_ensembl_id" varchar(50) COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."pub_hgnc_working" OWNER TO "genew";

-- ----------------------------
-- Table structure for public_data
-- ----------------------------
DROP TABLE IF EXISTS "public"."public_data";
CREATE TABLE "public"."public_data" (
  "st_hgnc_id" text COLLATE "pg_catalog"."default",
  "st_app_sym" text COLLATE "pg_catalog"."default",
  "st_app_sym_sort" text COLLATE "pg_catalog"."default",
  "st_app_name" text COLLATE "pg_catalog"."default",
  "st_status" text COLLATE "pg_catalog"."default",
  "st_locus_type" text COLLATE "pg_catalog"."default",
  "st_prev_sym" text COLLATE "pg_catalog"."default",
  "st_prev_name" text COLLATE "pg_catalog"."default",
  "st_aliases" text COLLATE "pg_catalog"."default",
  "st_pub_chrom_map" text COLLATE "pg_catalog"."default",
  "st_pub_chrom_map_sort" text COLLATE "pg_catalog"."default",
  "st_date2app_or_res" text COLLATE "pg_catalog"."default",
  "st_date_mod" text COLLATE "pg_catalog"."default",
  "st_date_name_change" text COLLATE "pg_catalog"."default",
  "st_pub_acc_num" text COLLATE "pg_catalog"."default",
  "st_enz_ids" text COLLATE "pg_catalog"."default",
  "st_pub_locuslink_id" text COLLATE "pg_catalog"."default",
  "st_mgd_id" text COLLATE "pg_catalog"."default",
  "st_other_ids" text COLLATE "pg_catalog"."default",
  "st_pubmed_ids" text COLLATE "pg_catalog"."default",
  "st_pub_refseq" text COLLATE "pg_catalog"."default",
  "st_gene_fam_name" text COLLATE "pg_catalog"."default",
  "gt_gdb_id" text COLLATE "pg_catalog"."default",
  "lt_ll_id" text COLLATE "pg_catalog"."default",
  "lt_ll_mim" text COLLATE "pg_catalog"."default",
  "lt_ll_refseq" text COLLATE "pg_catalog"."default",
  "pt_swissprot_id" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."public_data" OWNER TO "genew";

-- ----------------------------
-- Table structure for pubnome_delme
-- ----------------------------
DROP TABLE IF EXISTS "public"."pubnome_delme";
CREATE TABLE "public"."pubnome_delme" (
  "hgnc" int4,
  "date_approved" text COLLATE "pg_catalog"."default",
  "status" text COLLATE "pg_catalog"."default",
  "gene_name" text COLLATE "pg_catalog"."default",
  "symbol" varchar(255) COLLATE "pg_catalog"."default",
  "previous_symbol" text COLLATE "pg_catalog"."default",
  "enzyme_id" text COLLATE "pg_catalog"."default",
  "chrom_map" text COLLATE "pg_catalog"."default",
  "aliases" text COLLATE "pg_catalog"."default",
  "mgi_number" text COLLATE "pg_catalog"."default",
  "pmid1" text COLLATE "pg_catalog"."default",
  "pmid2" text COLLATE "pg_catalog"."default",
  "accession_number" text COLLATE "pg_catalog"."default",
  "previous_gene_name" text COLLATE "pg_catalog"."default",
  "gdb_id" text COLLATE "pg_catalog"."default",
  "locuslink_id" text COLLATE "pg_catalog"."default",
  "omim" text COLLATE "pg_catalog"."default",
  "ref_seq" text COLLATE "pg_catalog"."default",
  "swiss_prot_id" text COLLATE "pg_catalog"."default",
  "all_text" text COLLATE "pg_catalog"."default",
  "all_id" text COLLATE "pg_catalog"."default",
  "prev_and_alias" text COLLATE "pg_catalog"."default",
  "symb_prev_and_alias" text COLLATE "pg_catalog"."default",
  "prev_html" text COLLATE "pg_catalog"."default",
  "alias_html" text COLLATE "pg_catalog"."default",
  "sort_symbol" text COLLATE "pg_catalog"."default",
  "sort_chrom_map" text COLLATE "pg_catalog"."default",
  "ensembl_id" varchar(50) COLLATE "pg_catalog"."default",
  "record_type" varchar(255) COLLATE "pg_catalog"."default",
  "primary_ids" text COLLATE "pg_catalog"."default",
  "secondary_ids" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."pubnome_delme" OWNER TO "genew";

-- ----------------------------
-- Table structure for specialist
-- ----------------------------
DROP TABLE IF EXISTS "public"."specialist";
CREATE TABLE "public"."specialist" (
  "id" int4 NOT NULL,
  "name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "address" text COLLATE "pg_catalog"."default" NOT NULL,
  "url" varchar(255) COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."specialist" OWNER TO "genew";

-- ----------------------------
-- Table structure for stats_delme
-- ----------------------------
DROP TABLE IF EXISTS "public"."stats_delme";
CREATE TABLE "public"."stats_delme" (
  "db_data" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."stats_delme" OWNER TO "genew";

-- ----------------------------
-- Table structure for symbol_lookup
-- ----------------------------
DROP TABLE IF EXISTS "public"."symbol_lookup";
CREATE TABLE "public"."symbol_lookup" (
  "sl_symbol" varchar(255) COLLATE "pg_catalog"."default",
  "sl_hgnc_id" int4,
  "sl_source" varchar(50) COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."symbol_lookup" OWNER TO "genew";
COMMENT ON TABLE "public"."symbol_lookup" IS 'symbol_lookup created by /nas/misc/hgnc/genew/Genew4_maintain/make_symbol_lookup.pl. Wed Feb  5 12:14:05 2014 ';

-- ----------------------------
-- Table structure for target
-- ----------------------------
DROP TABLE IF EXISTS "public"."target";
CREATE TABLE "public"."target" (

)
;
ALTER TABLE "public"."target" OWNER TO "genew";

-- ----------------------------
-- Table structure for tax_names_tbl
-- ----------------------------
DROP TABLE IF EXISTS "public"."tax_names_tbl";
CREATE TABLE "public"."tax_names_tbl" (
  "tax_id" text COLLATE "pg_catalog"."default",
  "name_txt" text COLLATE "pg_catalog"."default",
  "uniq_name" text COLLATE "pg_catalog"."default",
  "name_class" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."tax_names_tbl" OWNER TO "genew";

-- ----------------------------
-- Table structure for test
-- ----------------------------
DROP TABLE IF EXISTS "public"."test";
CREATE TABLE "public"."test" (
  "hgnc" text COLLATE "pg_catalog"."default",
  "date_approved" text COLLATE "pg_catalog"."default",
  "status" text COLLATE "pg_catalog"."default",
  "gene_name" text COLLATE "pg_catalog"."default",
  "symbol" text COLLATE "pg_catalog"."default",
  "previous_symbol" text COLLATE "pg_catalog"."default",
  "enzyme_id" text COLLATE "pg_catalog"."default",
  "chrom_map" text COLLATE "pg_catalog"."default",
  "aliases" text COLLATE "pg_catalog"."default",
  "mgi_number" text COLLATE "pg_catalog"."default",
  "pmid1" text COLLATE "pg_catalog"."default",
  "pmid2" text COLLATE "pg_catalog"."default",
  "accession_number" text COLLATE "pg_catalog"."default",
  "previous_gene_name" text COLLATE "pg_catalog"."default",
  "gdb_id" text COLLATE "pg_catalog"."default",
  "locuslink_id" text COLLATE "pg_catalog"."default",
  "omim" text COLLATE "pg_catalog"."default",
  "ref_seq" text COLLATE "pg_catalog"."default",
  "swiss_prot_id" text COLLATE "pg_catalog"."default",
  "all_text" text COLLATE "pg_catalog"."default",
  "all_id" text COLLATE "pg_catalog"."default",
  "prev_and_alias" text COLLATE "pg_catalog"."default",
  "symb_prev_and_alias" text COLLATE "pg_catalog"."default",
  "prev_html" text COLLATE "pg_catalog"."default",
  "alias_html" text COLLATE "pg_catalog"."default",
  "sort_symbol" text COLLATE "pg_catalog"."default",
  "sort_chrom_map" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."test" OWNER TO "genew";

-- ----------------------------
-- Table structure for tmp
-- ----------------------------
DROP TABLE IF EXISTS "public"."tmp";
CREATE TABLE "public"."tmp" (
  "new_tbl" text COLLATE "pg_catalog"."default",
  "new_col" text COLLATE "pg_catalog"."default",
  "data_type" text COLLATE "pg_catalog"."default",
  "notes" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."tmp" OWNER TO "genew";

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
SELECT setval('"public"."cell_cell_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
SELECT setval('"public"."family_alias_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
SELECT setval('"public"."family_new_fam_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
SELECT setval('"public"."filestore_line_id_seq"', 2943553, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
SELECT setval('"public"."import_imp_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
SELECT setval('"public"."key_tbl_fld_id_seq"', 1, false);

-- ----------------------------
-- Indexes structure for table external_resource
-- ----------------------------
CREATE UNIQUE INDEX "external_resource_id_key" ON "public"."external_resource" USING btree (
  "id" "pg_catalog"."int4_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table external_resource
-- ----------------------------
ALTER TABLE "public"."external_resource" ADD CONSTRAINT "external_resource_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table family_alias
-- ----------------------------
ALTER TABLE "public"."family_alias" ADD CONSTRAINT "family_alias_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table family_has_external_resource
-- ----------------------------
ALTER TABLE "public"."family_has_external_resource" ADD CONSTRAINT "family_has_external_resource_pkey" PRIMARY KEY ("family_id", "ext_id");

-- ----------------------------
-- Primary Key structure for table family_has_specialist
-- ----------------------------
ALTER TABLE "public"."family_has_specialist" ADD CONSTRAINT "family_has_specialist_pkey" PRIMARY KEY ("fam_id", "specialist_id");

-- ----------------------------
-- Indexes structure for table family_new
-- ----------------------------
CREATE UNIQUE INDEX "family_new_id_key" ON "public"."family_new" USING btree (
  "id" "pg_catalog"."int4_ops" ASC NULLS LAST
);
CREATE INDEX "ind_name" ON "public"."family_new" USING btree (
  "abbreviation" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table family_new
-- ----------------------------
ALTER TABLE "public"."family_new" ADD CONSTRAINT "family_new_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table gene_has_family
-- ----------------------------
ALTER TABLE "public"."gene_has_family" ADD CONSTRAINT "gene_has_family_pkey" PRIMARY KEY ("hgnc_id", "family_id");

-- ----------------------------
-- Primary Key structure for table hierarchy
-- ----------------------------
ALTER TABLE "public"."hierarchy" ADD CONSTRAINT "heirarchy_pkey" PRIMARY KEY ("parent_fam_id", "child_fam_id");

-- ----------------------------
-- Primary Key structure for table hierarchy_closure
-- ----------------------------
ALTER TABLE "public"."hierarchy_closure" ADD CONSTRAINT "hierarchy_closure_pkey" PRIMARY KEY ("parent_fam_id", "child_fam_id", "distance");

-- ----------------------------
-- Indexes structure for table mane
-- ----------------------------
CREATE INDEX "mane_ensembl_gene_idx" ON "public"."mane" USING btree (
  "ensembl_gene" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "mane_ncbi_gene_idx" ON "public"."mane" USING btree (
  "ncbi_gene_id" "pg_catalog"."int4_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table mane
-- ----------------------------
ALTER TABLE "public"."mane" ADD CONSTRAINT "mane_pk" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table otter_ccds_hgnc
-- ----------------------------
CREATE INDEX "otter_ccds_hgnc_och_ccds_id_index" ON "public"."otter_ccds_hgnc" USING btree (
  "och_ccds_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "otter_ccds_hgnc_och_hgnc_id_index" ON "public"."otter_ccds_hgnc" USING btree (
  "och_hgnc_id" "pg_catalog"."int4_ops" ASC NULLS LAST
);
CREATE INDEX "otter_ccds_hgnc_och_vega_gene_id_index" ON "public"."otter_ccds_hgnc" USING btree (
  "och_vega_gene_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Indexes structure for table pub_hgnc
-- ----------------------------
CREATE INDEX "pub_hgnc_gd_app_sym_index" ON "public"."pub_hgnc" USING btree (
  "gd_app_sym" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "pub_hgnc_gd_hgnc_id_index" ON "public"."pub_hgnc" USING btree (
  "gd_hgnc_id" "pg_catalog"."int4_ops" ASC NULLS LAST
);
CREATE INDEX "pub_hgnc_gd_pub_eg_id_index" ON "public"."pub_hgnc" USING btree (
  "gd_pub_eg_id" "pg_catalog"."int4_ops" ASC NULLS LAST
);
CREATE INDEX "pub_hgnc_gd_pub_ensembl_id_index" ON "public"."pub_hgnc" USING btree (
  "gd_pub_ensembl_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "pub_hgnc_md_agr_index" ON "public"."pub_hgnc" USING btree (
  "md_agr" "pg_catalog"."int4_ops" ASC NULLS LAST
);
CREATE INDEX "pub_hgnc_md_eg_id_index" ON "public"."pub_hgnc" USING btree (
  "md_eg_id" "pg_catalog"."int4_ops" ASC NULLS LAST
);
CREATE INDEX "pub_hgnc_md_ensembl_id_index" ON "public"."pub_hgnc" USING btree (
  "md_ensembl_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "pub_hgnc_md_vega_id_index" ON "public"."pub_hgnc" USING btree (
  "md_vega_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Indexes structure for table specialist
-- ----------------------------
CREATE UNIQUE INDEX "specialist_id_key" ON "public"."specialist" USING btree (
  "id" "pg_catalog"."int4_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table specialist
-- ----------------------------
ALTER TABLE "public"."specialist" ADD CONSTRAINT "specialist_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Foreign Keys structure for table family_alias
-- ----------------------------
ALTER TABLE "public"."family_alias" ADD CONSTRAINT "fk_family_alias_family_new_1" FOREIGN KEY ("family_id") REFERENCES "public"."family_new" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table family_has_external_resource
-- ----------------------------
ALTER TABLE "public"."family_has_external_resource" ADD CONSTRAINT "fk_family_has_external_resource_external_resource_1" FOREIGN KEY ("ext_id") REFERENCES "public"."external_resource" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."family_has_external_resource" ADD CONSTRAINT "fk_family_has_external_resource_family_new_1" FOREIGN KEY ("family_id") REFERENCES "public"."family_new" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table family_has_specialist
-- ----------------------------
ALTER TABLE "public"."family_has_specialist" ADD CONSTRAINT "fk_family_has_specialist_family_new_1" FOREIGN KEY ("fam_id") REFERENCES "public"."family_new" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."family_has_specialist" ADD CONSTRAINT "fk_family_has_specialist_specialist_1" FOREIGN KEY ("specialist_id") REFERENCES "public"."specialist" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table gene_has_family
-- ----------------------------
ALTER TABLE "public"."gene_has_family" ADD CONSTRAINT "fk_gene_has_family_family_new_1" FOREIGN KEY ("family_id") REFERENCES "public"."family_new" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table hierarchy
-- ----------------------------
ALTER TABLE "public"."hierarchy" ADD CONSTRAINT "fk_hierarchy_family_new_1" FOREIGN KEY ("parent_fam_id") REFERENCES "public"."family_new" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."hierarchy" ADD CONSTRAINT "fk_hierarchy_family_new_2" FOREIGN KEY ("child_fam_id") REFERENCES "public"."family_new" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table hierarchy_closure
-- ----------------------------
ALTER TABLE "public"."hierarchy_closure" ADD CONSTRAINT "fk_hierarchy_closure_family_new_1" FOREIGN KEY ("parent_fam_id") REFERENCES "public"."family_new" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."hierarchy_closure" ADD CONSTRAINT "fk_hierarchy_closure_family_new_2" FOREIGN KEY ("child_fam_id") REFERENCES "public"."family_new" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
