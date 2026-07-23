"""Training contracts implemented by framework-specific adapters."""

from typing import Protocol, runtime_checkable

from cognityx_core.models import TrainingRequest, TrainingResult


@runtime_checkable
class Trainer(Protocol):
    """Train a model or other learned artifact."""

    def train(self, request: TrainingRequest) -> TrainingResult:
        """Execute a training request.

        Args:
            request: Framework-independent training inputs.

        Returns:
            The registered or registerable trained artifact and metrics.

        Raises:
            Exception: Implementations document backend-specific failures.
        """
        ...
