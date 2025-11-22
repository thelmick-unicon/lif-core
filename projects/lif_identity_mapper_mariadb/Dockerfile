FROM mariadb:10.11

# Switch to root user before installing
USER root

# Copy script that will move the proper seed file to the proper location
COPY --chmod=0755 01-seed-file-setup.sh /docker-entrypoint-initdb.d/

# Add the schema DDL
COPY 02-ddl.sql /docker-entrypoint-initdb.d/

# Add the placeholder seed file
COPY --chmod=0766 03-seed.sql /docker-entrypoint-initdb.d/

# Add the seed data files
COPY sample_data /seed_data
