# Architecture

The immutable value objects form the common vocabulary. Runtime-specific
components structurally implement the public protocols.

```mermaid
flowchart LR
    Client --> Trainer
    Client --> Evaluator
    Client --> InferenceEngine
    Client --> Deployer
    Trainer --> DatasetProvider
    Trainer --> ArtifactRegistry
    Evaluator --> DatasetProvider
    Evaluator --> ArtifactRegistry
    InferenceEngine --> ArtifactRegistry
    Deployer --> ArtifactRegistry
    Models[Shared value objects] --> Trainer
    Models --> Evaluator
    Models --> InferenceEngine
    Models --> Deployer
```

Protocols use structural typing, so adapters do not need to inherit from a base
class. `runtime_checkable` supports lightweight integration checks, while static
type checkers validate complete method signatures.
