CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
CREATE EXTENSION IF NOT EXISTS pgaudit;
DO
$do$
BEGIN
   IF EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'dagster') THEN

      RAISE NOTICE 'Role "dagster" already exists. Skipping.';
   ELSE
      CREATE ROLE dagster LOGIN;
   END IF;
END
$do$;
GRANT rds_iam TO dagster;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO dagster;
GRANT USAGE ON SCHEMA public TO dagster; 
ALTER DEFAULT PRIVILEGES IN SCHEMA public 
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO dagster;
