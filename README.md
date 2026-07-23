# cognityx-core

Shared, dependency-light Python interfaces for Cognityx AI systems.

## Included contracts

- training and evaluation
- synchronous inference
- deployment lifecycle
- dataset providers
- artifact registries
- immutable request, result, dataset, and artifact value objects

Concrete framework and infrastructure integrations belong in adapter packages.

## Development

```bash
uv sync --dev
uv run pytest
uv run mkdocs build --strict
uv run mkdocs serve
```

## Example

```python
from cognityx_core import Artifact, ArtifactRegistry


def publish(registry: ArtifactRegistry) -> Artifact:
    return registry.register(
        Artifact("classifier", "1.0.0", "s3://models/classifier/1.0.0")
    )
```
