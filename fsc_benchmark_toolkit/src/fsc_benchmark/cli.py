"""Command-line interface for fsc-benchmark."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List

from .io import load_jsonl, validate_jsonl, write_json
from .metrics import compute_metrics, group_metrics
from .reporting import classification_markdown, full_report, grouped_to_markdown, records_to_rows, summary_to_markdown
from .taxonomy import taxonomy_text


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="fsc-benchmark", description="False Security Confidence benchmark utilities")
    sub = parser.add_subparsers(dest="command", required=True)

    p_tax = sub.add_parser("taxonomy", help="Print the FSC taxonomy and measurement definitions")

    p_validate = sub.add_parser("validate", help="Validate a JSONL generation file")
    p_validate.add_argument("path", help="Path to JSONL file")

    p_classify = sub.add_parser("classify", help="Classify generation records")
    p_classify.add_argument("path", help="Path to JSONL file")
    p_classify.add_argument("--format", choices=["json", "md"], default="md")

    p_metrics = sub.add_parser("metrics", help="Compute FSC metrics")
    p_metrics.add_argument("path", help="Path to JSONL file")
    p_metrics.add_argument("--group-by", default="", help="Comma-separated fields, e.g. model,ecosystem")
    p_metrics.add_argument("--format", choices=["json", "md"], default="md")

    p_report = sub.add_parser("report", help="Generate a full Markdown report")
    p_report.add_argument("path", help="Path to JSONL file")
    p_report.add_argument("--out", help="Optional output path")
    p_report.add_argument("--group-by", default="model,ecosystem", help="Comma-separated fields")

    args = parser.parse_args(argv)

    if args.command == "taxonomy":
        print(taxonomy_text())
        return 0

    if args.command == "validate":
        ok, errors = validate_jsonl(args.path)
        if ok:
            print(f"OK: {args.path}")
            return 0
        for error in errors:
            print(error)
        return 1

    if args.command == "classify":
        records = load_jsonl(args.path)
        if args.format == "json":
            print(json.dumps(records_to_rows(records), indent=2, sort_keys=True))
        else:
            print(classification_markdown(records))
        return 0

    if args.command == "metrics":
        records = load_jsonl(args.path)
        group_by = _parse_group_by(args.group_by)
        if group_by:
            grouped = group_metrics(records, group_by)
            if args.format == "json":
                print(json.dumps({k: v.to_dict() for k, v in grouped.items()}, indent=2, sort_keys=True))
            else:
                print(grouped_to_markdown(grouped, f"Grouped Metrics by {', '.join(group_by)}"))
        else:
            summary = compute_metrics(records)
            if args.format == "json":
                print(json.dumps(summary.to_dict(), indent=2, sort_keys=True))
            else:
                print(summary_to_markdown(summary))
        return 0

    if args.command == "report":
        records = load_jsonl(args.path)
        group_by = tuple(_parse_group_by(args.group_by) or ["model", "ecosystem"])
        report = full_report(records, group_by=group_by)
        if args.out:
            out_path = Path(args.out)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(report, encoding="utf-8")
            print(f"Wrote {out_path}")
        else:
            print(report)
        return 0

    parser.error("unhandled command")
    return 2


def _parse_group_by(value: str) -> List[str]:
    return [part.strip() for part in value.split(",") if part.strip()]


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
