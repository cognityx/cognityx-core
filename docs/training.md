# Training and reports

## Can I run training from this package?

Not by itself. `cognityx-core` is a dependency-free contract package. It does
not contain a model framework, a concrete trainer, or a `cognityx train`
command. A PyTorch, Transformers, or other adapter package must implement
`TrainingBackend` and register it with `BackendFactory`.

Once an adapter is installed and registered, application code starts a run
through the common API:

```python
from cognityx_core import BackendConfig, BackendFactory, Dataset, TrainingRequest

# The adapter package creates and registers this factory.
factory = BackendFactory()
factory.register("my-trainer", create_my_training_backend)
trainer = factory.create(BackendConfig("my-trainer"))

result = trainer.train(
    TrainingRequest(
        dataset=Dataset(
            name="instruction-data",
            version="1",
            uri="file:///data/instruction-data.jsonl",
        ),
        base_artifact=my_base_model,
        parameters={
            "training_type": "lora",
            "epochs": 3,
            "batch_size": 8,
            "learning_rate": 2e-4,
        },
        output_dir="outputs/training",
    )
)

print(result.artifact.uri)
print(result.report_uri)
```

`create_my_training_backend` and `my_base_model` in this example are supplied
by the adapter/application. They are intentionally not defined by
`cognityx-core`.

## Output layout

Each backend should place one run under its own identifier:

```text
outputs/training/
└── <run-id>/
    ├── training-report.json
    └── <model or adapter files>
```

The adapter builds a `TrainingReport` and calls:

```python
report_path = write_training_report(report, request.output_dir)
```

The JSON report supports:

- model, dataset, run status, timestamps, duration, and training configuration;
- original and final total/trainable parameter counts;
- GPU utilization, memory, and optional energy consumption;
- CPU utilization, main RAM, and disk reads/writes;
- response-time distributions for named operations such as `training_step`;
- LoRA adapter parameter count, GPU-resident size, serialized disk size, and
  saved URI;
- training metrics, environment metadata, and failure details.

The concrete backend is responsible for sampling these measurements because
the necessary APIs differ among CUDA, ROCm, operating systems, and training
frameworks.

## Commands currently available

There is no training CLI in this package yet. The repository provides these
development and documentation commands:

| Command | Purpose |
| --- | --- |
| `uv sync --dev` | Install the package and development dependencies. |
| `uv run pytest` | Run contract tests. |
| `uv run pytest --help` | Show pytest command help. |
| `uv run mkdocs serve` | Preview documentation at `http://127.0.0.1:8124/`. |
| `uv run mkdocs build --strict` | Build and validate documentation. |
| `uv run mkdocs --help` | Show documentation command help. |
| `uv build` | Build the source archive and wheel. |
| `uv build --help` | Show package-build help. |

The eventual user-facing training command belongs in the concrete training
package, where model, dataset, CUDA, and LoRA options can be validated.
