# Interface guide

| Area | Protocol | Responsibility |
| --- | --- | --- |
| Training | `Trainer` | Produce a versioned artifact from a dataset and parameters. |
| Evaluation | `Evaluator` | Measure an artifact against a dataset. |
| Inference | `InferenceEngine` | Execute a synchronous inference request. |
| Deployment | `Deployer` | Create and remove serving deployments. |
| Datasets | `DatasetProvider` | Resolve and enumerate versioned datasets. |
| Artifacts | `ArtifactRegistry` | Publish, resolve and enumerate artifacts. |

Requests and results are frozen, slotted dataclasses. Their `metadata` and
`parameters` mappings are extension points for provider-specific values while
the top-level lifecycle remains stable.

Concrete packages should document backend exceptions, authentication, retry
behavior, and side effects.
