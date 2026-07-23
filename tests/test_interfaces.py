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
