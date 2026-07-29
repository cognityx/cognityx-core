# cognityx-core

Shared, dependency-light Python interfaces for Cognityx AI systems.

## Included contracts

- training and evaluation
- synchronous inference
- deployment lifecycle
- dataset providers
- artifact registries
- immutable request, result, dataset, and artifact value objects
- per-run JSON training reports with configuration, parameter, GPU, CPU, RAM,
  disk-I/O, and response-time metrics

Concrete framework and infrastructure integrations belong in adapter packages.
This package does not currently provide a training CLI or concrete trainer.
See the
[training and reporting guide](docs/training.md)
for the backend call pattern, output layout, measurements, and available
development commands.

Training requests default to `outputs/training`. Backends should keep each
run's artifacts under `<output_dir>/<run_id>/` and write
`training-report.json` there with `write_training_report`. GPU measurements are
sampled by the framework adapter and represented using `GPUUsage`. Host
resource samples use `SystemUsage`, operation latency distributions use
`ResponseTime`, and LoRA adapter reports use `AdapterUsage` to distinguish
in-GPU size from serialized size and saved location on disk.

## Development

```bash
uv sync --dev
uv run pytest
uv run mkdocs build --strict
uv run mkdocs serve
```

The documentation preview uses <http://127.0.0.1:8124/> so it can run beside
the `cognityx-inference` documentation server.

## Example

```python
from cognityx_core import Artifact, ArtifactRegistry


def publish(registry: ArtifactRegistry) -> Artifact:
    return registry.register(
        Artifact("classifier", "1.0.0", "s3://models/classifier/1.0.0")
    )
```
