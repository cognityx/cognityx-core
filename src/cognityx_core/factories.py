"""Configuration-driven backend construction."""

from collections.abc import Callable
from typing import Generic, TypeVar

from cognityx_core.configuration import BackendConfig

BackendT = TypeVar("BackendT")


class BackendFactory(Generic[BackendT]):
    """Map stable backend names to package-owned constructors."""

    def __init__(self) -> None:
        self._builders: dict[str, Callable[[BackendConfig], BackendT]] = {}

    def register(
        self,
        name: str,
        builder: Callable[[BackendConfig], BackendT],
    ) -> None:
        """Register a constructor under a normalized backend name."""
        normalized = name.strip().casefold()
        if not normalized:
            raise ValueError("Backend name must not be empty.")
        if normalized in self._builders:
            raise ValueError(f"Backend already registered: {name}")
        self._builders[normalized] = builder

    def create(self, config: BackendConfig) -> BackendT:
        """Create the backend selected by configuration.

        Raises:
            KeyError: If no constructor is registered for the selected backend.
        """
        name = config.backend.strip().casefold()
        try:
            builder = self._builders[name]
        except KeyError as exc:
            available = ", ".join(sorted(self._builders)) or "none"
            raise KeyError(
                f"Unknown backend '{config.backend}'. Registered backends: {available}"
            ) from exc
        return builder(config)

    @property
    def registered_backends(self) -> tuple[str, ...]:
        """Return registered names in stable sorted order."""
        return tuple(sorted(self._builders))
