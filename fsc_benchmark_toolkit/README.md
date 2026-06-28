# FSC Benchmark Toolkit

Utilities for measuring **False Security Confidence (FSC)** in benign LLM code generation.

This repository accompanies the technical report:

> Xiaolei Ren. *False Security Confidence in Benign LLM Code Generation: A Framework Note on Measurement, Task Ecosystems, and Hard Cases.* arXiv preprint, April 2026.  
> arXiv: [https://arxiv.org/abs/2604.17014](https://arxiv.org/abs/2604.17014)

## What is FSC?

False Security Confidence (FSC) describes the condition in which a generated code sample passes functional evaluation while failing security requirements, creating misleading confidence in its quality.

At the sample level:

```text
FSC(s) = functional_correct(s) AND NOT security_successful(s)
```

At the dataset level, FSC rate is a **conditional security-failure metric**:

```text
FSC rate = count(functional_correct AND security_failed) / count(functional_correct)
```

The denominator is intentionally the set of functionally correct outputs, not all generations. This isolates over-trust risk inside apparent success.

## Scope

This toolkit is an executable scaffolding for the FSC framework. It provides:

- FSC and FSC-hard metric computation.
- Three task ecosystems:
  - `general_purpose`
  - `deployment_context`
  - `security_explicit`
- JSONL input schema for model generations and validation outcomes.
- CLI commands for validation, classification, aggregation, and report generation.
- Synthetic demonstration examples.
- Documentation for measurement, validation, and future benchmark release.

## Repository Status

Benchmark data, evaluation scripts, and task definitions will be released upon paper acceptance.

The examples currently included in this repository are **synthetic demonstration fixtures**. They are intended to test the tool and illustrate the schema. They are not the final FSC benchmark dataset and should not be interpreted as prevalence evidence.

## Installation

Requires Python 3.9+.

```bash
python -m pip install -e .
```

No external runtime dependencies are required.

## Quick Start

Show taxonomy:

```bash
fsc-benchmark taxonomy
```

Validate example records:

```bash
fsc-benchmark validate examples/generations/demo_generations.jsonl
```

Classify each generation:

```bash
fsc-benchmark classify examples/generations/demo_generations.jsonl --format md
```

Compute aggregate metrics:

```bash
fsc-benchmark metrics examples/generations/demo_generations.jsonl --group-by model,ecosystem
```

Generate a Markdown report:

```bash
fsc-benchmark report examples/generations/demo_generations.jsonl --out reports/demo_report.md
```

## Input Format

Records are JSON Lines (`.jsonl`). Each line represents one generated code sample and its validation outcomes.

Minimal fields:

```json
{
  "sample_id": "sample-001",
  "model": "demo-model-a",
  "task_id": "deploy-sql-001",
  "ecosystem": "deployment_context",
  "language": "python",
  "functional_correct": true,
  "security_successful": false,
  "static_flagged": false,
  "dynamic_evidence": true,
  "semantic_evidence": false
}
```

See `docs/INPUT_SCHEMA.md` for the full schema.

## Key Outputs

For each sample, the toolkit reports:

- `functionally_correct`
- `security_successful`
- `is_fsc`
- `is_fsc_hard`
- `classification`

For groups or whole datasets, it reports:

- total sample count
- functional correctness rate
- raw insecure-code rate
- FSC rate
- FSC-hard count and FSC-hard rate among FSC cases
- analyzer-visible vs analyzer-silent FSC cases

## Definitions Implemented

### FSC

A sample is FSC when:

```text
functional_correct == true AND security_successful == false
```

### FSC-hard

A sample is FSC-hard when:

```text
is_fsc == true
AND static_flagged == false
AND (dynamic_evidence == true OR semantic_evidence == true)
```

This follows the report's definition: FSC-hard is the subset of FSC cases where static tooling fails to flag the vulnerability while dynamic or semantic validation still confirms that the exploit path or security failure remains reachable.

## Repository Layout

```text
fsc_benchmark_toolkit/
  src/fsc_benchmark/       # Python package
  examples/generations/    # synthetic JSONL fixtures
  examples/tasks/          # synthetic task metadata fixtures
  docs/                    # taxonomy, metric, schema, validation docs
  tests/                   # unit tests
  reports/                 # generated report examples
  pyproject.toml
  README.md
```

## Citation

```bibtex
@misc{ren2026fsc,
  title        = {False Security Confidence in Benign LLM Code Generation: A Framework Note on Measurement, Task Ecosystems, and Hard Cases},
  author       = {Ren, Xiaolei},
  year         = {2026},
  eprint       = {2604.17014},
  archivePrefix= {arXiv},
  primaryClass = {cs.CR}
}
```

## License

MIT License. See `LICENSE`.
