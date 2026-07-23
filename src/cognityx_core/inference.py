"""Synchronous inference contracts for serving adapters."""

from typing import Protocol, runtime_checkable

from cognityx_core.models import InferenceRequest, InferenceResult


@runtime_checkable
class InferenceEngine(Protocol):
    """Perform synchronous inference without prescribing a runtime."""

    def infer(self, request: InferenceRequest) -> InferenceResult:
        """Run one inference request and return its outputs."""
        ...
