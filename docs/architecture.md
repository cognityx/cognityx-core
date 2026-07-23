# Architecture

The immutable value objects form the common vocabulary. Runtime-specific
components structurally implement the public protocols.

```mermaid
flowchart LR
    Client --> BackendFactory
    BackendFactory --> TrainingBackend
    BackendFactory --> EvaluatorBackend
    BackendFactory --> InferenceBackend
    BackendFactory --> DeploymentBackend
    TrainingBackend --> DatasetProvider
    TrainingBackend --> ModelArtifactRegistry
    EvaluatorBackend --> DatasetProvider
    EvaluatorBackend --> ModelArtifactRegistry
    InferenceBackend --> ModelArtifactRegistry
    DeploymentBackend --> ModelArtifactRegistry
    Models[Shared value objects] --> TrainingBackend
    Models --> EvaluatorBackend
    Models --> InferenceBackend
    Models --> DeploymentBackend
```

Protocols use structural typing, so adapters do not need to inherit from a base
class. `runtime_checkable` supports lightweight integration checks, while static
type checkers validate complete method signatures.
