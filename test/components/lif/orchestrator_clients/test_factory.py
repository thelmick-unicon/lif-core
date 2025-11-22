import pytest
from typing import Dict, Any

from lif.orchestrator_clients.factory import OrchestratorFactory, OrchestratorNotFoundError
from lif.orchestrator_service.core import OrchestratorClient
from lif.datatypes import OrchestratorJobDefinition, OrchestratorJob, OrchestratorJobStatus


class FakeClient(OrchestratorClient):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.submitted: list[str] = []

    async def post_job(self, job_definition: OrchestratorJobDefinition) -> str:  # type: ignore[override]
        job_id = job_definition.lif_query_plan.__class__.__name__  # just something deterministic
        self.submitted.append(job_id)
        return job_id

    async def get_job_status(self, job_id: str) -> OrchestratorJob:  # type: ignore[override]
        # minimal fake implementation always returns STARTING
        return OrchestratorJob(job_id=job_id, status=OrchestratorJobStatus.STARTING)


def test_create_returns_dagster_instance(monkeypatch):
    # We only assert type name to avoid importing heavy dagster libs in assertions
    client = OrchestratorFactory.create("dagster", config={})
    assert client.__class__.__name__ == "DagsterClient"


def test_create_invalid_raises():
    with pytest.raises(OrchestratorNotFoundError):
        OrchestratorFactory.create("nope", config={})


def test_register_and_create_new_type():
    OrchestratorFactory.register("fake", FakeClient, override=True)
    client = OrchestratorFactory.create("fake", config={"x": 1})
    assert isinstance(client, FakeClient)
    assert client.config == {"x": 1}


def test_register_duplicate_without_override_fails():
    OrchestratorFactory.register("dup", FakeClient, override=True)
    with pytest.raises(ValueError):
        OrchestratorFactory.register("dup", FakeClient, override=False)


def test_list_returns_copy():
    listing = OrchestratorFactory.list()
    listing["dagster"] = FakeClient  # mutate copy
    assert OrchestratorFactory._registry["dagster"].__name__ == "DagsterClient"  # original unchanged
