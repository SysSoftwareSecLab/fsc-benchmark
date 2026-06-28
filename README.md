# FSC Benchmark


fsc_benchmark_toolkit/
  README.md
  LICENSE
  CITATION.cff
  MANIFEST.md
  pyproject.toml
  src/fsc_benchmark/
    models.py
    metrics.py
    reporting.py
    io.py
    taxonomy.py
    cli.py
  examples/
    generations/demo_generations.jsonl
    tasks/demo_tasks.json
  docs/
    TAXONOMY.md
    METRICS.md
    INPUT_SCHEMA.md
    VALIDATION_GUIDE.md
    TASK_ECOSYSTEMS.md
    RELEASE_NOTES.md
  tests/
    test_metrics.py
    test_io_cli.py
  reports/
    demo_report.md

**False Security Confidence in Benign LLM Code Generation**

This repository accompanies the technical report:

> Xiaolei Ren. "False Security Confidence in Benign LLM Code 
> Generation: A Framework Note on Measurement, Task Ecosystems, 
> and Hard Cases." arXiv preprint, April 2026.
> [[arXiv link](https://arxiv.org/abs/2604.17014v2)]
https://arxiv.org/abs/2604.17014v2
## What is FSC?

False Security Confidence (FSC) describes the condition in which 
a generated code sample passes functional evaluation while failing 
security requirements — creating misleading confidence in its quality.

**FSC rate** measures security failure *within the set of 
functionally correct outputs*, not across all generations.

## Repository Status

Benchmark data, evaluation scripts, and task definitions will be 
released upon paper acceptance.

## Contact

Xiaolei Ren — xlren@must.edu.mo  
School of Computer Science and Engineering  
Macau University of Science and Technology
