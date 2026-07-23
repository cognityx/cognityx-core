"""Dependency-free value objects shared by all core interfaces."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

Metadata = Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class Artifact:
    """Identify a versioned artifact stored by an artifact registry."""

    name: str
    version: str
    uri: str
    metadata: Metadata = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Dataset:
    """Identify a versioned dataset supplied by a dataset provider."""

    name: str
    version: str
    uri: str
    metadata: Metadata = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class TrainingRequest:
    """Describe a training job independently of a training framework."""

    dataset: Dataset
    parameters: Metadata = field(default_factory=dict)
    base_artifact: Artifact | None = None
    output_dir: str = "outputs/training"


@dataclass(frozen=True, slots=True)
class TrainingResult:
    """Describe the output and metrics of a completed training job."""

    artifact: Artifact
    metrics: Metadata = field(default_factory=dict)
    report_uri: str | None = None


@dataclass(frozen=True, slots=True)
class EvaluationRequest:
    """Describe an artifact evaluation against a dataset."""

    artifact: Artifact
    dataset: Dataset
    parameters: Metadata = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    """Contain evaluation measurements and optional detailed outputs."""

    metrics: Metadata
    outputs: Metadata = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class InferenceRequest:
    """Contain one inference payload and backend-independent parameters."""

    inputs: Metadata
    parameters: Metadata = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class InferenceResult:
    """Contain one inference response and associated metadata."""

    outputs: Metadata
    metadata: Metadata = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class DeploymentRequest:
    """Describe how an artifact should be deployed."""

    artifact: Artifact
    target: str
    parameters: Metadata = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class DeploymentResult:
    """Identify a created deployment and its externally usable endpoint."""

    deployment_id: str
    endpoint: str
    metadata: Metadata = field(default_factory=dict)
