"""Portable JSON reporting for training runs."""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from cognityx_core.models import Artifact, Dataset, Metadata


@dataclass(frozen=True, slots=True)
class ParameterCounts:
    """Model parameter counts observed before and after training."""

    original_total: int
    original_trainable: int
    final_total: int
    final_trainable: int


@dataclass(frozen=True, slots=True)
class GPUUsage:
    """Aggregated utilization and memory measurements for one GPU."""

    device: str
    device_index: int | None = None
    sample_count: int = 0
    utilization_average_percent: float | None = None
    utilization_peak_percent: float | None = None
    memory_average_bytes: int | None = None
    memory_peak_bytes: int | None = None
    energy_consumed_joules: float | None = None


@dataclass(frozen=True, slots=True)
class SystemUsage:
    """Aggregated CPU, main-memory, and disk-I/O measurements."""

    sample_count: int = 0
    cpu_average_percent: float | None = None
    cpu_peak_percent: float | None = None
    ram_average_bytes: int | None = None
    ram_peak_bytes: int | None = None
    disk_read_bytes: int | None = None
    disk_write_bytes: int | None = None
    disk_read_operations: int | None = None
    disk_write_operations: int | None = None


@dataclass(frozen=True, slots=True)
class ResponseTime:
    """Latency distribution for measured training operations."""

    operation: str
    sample_count: int
    average_ms: float | None = None
    minimum_ms: float | None = None
    median_ms: float | None = None
    p95_ms: float | None = None
    p99_ms: float | None = None
    maximum_ms: float | None = None


@dataclass(frozen=True, slots=True)
class AdapterUsage:
    """LoRA or other parameter-efficient adapter size measurements."""

    adapter_type: str
    parameter_count: int | None = None
    gpu_resident_bytes: int | None = None
    gpu_resident_peak_bytes: int | None = None
    serialized_size_bytes: int | None = None
    saved_uri: str | None = None


@dataclass(frozen=True, slots=True)
class TrainingReport:
    """Serializable measurements and provenance for one training run."""

    run_id: str
    status: str
    started_at: str
    finished_at: str
    training_type: str
    model: Artifact
    dataset: Dataset
    configuration: Metadata = field(default_factory=dict)
    parameter_counts: ParameterCounts | None = None
    gpu_usage: tuple[GPUUsage, ...] = ()
    system_usage: SystemUsage | None = None
    response_times: tuple[ResponseTime, ...] = ()
    adapter_usage: AdapterUsage | None = None
    metrics: Metadata = field(default_factory=dict)
    environment: Metadata = field(default_factory=dict)
    error: str | None = None

    @property
    def duration_seconds(self) -> float:
        """Return elapsed wall-clock time represented by the report."""
        started = datetime.fromisoformat(self.started_at)
        finished = datetime.fromisoformat(self.finished_at)
        return (finished - started).total_seconds()

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible representation."""
        value = asdict(self)
        value["duration_seconds"] = self.duration_seconds
        return value


def utc_now() -> str:
    """Return an ISO 8601 UTC timestamp suitable for reports."""
    return datetime.now(timezone.utc).isoformat()


def write_training_report(
    report: TrainingReport,
    output_dir: str | os.PathLike[str],
) -> Path:
    """Atomically write ``<output_dir>/<run_id>/training-report.json``.

    The per-run directory keeps model outputs and their report together.
    Existing reports are replaced atomically, which also allows a backend to
    persist an initial failure report and later retry the same run identifier.
    """
    run_dir = Path(output_dir) / report.run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    report_path = run_dir / "training-report.json"
    temporary_path = run_dir / ".training-report.json.tmp"
    temporary_path.write_text(
        json.dumps(report.to_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary_path.replace(report_path)
    return report_path
