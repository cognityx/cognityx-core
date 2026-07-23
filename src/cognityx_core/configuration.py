"""Backend-neutral configuration value objects."""

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class BackendConfig:
    """Select a backend and carry portable orchestration metadata.

    Backend packages should subclass this type for their own strongly typed
    options instead of placing framework-specific fields in the core package.
    """

    backend: str
    metadata: Mapping[str, Any] = field(default_factory=dict)
