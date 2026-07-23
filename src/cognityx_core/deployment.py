"""Deployment lifecycle contracts for infrastructure adapters."""

from typing import Protocol, runtime_checkable

from cognityx_core.models import DeploymentRequest, DeploymentResult


@runtime_checkable
class Deployer(Protocol):
    """Create and remove deployments for versioned artifacts."""

    def deploy(self, request: DeploymentRequest) -> DeploymentResult:
        """Create a deployment and return its identity and endpoint."""
        ...

    def undeploy(self, deployment_id: str) -> None:
        """Remove a deployment.

        Args:
            deployment_id: Provider-specific deployment identifier.
        """
        ...
