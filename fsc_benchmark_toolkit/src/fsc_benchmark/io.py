"""Input/output helpers for FSC JSONL files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List, Tuple

from .models import GenerationRecord


def load_jsonl(path: str | Path) -> List[GenerationRecord]:
    p = Path(path)
    records: List[GenerationRecord] = []
    with p.open("r", encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            try:
                obj = json.loads(stripped)
                records.append(GenerationRecord.from_dict(obj))
            except Exception as exc:
                raise ValueError(f"{p}:{line_no}: {exc}") from exc
    return records


def validate_jsonl(path: str | Path) -> Tuple[bool, List[str]]:
    errors: List[str] = []
    p = Path(path)
    try:
        with p.open("r", encoding="utf-8") as fh:
            for line_no, line in enumerate(fh, start=1):
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                try:
                    obj = json.loads(stripped)
                    GenerationRecord.from_dict(obj)
                except Exception as exc:
                    errors.append(f"{p}:{line_no}: {exc}")
    except FileNotFoundError:
        errors.append(f"File not found: {p}")
    return (len(errors) == 0, errors)


def write_json(path: str | Path, data: object) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def iter_jsonl_files(path: str | Path):
    p = Path(path)
    if p.is_file():
        yield p
    else:
        yield from sorted(p.glob("*.jsonl"))
