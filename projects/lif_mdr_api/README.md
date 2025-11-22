# LIF Metadata Repository (MDR) API

The **Metadata Repository (MDR)** is a key component of LIF. It provides the capabilities to maintain the *LIF data model* in all of its iterations---including an *organization-specific LIF data model* and *partner LIF data models.* The **MDR** and *LIF data model* will be maintained by the steward or organization governing LIF.

The **MDR** is a standalone component that serves as the LIF system of record. It is where individuals from implementing organizations maintain their *organization-specific LIF data model* and *partner LIF data models* through a graphical user interface.

Additionally, the **MDR** provides the capability for the organization to maintain source data model(s) and mappings to transform data into a structure aligned to the *organization-specific LIF data model*.

The **MDR** will enable the organization to define which elements of its *organization-specific LIF data model* can be shared externally as its *partner-accessible LIF data model*. As a Possible Future Roadmap Item, the **MDR** will also allow the retrieval of the *partner-accessible LIF data model* from partners that have allowed for queries via **LIF API**.

The API is created with FastAPI and dependency management is done by UV.

## Quickstart
 - Before running the API, the DB should be up and running.
 - Copy the `mdr-api.env.example` file and rename it as `mdr-api.env` under the `projects/lif_mdr_api` folder and add/adjust the database, CORs, and auth details.


### Deployment:
- Goto `projects/lif_mdr_api` folder and run :
    ```
    docker-compose up --build -d
    ```
- Once deployed you can see swagger at http://localhost:8012/docs#


## Test Cases

- This repository includes a suite of unit tests under `test/components/lif/mdr_services`. The tests use `pytest` and cover the FASTAPI services: `datamodel_service`, `entity_service`, `attribute_service`, and `schema_generation_service`. 
- You can run the tests as such in `test/components/lif/mdr_services`:
    - `pytest test_attribute_service.py`
    - `pytest test_datamodel_service.py`
    - `pytest test_entity_service.py`
    - `pytest test_schema_generation_service.py`
