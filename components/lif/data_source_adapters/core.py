from abc import ABC, abstractmethod
from enum import Enum
from typing import ClassVar

from lif.datatypes import OrchestratorJobQueryPlanPartResults
from lif.logging import get_logger

logger = get_logger(__name__)


class LIFAdapterType(Enum):
    """Enumeration of LIF adapter types."""

    LIF_TO_LIF = "LIF_TO_LIF"
    STANDALONE = "STANDALONE"
    PIPELINE_INTEGRATED = "PIPELINE_INTEGRATED"
    AI_WRITE = "AI_WRITE"


class LIFDataSourceAdapter(ABC):
    """Abstract base class for data source adapters.

    Class Variables:
        adapter_id (str): Unique identifier for the adapter. This string
            will be used in configurations to reference this adapter.
        adapter_type (LIFAdapterType): Type of the adapter.
        credential_keys: List of credential keys this adapter expects
            (e.g., ["host", "token"]). All credentials are optional unless
            the adapter's __init__ method validates otherwise.
    """

    adapter_id: ClassVar[str]
    adapter_type: ClassVar[LIFAdapterType]
    credential_keys: ClassVar[list[str]] = []  # Default to empty list

    def __init_subclass__(cls):
        super().__init_subclass__()
        if not hasattr(cls, "adapter_id"):
            raise NotImplementedError("Subclasses must define 'adapter_id' as a class variable.")
        if not hasattr(cls, "adapter_type"):
            raise NotImplementedError("Subclasses must define 'adapter_type' as a class variable.")
        # credential_keys is optional - some adapters might not need credentials

    @classmethod
    def validate_credentials(cls, credentials: dict) -> None:
        """Basic validation - subclasses can override for custom logic."""
        # For now, just check that provided credentials are recognized
        unrecognized = set(credentials.keys()) - set(cls.credential_keys)
        if unrecognized:
            logger.warning(f"Unrecognized credentials for {cls.__name__}: {unrecognized}")

    @abstractmethod
    def run(self) -> OrchestratorJobQueryPlanPartResults | dict:
        """Run the adapter logic."""
        pass
