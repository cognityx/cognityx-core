"""Evaluation contracts implemented by task-specific evaluators."""

from typing import Protocol, runtime_checkable

from cognityx_core.models import EvaluationRequest, EvaluationResult


@runtime_checkable
class Evaluator(Protocol):
    """Evaluate an artifact using a declared dataset and parameters."""

    def evaluate(self, request: EvaluationRequest) -> EvaluationResult:
        """Run an evaluation and return measurements."""
        ...
