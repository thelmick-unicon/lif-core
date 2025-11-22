# LIF Orchestrator

This project plays a significant role in coordinating and running data jobs to fetch data from the source data environments as specified in the jobs. The  **Orchestrator** ensures that the **Query Planner** can access the required data from its sources without having to know connection or format details about the source data systems. This abstraction provides a highly available, fault-tolerant, and integrated data environment over external data systems for the LIF system enabling real-time data exchange across heterogeneous data environments.

The **Orchestrator** helps the **Query Planner** fulfil LIF Queries that require data not available with the **LIF Cache** yet. While the **LIF Cache** provides access to *cached* source data, the **Orchestrator** offers *real-time* access to the source data systems.

The **Orchestrator** exposes an API via `bases/lif/orchestrator_restapi/core.py`. The **Orchestrator** leverages Dagster to execute on the jobs requested from the **Query Planner**.



