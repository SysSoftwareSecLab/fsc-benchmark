# Task Ecosystems

The FSC framework separates tasks into three ecosystems.

## General-purpose Programming

Common algorithmic, input/output, or data-processing tasks with no explicit security framing.

Potential FSC pattern: narrow functional tests pass while latent vulnerabilities are hidden.

## Deployment-context Tasks

Tasks with realistic deployment assumptions, such as:

- secrets handling
- authorization logic
- request routing
- configuration semantics
- service boundaries
- environment assumptions

Potential FSC pattern: functionally correct code fails under realistic deployment or threat assumptions.

## Security-explicit Programming

Tasks that directly request security behavior, such as:

- validation
- sanitization
- cryptography
- access control
- safe deserialization

Potential FSC pattern: the model appears to understand the security goal yet generates a vulnerable implementation.
