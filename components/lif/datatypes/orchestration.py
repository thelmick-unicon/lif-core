from enum import Enum
from typing import Any, Dict, List

from pydantic import BaseModel, Field

from .core import LIFQueryPlan, LIFPersonIdentifier, LIFFragment


class OrchestratorJobRequest(BaseModel):
    """
    Pydantic model for an orchestrator job request.
    Attributes:
        lif_query_plan (LIFQueryPlan): LIF Query Plan for the orchestration.
        async_ (bool): Whether the orchestration should be run asynchronously.
    """

    lif_query_plan: LIFQueryPlan = Field(..., description="LIF Query Plan for the orchestration")
    async_: bool = Field(True, alias="async")


class OrchestratorJobRequestResponse(BaseModel):
    """
    Pydantic model for the response for an orchestrator job request.

    Attributes:
        run_id (str): Run ID for the orchestration.
    """

    run_id: str = Field(..., description="Run ID for the orchestration")


class OrchestratorJobQueryPlanPartResults(BaseModel):
    """
    Pydantic model for the result of a single part of an orchestrator job.

    Attributes:
        information_source_id (str): Identifier for the information source.
        adapter_id (str): Identifier for the adapter.
        data_timestamp (str): Timestamp of the data retrieval.
        fragments (List[LIFFragment]): List of LIF Fragments.
        error (str | None): Optional error message if the part failed.
    """

    information_source_id: str = Field(..., description="Identifier for the information source")
    adapter_id: str = Field(..., description="Identifier for the adapter")
    data_timestamp: str | None = Field(None, description="Timestamp of the data retrieval")
    person_id: LIFPersonIdentifier = Field(..., description="Person ID for the query plan part")
    fragments: List[LIFFragment] = Field(..., description="List of LIF Fragments")
    error: str | None = Field(None, description="Error message if the part failed")


class OrchestratorJobResults(BaseModel):
    """
    Pydantic model for the result of an orchestrator job.

    Attributes:
        run_id (str): Run ID for the orchestration.
        query_plan_part_results (List[OrchestratorJobQueryPlanPartResults]): List of results for each part of the query plan.
    """

    run_id: str = Field(..., description="Run ID for the orchestration")
    query_plan_part_results: List[OrchestratorJobQueryPlanPartResults] = Field(
        ..., description="List of results for each part of the query plan"
    )


class OrchestratorJobStatus(Enum):
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class OrchestratorJob(BaseModel):
    job_id: str = Field(..., description="Unique identifier for the job")
    status: OrchestratorJobStatus = Field(..., description="Current status of the job")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional job metadata")

    model_config = {"json_encoders": {OrchestratorJobStatus: lambda v: v.value}}


class OrchestratorJobDefinition(BaseModel):
    lif_query_plan: LIFQueryPlan = Field(..., description="LIF Query Plan to be parsed into orchestrated job")

    # TODO: Add validation
