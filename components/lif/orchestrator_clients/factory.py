"""Factory and registry for orchestrator client implementations.

This module provides:
    * A lightweight exception (`OrchestratorNotFoundError`) for unknown orchestrator types.
    * A simple, non-thread-safe registry (`OrchestratorFactory`) used at application startup
        to construct concrete `OrchestratorClient` implementations (e.g. Dagster, Airflow).

Design notes:
    * Intentional lack of locking for simplicity--safe because registration happens during
        process initialization, not concurrently.
    * Returning a defensive copy in `list()` prevents accidental mutation of internal state.
    * `register()` supports optional overrides for replacing built-ins (useful in tests or
        feature flags).
"""

from typing import Dict, Any, Type, TypeVar
import logging

from lif.orchestrator_service.core import OrchestratorClient
from .dagster import DagsterClient  # built-in implementations

logger = logging.getLogger(__name__)

TClient = TypeVar("TClient", bound=OrchestratorClient)


class OrchestratorNotFoundError(LookupError):
    """Raised when a requested orchestrator type is not registered.

    Attributes:
        orchestrator_type: The unknown key requested.
        available: Current mapping of registered orchestrators (for diagnostics/UI).
    """

    def __init__(self, orchestrator_type: str, available: Dict[str, Type[OrchestratorClient]]):
        msg = (
            f"Unsupported orchestrator type '{orchestrator_type}'. Available: {', '.join(available.keys()) or '(none)'}"
        )
        super().__init__(msg)
        self.orchestrator_type = orchestrator_type
        self.available = available


class OrchestratorFactory:
    """Simple registry + factory for orchestrator clients.

    Responsibilities:
        * Maintain a mapping from orchestrator type string -> concrete client class.
        * Instantiate a client via `create()` given a type and config dict.
        * Allow external registration of additional types (plugins, tests, overrides).

    This is intentionally minimal; if dynamic / concurrent mutation is ever required,
    consider introducing locking or an injectable registry instance.
    """

    _registry: Dict[str, Type[OrchestratorClient]] = {
        "dagster": DagsterClient
        # "airflow": AirflowClient,
    }

    @classmethod
    def list(cls) -> Dict[str, Type[OrchestratorClient]]:
        """Return a defensive copy of the registered orchestrator mapping."""
        return dict(cls._registry)

    @classmethod
    def create(cls, orchestrator_type: str, config: Dict[str, Any]) -> OrchestratorClient:
        """Instantiate an orchestrator client of the requested type.

        Args:
            orchestrator_type: Registry key identifying the implementation.
            config: Arbitrary configuration dict passed to the client constructor.

        Raises:
            OrchestratorNotFoundError: If the type is not registered.

        Returns:
            A concrete `OrchestratorClient` implementation instance.
        """
        try:
            impl = cls._registry[orchestrator_type]
        except KeyError:
            raise OrchestratorNotFoundError(orchestrator_type, cls._registry)
        client = impl(config)
        logger.debug("Created orchestrator '%s' instance: %s", orchestrator_type, impl.__name__)
        return client

    @classmethod
    def register(cls, name: str, impl: Type[TClient], *, override: bool = False) -> None:
        """Register a new orchestrator implementation.

        Args:
            name: Registry key to associate with the client class.
            impl: Concrete class inheriting from `OrchestratorClient`.
            override: When True, replace any existing registration for this name.

        Raises:
            TypeError: If the provided class does not subclass `OrchestratorClient`.
            ValueError: If the name already exists and `override` is False.
        """
        if not issubclass(impl, OrchestratorClient):
            raise TypeError(f"{impl} must subclass OrchestratorClient")
        if not override and name in cls._registry:
            raise ValueError(f"Orchestrator '{name}' already registered (use override=True)")
        cls._registry[name] = impl
        logger.info("Registered orchestrator '%s' -> %s", name, impl.__name__)
