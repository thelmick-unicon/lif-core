# LIF Metadata Repository (MDR) Database

The **Metadata Repository (MDR)** is a key component of LIF. It provides the capabilities to maintain the *LIF data model* in all of its iterations---including an *organization-specific LIF data model* and *partner LIF data models.* The **MDR** and *LIF data model* will be maintained by the steward or organization governing LIF.

The **MDR** is a standalone component that serves as the LIF system of record. It is where individuals from implementing organizations maintain their *organization-specific LIF data model* and *partner LIF data models* through a graphical user interface.

Additionally, the **MDR** provides the capability for the organization to maintain source data model(s) and mappings to transform data into a structure aligned to the *organization-specific LIF data model*.

The **MDR** will enable the organization to define which elements of its *organization-specific LIF data model* can be shared externally as its *partner-accessible LIF data model*. As a Possible Future Roadmap Item, the **MDR** will also allow the retrieval of the *partner-accessible LIF data model* from partners that have allowed for queries via **LIF API**.

MDR uses a PostgreSQL database to persist the metadata on data schemas.

The database is initialized with a dataset of multiple schemas and mappings.

## Quick start

### Database Only

Default configurations should be sufficient to initialize the database for a non-production environment with the commands:

```bash
# From the root of [lif-main]
cd projects/lif_mdr_database
docker compose down && docker compose build --no-cache && docker compose up -d
```

Available configurations are exposed in the docker compose file: `projects/lif_mdr_database/docker-compose.yaml`.

The database can be accessed from the host system via port `5445`.

### As part of the LIF Ecosystem

Similar to the 'Database Only' flow, the all-in-one docker compose flow has default configurations for the MDR database meant for a non-production environment:

```bash
# From the root of [lif-main]
docker-compose -f deployments/advisor-demo-docker/docker-compose.yml up --build
```

Available configurations are exposed in the docker compose file: `deployments/advisor-demo-docker/docker-compose.yml`.

The database can be accessed from the host system via port `5445`.

### Updating MDR Database Seed Data
When you update metadata in the MDR UI, MDR API, or manually in the DB, if you want your changes to persist, you will need to export the `backup.sql` and copy this to `V1.1__metadata_repository_init.sql`.
1. `cd projects/lif_mdr_database`  
2. Create a new copy of backup.sql:
```
PGPASSWORD='postgres' pg_dump \
  --host=localhost --port=5445 --username=postgres \
  --file=backup.sql \
  --no-owner --no-privileges \
  LIF
```
3. Copy backup.sql and paste it into sam/mdr-database/flyway/flyway-files/flyway/sql/mdr/V1.1\_\_metadata\_repository\_init.sql. Since it's a large file, I usually copy the file directly, not its contents. And then rename the files appropriately and delete the old one.
4. Open V1.1\_\_metadata\_repository\_init.sql and find near the top `\restrict ...` and comment out this line. Find near the bottom `\unrestrict ...` and comment out this line.  
5. Once your PR is merged, you will need to ask someone with a Linux OS to redeploy the MDR DB in AWS.

---

- In folder `mdr_database`, we have dockerize postgres with restore script `backup.sql`.
- This script will create the schema and add all the crosswalk workbook data into the database in addition to 2 other sample data models:
    - StateU OB3: this is an example of OB3 data model that StateU uses for LIF implementation. This is just to show how organization data model looks in the database.
    - StateU LIF: this is an example of LIF extension that StateU has done for LIF implementation. This is just to show how LIF extension looks in the database.
- If you are not using this dockerize postgres and you have your own postgres DB, you can run:
```bash
psql --host=$POSTGRES_HOST --username=$POSTGRES_USER --dbname=$POSTGRES_DB -f <LOCATION TO backup.sql FILE>
```
    - Replace your database details and make sure to export environment variable named `PGPASSWORD` as your postgres password.
- Using DBeaver or your preferred postgres client, confirm that there are tables in your LIF database on port 5445.

**NOTES:** 
- Right now the code is only working with postgres database.
- If you are going to use APIs, create `db_creds.env ` file under the `metadata-repo-api` folder (if it does not already exist) and update the db credentials as per the changes in the above environmental variables.

**TROUBLESHOOTING:**
- If you run into a situation where you are not seeing new data in the MDR, first be sure that you have the latest data from the repo. Another solution is to run `docker compose down && docker compose build --no-cache && docker compose up -d` when building the mdr_database and metadata-repo-api docker containers. This will clear the cache.
- If you have the MDR UI up and running, but do not see any data models, ensure that your db_creds.env file has the correct DB name, user, password, and port.
