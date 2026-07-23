"""Artifact registry contracts for model and asset storage adapters."""

from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable

from cognityx_core.models import Artifact


@runtime_checkable
class ArtifactRegistry(Protocol):
    """Publish, resolve, and enumerate versioned artifacts."""

    def register(self, artifact: Artifact) -> Artifact:
        """Publish an artifact and return its canonical registry identity."""
        ...

    def get(self, name: str, version: str | None = None) -> Artifact:
        """Resolve an artifact, optionally selecting a specific version."""
        ...

    def list(self) -> tuple[Artifact, ...]:
        """Return artifacts visible through this registry."""
        ...


class ModelArtifactRegistry(ABC):
    """Abstract registry for publishing and resolving trained model artifacts."""

    @abstractmethod
    def register(self, artifact: Artifact) -> Artifact:
        """Publish an artifact and return its canonical identity."""

    @abstractmethod
    def get(self, name: str, version: str | None = None) -> Artifact:
        """Resolve an artifact, optionally selecting a version."""

    @abstractmethod
    def list(self) -> tuple[Artifact, ...]:
        """Return all visible model artifacts."""
