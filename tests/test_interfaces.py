"""Contract-level tests that require no ML frameworks or services."""

from cognityx_core import (
    Artifact,
    ArtifactRegistry,
    BackendConfig,
    BackendFactory,
    Dataset,
    InferenceEngine,
    InferenceRequest,
    InferenceResult,
    TrainingRequest,
    TrainingBackend,
    AdapterUsage,
    GPUUsage,
    ParameterCounts,
    ResponseTime,
    SystemUsage,
    TrainingReport,
    write_training_report,
)


class MemoryRegistry:
    """Minimal structural implementation used to test the registry protocol."""

    def __init__(self) -> None:
        self.artifacts: dict[tuple[str, str], Artifact] = {}

    def register(self, artifact: Artifact) -> Artifact:
        self.artifacts[(artifact.name, artifact.version)] = artifact
        return artifact

    def get(self, name: str, version: str | None = None) -> Artifact:
        matches = [item for (item_name, _), item in self.artifacts.items() if item_name == name]
        if version is not None:
            return self.artifacts[(name, version)]
        return matches[-1]

    def list(self) -> tuple[Artifact, ...]:
        return tuple(self.artifacts.values())


class EchoEngine:
    """Minimal structural inference implementation."""

    def infer(self, request: InferenceRequest) -> InferenceResult:
        return InferenceResult(outputs=request.inputs)


def test_value_objects_are_immutable() -> None:
    dataset = Dataset("sample", "1", "memory://sample")
    request = TrainingRequest(dataset)

    assert request.dataset == dataset


def test_registry_protocol_accepts_structural_implementation() -> None:
    registry = MemoryRegistry()
    artifact = Artifact("model", "1", "memory://model")

    assert isinstance(registry, ArtifactRegistry)
    assert registry.register(artifact) == artifact
    assert registry.get("model") == artifact


def test_inference_protocol_accepts_structural_implementation() -> None:
    engine = EchoEngine()

    assert isinstance(engine, InferenceEngine)
    assert engine.infer(InferenceRequest({"text": "hello"})).outputs == {"text": "hello"}


class TestTrainingBackend(TrainingBackend):
    """Small concrete backend used to verify ABC and factory behavior."""

    def train(self, request: TrainingRequest):
        raise NotImplementedError


def test_configuration_driven_factory() -> None:
    factory: BackendFactory[TrainingBackend] = BackendFactory()
    factory.register("custom-pytorch", lambda _config: TestTrainingBackend())

    backend = factory.create(BackendConfig("custom-pytorch"))

    assert isinstance(backend, TrainingBackend)
    assert factory.registered_backends == ("custom-pytorch",)


def test_training_request_has_a_default_output_directory() -> None:
    request = TrainingRequest(Dataset("sample", "1", "memory://sample"))

    assert request.output_dir == "outputs/training"


def test_training_report_is_written_to_its_run_directory(tmp_path) -> None:
    report = TrainingReport(
        run_id="run-001",
        status="completed",
        started_at="2026-07-23T10:00:00+00:00",
        finished_at="2026-07-23T10:02:30+00:00",
        training_type="lora",
        model=Artifact("base-model", "1", "hf://base-model"),
        dataset=Dataset("sample", "2", "s3://datasets/sample"),
        configuration={"epochs": 3, "batch_size": 8},
        parameter_counts=ParameterCounts(
            original_total=1_000,
            original_trainable=1_000,
            final_total=1_100,
            final_trainable=100,
        ),
        gpu_usage=(
            GPUUsage(
                device="NVIDIA Test GPU",
                device_index=0,
                sample_count=10,
                utilization_average_percent=72.5,
                utilization_peak_percent=96.0,
                memory_peak_bytes=8_000_000,
            ),
        ),
        system_usage=SystemUsage(
            sample_count=10,
            cpu_average_percent=45.5,
            cpu_peak_percent=91.0,
            ram_peak_bytes=16_000_000,
            disk_read_bytes=20_000_000,
            disk_write_bytes=4_000_000,
        ),
        response_times=(
            ResponseTime(
                operation="training_step",
                sample_count=10,
                average_ms=120.0,
                median_ms=118.0,
                p95_ms=140.0,
                maximum_ms=145.0,
            ),
        ),
        adapter_usage=AdapterUsage(
            adapter_type="lora",
            parameter_count=100,
            gpu_resident_peak_bytes=2_000_000,
            serialized_size_bytes=500_000,
            saved_uri="file:///models/run-001/adapter",
        ),
        metrics={"train_loss": 0.25},
    )

    report_path = write_training_report(report, tmp_path)
    contents = report_path.read_text(encoding="utf-8")

    assert report_path == tmp_path / "run-001" / "training-report.json"
    assert '"duration_seconds": 150.0' in contents
    assert '"original_total": 1000' in contents
    assert '"utilization_peak_percent": 96.0' in contents
    assert '"cpu_peak_percent": 91.0' in contents
    assert '"disk_write_bytes": 4000000' in contents
    assert '"p95_ms": 140.0' in contents
    assert '"gpu_resident_peak_bytes": 2000000' in contents
    assert '"serialized_size_bytes": 500000' in contents
