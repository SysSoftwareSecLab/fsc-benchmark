"""Markdown and JSON-friendly reporting helpers."""

from __future__ import annotations

from typing import Dict, Iterable, List, Sequence

from .metrics import MetricSummary, classify, compute_metrics, group_metrics, is_fsc, is_fsc_hard
from .models import GenerationRecord


def format_rate(value) -> str:
    if value is None:
        return "N/A"
    return f"{value:.3f}"


def records_to_rows(records: Sequence[GenerationRecord]) -> List[dict]:
    rows = []
    for record in records:
        rows.append({
            "sample_id": record.sample_id,
            "model": record.model,
            "task_id": record.task_id,
            "ecosystem": record.ecosystem.value,
            "language": record.language,
            "functional_correct": record.functional_correct,
            "security_successful": record.security_successful,
            "static_flagged": record.static_flagged,
            "dynamic_evidence": record.dynamic_evidence,
            "semantic_evidence": record.semantic_evidence,
            "is_fsc": is_fsc(record),
            "is_fsc_hard": is_fsc_hard(record),
            "classification": classify(record).value,
        })
    return rows


def summary_to_markdown(summary: MetricSummary, title: str = "FSC Metric Summary") -> str:
    lines = [f"# {title}", ""]
    lines.append("| Metric | Value |")
    lines.append("|---|---:|")
    lines.append(f"| Total samples | {summary.total} |")
    lines.append(f"| Functionally correct samples | {summary.functional_correct} |")
    lines.append(f"| Security-failing samples | {summary.security_failed} |")
    lines.append(f"| FSC samples | {summary.fsc_count} |")
    lines.append(f"| FSC-hard samples | {summary.fsc_hard_count} |")
    lines.append(f"| Static-visible FSC samples | {summary.static_visible_fsc_count} |")
    lines.append(f"| Static-silent FSC samples | {summary.static_silent_fsc_count} |")
    lines.append(f"| Functional correctness rate | {format_rate(summary.functional_correctness_rate)} |")
    lines.append(f"| Raw insecure-code rate | {format_rate(summary.raw_insecure_rate)} |")
    lines.append(f"| FSC rate | {format_rate(summary.fsc_rate)} |")
    lines.append(f"| FSC-hard rate among FSC | {format_rate(summary.fsc_hard_rate_among_fsc)} |")
    return "\n".join(lines) + "\n"


def grouped_to_markdown(grouped: Dict[str, MetricSummary], title: str = "Grouped FSC Metrics") -> str:
    lines = [f"# {title}", ""]
    lines.append("| Group | Total | FCR | Raw insecure | FSC count | FSC rate | FSC-hard |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for key, summary in grouped.items():
        lines.append(
            f"| {key} | {summary.total} | {format_rate(summary.functional_correctness_rate)} | "
            f"{format_rate(summary.raw_insecure_rate)} | {summary.fsc_count} | "
            f"{format_rate(summary.fsc_rate)} | {summary.fsc_hard_count} |"
        )
    return "\n".join(lines) + "\n"


def classification_markdown(records: Sequence[GenerationRecord]) -> str:
    lines = ["# FSC Sample Classifications", ""]
    lines.append("| Sample | Model | Task | Ecosystem | FCR | SSR | FSC | FSC-hard | Classification |")
    lines.append("|---|---|---|---|---:|---:|---:|---:|---|")
    for row in records_to_rows(records):
        lines.append(
            f"| {row['sample_id']} | {row['model']} | {row['task_id']} | {row['ecosystem']} | "
            f"{row['functional_correct']} | {row['security_successful']} | {row['is_fsc']} | "
            f"{row['is_fsc_hard']} | {row['classification']} |"
        )
    return "\n".join(lines) + "\n"


def full_report(records: Sequence[GenerationRecord], group_by=("model", "ecosystem")) -> str:
    summary = compute_metrics(records)
    grouped = group_metrics(records, group_by)
    parts = [
        summary_to_markdown(summary, "FSC Benchmark Report"),
        grouped_to_markdown(grouped, f"Grouped Metrics by {', '.join(group_by)}"),
        classification_markdown(records),
        "## Interpretation Notes\n\n"
        "FSC rate is conditional on functional correctness. It should be interpreted together "
        "with functional correctness rate, raw insecure-code rate, analyzer coverage notes, and "
        "representative adjudicated examples. Synthetic fixtures in this repository are not prevalence estimates.\n",
    ]
    return "\n".join(parts)
