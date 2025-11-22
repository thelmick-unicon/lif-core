# Dagster OSS for Docker Compose

This project defines the *Dagster OSS*-focused deployment artifacts, used in Docker Compose, that are downstream from the **Orchestrator**: namely the **Code Location** (Adapters), **Web Server** (*Dagster* UI), and **Daemon** (*Dagster* Job Scheduler and Executor). These deployment artifacts are used to deploy the code from
`/orchestrators/dagster/lif-orchestrator` in Docker Compose. The Dockerfiles defined in this project can be utilized in various `docker_compose.yml` files in this repository, but are at least used in `deployments/advisor-demo-docker/docker-compose.yml`.

## Web Server
This is the API and UX of *Dagster*. Among other activities, a user can view job execution results.

The **Web Server** is defined in the `projects/dagster_docker_compose/Dockerfile.dagster` file which also defines the **Daemon**.

When ran locally via `advisor-demo-docker`, the Dagster **Web Server** URL is http://localhost:3000 .

## Daemon
Among other responsibilities, this executes the *Dagster* runs against the **Code Location**.

The **Daemon** is defined in the `projects/dagster_docker_compose/Dockerfile.dagster` file which also defines the **Web Server**.

## Code Location
This runs the gRPC server that uses code (known as **Adapters**) to access the source data systems for execution by the Dagster **Daemon**.

The **Code Location** is defined in the `projects/dagster_docker_compose/Dockerfile.code_location` file.

Each **Adapter** in a LIF implementation provides an interface by which the user can access their data as requested from an internal or external source data system. **Adapters** query source data systems and return requested learner data in a LIF-compliant data format or in a source data format defined in the **MDR**. With it's ability to transfer learner's data from data source systems to a LIF system, **Adapters** connect LIF implementations to a wide array of source data systems, including proprietary systems.

There are several varieties of **Adapters** that can be used. Currently, the LIF Initiative offers a *LIF to LIF* **Adapter** and an *Example Data Source to LIF* **Adapter**.

### LIF to LIF Adapter
This **Adapter** can connect and query a source data system that responds in LIF format.

### Example Data Source to LIF Adapter
This **Adapter** can connect and query a source data system that responds in non-LIF format. This output is then used as input to the **Transformer** that leverages mappings from **MDR** to convert non-LIF formatted data into the LIF format.

The *Example Data Source* project (`projects/lif_example_data_source_rest_api`) is the source data system, and intended to be a reference implementation for other non-LIF APIs in an adopter's ecosystem.

## PostgreSQL
As a notable mention, though not specified in this project, *Dagster* also uses PostgreSQL to run its services. This database is defined in `deployments/advisor-demo-docker/docker-compose.yml > postgres-dagster`

## Additional Notes
More information on deploying *Dagster OSS* can be found at https://docs.dagster.io/deployment .

### `run_launcher` in `dagster.yaml`
From the [Dagster Run Launcher docs](https://docs.dagster.io/deployment/execution/run-launchers):
> A launch operation allocates computational resources (e.g. a process, a container, a Kubernetes pod, etc) to carry out a run execution and then instigates the execution.

For speed's sake, the code is using the `DefaultRunLauncher`.

If better isolation is desired, the `DockerRunLauncher` can be configured in `dagster.yaml` instead (just comment/uncomment as necessary). Handling for environment variables when using the `DockerRunLauncher` deviates from the Dagster docs and instead utilizes methodology defined [here](https://github.com/dagster-io/dagster/discussions/21100#discussioncomment-10999238). See the notes in `code_location_entrypoint.sh` and `Dockerfile.code_location` for more information.
