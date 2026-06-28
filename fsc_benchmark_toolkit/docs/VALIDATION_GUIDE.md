# Validation Guide

The FSC framework depends on disciplined validation.

## Functional Correctness

Use task-specific oracles whenever possible:

- unit tests
- property tests
- reference output comparison
- domain-specific behavioral checks

Avoid treating stylistic plausibility as functional correctness.

## Security Success

Security validation may include:

- static analyzers
- dynamic tests
- exploit oracles
- semantic validation
- selective human adjudication

The validation stack should be sufficient for the claim being made.

## FSC-hard Claims

For FSC-hard claims, static silence alone is not enough. FSC-hard requires that static tooling fails to flag the vulnerability while dynamic or semantic evidence still confirms that the security failure is reachable or substantively present.

## Synthetic Fixtures

The included examples are only synthetic fixtures for testing the toolkit. They are not benchmark data and should not be used for prevalence claims.
