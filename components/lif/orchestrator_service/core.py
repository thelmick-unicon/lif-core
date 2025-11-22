from abc import ABC, abstractmethod
from typing import Any

from lif.datatypes import OrchestratorJobDefinition, OrchestratorJob


class OrchestratorClient(ABC):
    """Abstract base class for all orchestrator implementations"""

    def __init__(self, config: dict[str, Any] | None = None):
        self._raw_config = config or {}

    @abstractmethod
    async def post_job(self, job_definition: OrchestratorJobDefinition) -> str:
        """Submit a job and return job ID"""
        pass

    @abstractmethod
    async def get_job_status(self, job_id: str) -> OrchestratorJob:
        """Get current status of a job"""
        pass

    # @abstractmethod
    # async def cancel_job(self, job_id: str) -> bool:
    #     """Cancel a running job"""
    #     pass

    # @abstractmethod
    # def set_result_queue(self, queue: "QueueInterface") -> None:
    #     """Set the result queue for job results"""
    #     pass
