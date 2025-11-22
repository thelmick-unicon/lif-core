CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
CREATE EXTENSION IF NOT EXISTS pgaudit;
DO
$do$
BEGIN
   IF EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'mdr') THEN

      RAISE NOTICE 'Role "mdr" already exists. Skipping.';
   ELSE
      CREATE ROLE mdr LOGIN;
   END IF;
END
$do$;
GRANT rds_iam TO mdr;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO mdr;
GRANT USAGE ON SCHEMA public TO mdr; 
ALTER DEFAULT PRIVILEGES IN SCHEMA public 
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO mdr;
