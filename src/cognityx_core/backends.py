"""Abstract backend contracts shared by Cognityx implementations."""

from abc import ABC, abstractmethod

from cognityx_core.models import (
    DeploymentRequest,
    DeploymentResult,
    EvaluationRequest,
    EvaluationResult,
    InferenceRequest,
    InferenceResult,
    TrainingRequest,
    TrainingResult,
)


class TrainingBackend(ABC):
    """Train model artifacts from configuration-independent requests."""

    @abstractmethod
    def train(self, request: TrainingRequest) -> TrainingResult:
        """Run training and return the resulting artifact and metrics."""


class EvaluatorBackend(ABC):
    """Evaluate model artifacts against datasets."""

    @abstractmethod
    def evaluate(self, request: EvaluationRequest) -> EvaluationResult:
        """Run an evaluation and return its measurements."""


class InferenceBackend(ABC):
    """Serve synchronous inference requests."""

    @abstractmethod
    def infer(self, request: InferenceRequest) -> InferenceResult:
        """Run one inference request."""


class DeploymentBackend(ABC):
    """Create and remove model-serving deployments."""

    @abstractmethod
    def deploy(self, request: DeploymentRequest) -> DeploymentResult:
        """Create a deployment."""

    @abstractmethod
    def undeploy(self, deployment_id: str) -> None:
        """Remove an existing deployment."""
