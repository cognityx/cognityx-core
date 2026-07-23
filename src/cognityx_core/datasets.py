"""Dataset discovery contracts for storage and catalog adapters."""

from typing import Protocol, runtime_checkable

from cognityx_core.models import Dataset


@runtime_checkable
class DatasetProvider(Protocol):
    """Resolve and enumerate versioned datasets."""

    def get(self, name: str, version: str | None = None) -> Dataset:
        """Resolve a dataset, optionally selecting a specific version."""
        ...

    def list(self) -> tuple[Dataset, ...]:
        """Return datasets visible through this provider."""
        ...
