# Cognityx Core

`cognityx-core` defines dependency-light contracts shared by Cognityx training,
evaluation, inference, deployment, dataset, and artifact-registry components.

The package intentionally contains interfaces and value objects—not concrete ML,
cloud, database, or serving implementations. Implementations can therefore use
their preferred frameworks while remaining interoperable at package boundaries.

- [Architecture](architecture.md)
- [Interface guide](interfaces.md)
- [Generated API reference](api.md)
