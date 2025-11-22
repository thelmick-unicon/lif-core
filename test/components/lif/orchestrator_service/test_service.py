import asyncio
from typing import Any, Optional
import pytest
import os

# Ensure required env var is present before importing modules that read it at import time.
os.environ.setdefault("LIF_ADAPTER__LIF_TO_LIF__GRAPHQL_API_URL", "http://lif-to-lif.test/graphql")

from lif.orchestrator_service.service import OrchestratorService
from lif.datatypes import LIFQueryPlan, LIFQueryPlanPart, LIFPersonIdentifier, OrchestratorJob, OrchestratorJobStatus


# env var set above at import time


class FakeOrchestrator:
    def __init__(self):
        self.received_job_definition: Any = None
        self.job_status_to_return: OrchestratorJob = OrchestratorJob(
            job_id="test", status=OrchestratorJobStatus.RUNNING
        )
        self.post_job_exception: Optional[Exception] = None
        self.post_job_return: str = "run-123"

    async def post_job(self, job_definition):
        self.received_job_definition = job_definition
        if self.post_job_exception:
            raise self.post_job_exception
        return self.post_job_return

    async def get_job_status(self, job_id: str):
        return self.job_status_to_return


def test_submit_job_success(monkeypatch):
    orchestrator = FakeOrchestrator()

    # Patch the factory to return our fake orchestrator
    monkeypatch.setattr(
        "lif.orchestrator_service.service.OrchestratorFactory.create",
        lambda orchestrator_type, cfg: orchestrator,
        raising=False,
    )

    service = OrchestratorService(config={})

    part = LIFQueryPlanPart(
        information_source_id="test_source",
        adapter_id="lif-to-lif",
        person_id=LIFPersonIdentifier(identifier="123", identifierType="pid"),
        lif_fragment_paths=["person.name", "person.age"],
        translation=None,
    )
    plan = LIFQueryPlan(root=[part])

    run_id = asyncio.run(service.submit_job(plan))

    assert run_id == orchestrator.post_job_return
    assert orchestrator.received_job_definition is not None
    assert orchestrator.received_job_definition.lif_query_plan[0].adapter_id == "lif-to-lif"
    assert orchestrator.received_job_definition.lif_query_plan[0].person_id.identifier == "123"
    assert orchestrator.received_job_definition.lif_query_plan[0].lif_fragment_paths == ["person.name", "person.age"]


def test_submit_job_propagates_exception(monkeypatch):
    orchestrator = FakeOrchestrator()
    orchestrator.post_job_exception = RuntimeError("boom")

    monkeypatch.setattr(
        "lif.orchestrator_service.service.OrchestratorFactory.create",
        lambda orchestrator_type, cfg: orchestrator,
        raising=False,
    )

    service = OrchestratorService(config={})

    part = LIFQueryPlanPart(
        information_source_id="test_source",
        adapter_id="lif-to-lif",
        person_id=LIFPersonIdentifier(identifier="123", identifierType="pid"),
        lif_fragment_paths=["person.name"],
        translation=None,
    )
    plan = LIFQueryPlan(root=[part])

    with pytest.raises(RuntimeError):
        asyncio.run(service.submit_job(plan))


def test_get_job_status_success(monkeypatch):
    orchestrator = FakeOrchestrator()
    orchestrator.job_status_to_return = OrchestratorJob(job_id="abc", status=OrchestratorJobStatus.COMPLETED)

    monkeypatch.setattr(
        "lif.orchestrator_service.service.OrchestratorFactory.create",
        lambda orchestrator_type, cfg: orchestrator,
        raising=False,
    )

    service = OrchestratorService(config={})

    job = asyncio.run(service.get_job_status("abc"))
    assert job.job_id == "abc"
    assert job.status == OrchestratorJobStatus.COMPLETED


def test_get_job_status_propagates_exception(monkeypatch):
    orchestrator = FakeOrchestrator()

    async def raise_exc(job_id: str):
        raise RuntimeError("status failed")

    monkeypatch.setattr(orchestrator, "get_job_status", raise_exc, raising=False)

    monkeypatch.setattr(
        "lif.orchestrator_service.service.OrchestratorFactory.create",
        lambda orchestrator_type, cfg: orchestrator,
        raising=False,
    )

    service = OrchestratorService(config={})

    with pytest.raises(RuntimeError):
        asyncio.run(service.get_job_status("abc"))
