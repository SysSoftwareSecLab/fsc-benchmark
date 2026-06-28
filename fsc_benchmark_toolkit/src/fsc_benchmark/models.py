"""Data models for the FSC benchmark toolkit.

The toolkit intentionally uses the Python standard library only.  These
classes provide a lightweight, explicit schema for generation-level records.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Iterable, List, Optional


class Ecosystem(str, Enum):
    """Task ecosystems proposed by the FSC framework."""

    GENERAL_PURPOSE = "general_purpose"
    DEPLOYMENT_CONTEXT = "deployment_context"
    SECURITY_EXPLICIT = "security_explicit"


class Classification(str, Enum):
    """Sample-level classification used by this toolkit."""

    SECURE_FUNCTIONAL = "secure_functional"
    FSC = "false_security_confidence"
    FSC_HARD = "fsc_hard"
    FUNCTIONAL_FAILURE = "functional_failure"
    SECURITY_FAILURE_WITHOUT_FUNCTIONAL_SUCCESS = "security_failure_without_functional_success"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class GenerationRecord:
    """One generated code sample and its validation outcomes.

    Required indicators:
      - functional_correct: whether the task oracle passes.
      - security_successful: whether the security validation stack passes.

    Optional FSC-hard indicators:
      - static_flagged: whether static tooling flagged the vulnerability.
      - dynamic_evidence: whether dynamic validation confirms a reachable failure.
      - semantic_evidence: whether semantic/oracle evidence confirms a failure.
    """

    sample_id: str
    model: str
    task_id: str
    ecosystem: Ecosystem
    language: str
    functional_correct: bool
    security_successful: bool
    prompt_id: Optional[str] = None
    static_flagged: Optional[bool] = None
    dynamic_evidence: bool = False
    semantic_evidence: bool = False
    analyzer_notes: List[str] = field(default_factory=list)
    security_categories: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def from_dict(obj: Dict[str, Any]) -> "GenerationRecord":
        required = [
            "sample_id",
            "model",
            "task_id",
            "ecosystem",
            "language",
            "functional_correct",
            "security_successful",
        ]
        missing = [key for key in required if key not in obj]
        if missing:
            raise ValueError(f"Missing required field(s): {', '.join(missing)}")

        try:
            ecosystem = Ecosystem(obj["ecosystem"])
        except ValueError as exc:
            valid = ", ".join(e.value for e in Ecosystem)
            raise ValueError(f"Invalid ecosystem {obj.get('ecosystem')!r}; expected one of: {valid}") from exc

        return GenerationRecord(
            sample_id=str(obj["sample_id"]),
            model=str(obj["model"]),
            task_id=str(obj["task_id"]),
            ecosystem=ecosystem,
            language=str(obj["language"]),
            functional_correct=_coerce_bool(obj["functional_correct"], "functional_correct"),
            security_successful=_coerce_bool(obj["security_successful"], "security_successful"),
            prompt_id=str(obj["prompt_id"]) if obj.get("prompt_id") is not None else None,
            static_flagged=_coerce_optional_bool(obj.get("static_flagged"), "static_flagged"),
            dynamic_evidence=_coerce_bool(obj.get("dynamic_evidence", False), "dynamic_evidence"),
            semantic_evidence=_coerce_bool(obj.get("semantic_evidence", False), "semantic_evidence"),
            analyzer_notes=_coerce_list(obj.get("analyzer_notes", []), "analyzer_notes"),
            security_categories=_coerce_list(obj.get("security_categories", []), "security_categories"),
            metadata=dict(obj.get("metadata", {})),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sample_id": self.sample_id,
            "model": self.model,
            "task_id": self.task_id,
            "ecosystem": self.ecosystem.value,
            "language": self.language,
            "functional_correct": self.functional_correct,
            "security_successful": self.security_successful,
            "prompt_id": self.prompt_id,
            "static_flagged": self.static_flagged,
            "dynamic_evidence": self.dynamic_evidence,
            "semantic_evidence": self.semantic_evidence,
            "analyzer_notes": list(self.analyzer_notes),
            "security_categories": list(self.security_categories),
            "metadata": dict(self.metadata),
        }


def _coerce_bool(value: Any, field_name: str) -> bool:
    if isinstance(value, bool):
        return value
    raise ValueError(f"Field {field_name!r} must be a boolean, got {type(value).__name__}")


def _coerce_optional_bool(value: Any, field_name: str) -> Optional[bool]:
    if value is None:
        return None
    return _coerce_bool(value, field_name)


def _coerce_list(value: Any, field_name: str) -> List[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError(f"Field {field_name!r} must be a list")
    return [str(item) for item in value]
