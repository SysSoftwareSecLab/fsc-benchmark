"""FSC Benchmark Toolkit."""

from .models import Ecosystem, GenerationRecord, Classification
from .metrics import (
    is_fsc,
    is_fsc_hard,
    compute_metrics,
    group_metrics,
)

__version__ = "0.1.0"

__all__ = [
    "Ecosystem",
    "GenerationRecord",
    "Classification",
    "is_fsc",
    "is_fsc_hard",
    "compute_metrics",
    "group_metrics",
]
