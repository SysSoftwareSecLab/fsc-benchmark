# FSC Taxonomy

False Security Confidence (FSC) is a measurement-oriented concept for initial LLM code generation.

## Sample-level definition

A generated sample exhibits FSC when:

```text
FCR(s) = 1 AND SSR(s) = 0
```

where:

- `FCR(s)` is the functional correctness result under the task oracle.
- `SSR(s)` is the security success result under the chosen validation stack.

## Dataset-level metric

```text
FSC rate = count(FCR = 1 AND SSR = 0) / count(FCR = 1)
```

This denominator is essential. Dividing by all generations would mix ordinary coding ability with security behavior.

## Task ecosystems

1. `general_purpose`: common algorithmic, input/output, and data-processing problems.
2. `deployment_context`: secrets, authorization, routing, configuration, service boundaries, environment assumptions.
3. `security_explicit`: direct requests for validation, sanitization, cryptography, access control, or other security behavior.

## FSC-hard

FSC-hard is a refinement layer, not a separate top-level problem:

```text
FSC-hard = FSC AND static_flagged == false AND (dynamic_evidence OR semantic_evidence)
```

It represents cases where static tooling is silent while dynamic or semantic validation still confirms that a security failure remains.

## Boundary

FSC is not a repair-time concept. Apparent repair behavior belongs to the companion Pseudo-Repair framework.
