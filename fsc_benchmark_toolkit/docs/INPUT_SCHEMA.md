# Input Schema

The toolkit accepts JSON Lines (`.jsonl`) files. Each line is one generated sample.

## Required fields

| Field | Type | Description |
|---|---|---|
| `sample_id` | string | Unique identifier for the generated sample. |
| `model` | string | Model or model snapshot name. |
| `task_id` | string | Task identifier. |
| `ecosystem` | string | One of `general_purpose`, `deployment_context`, `security_explicit`. |
| `language` | string | Programming language. |
| `functional_correct` | boolean | Result of the task functional oracle. |
| `security_successful` | boolean | Result of the security validation stack. |

## Optional fields

| Field | Type | Description |
|---|---|---|
| `prompt_id` | string/null | Prompt identifier. |
| `static_flagged` | boolean/null | Whether static analysis flagged the vulnerability. Required for FSC-hard analysis. |
| `dynamic_evidence` | boolean | Whether dynamic validation confirms the failure path. |
| `semantic_evidence` | boolean | Whether semantic/oracle evidence confirms the failure. |
| `analyzer_notes` | list[string] | Notes about analyzers or adjudication. |
| `security_categories` | list[string] | CWE or internal security category labels. |
| `metadata` | object | Additional fields. |

## Example

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
  "semantic_evidence": false,
  "security_categories": ["CWE-89"],
  "analyzer_notes": ["Synthetic example"],
  "metadata": {"fixture": true}
}
```
