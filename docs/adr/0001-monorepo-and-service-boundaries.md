# ADR 0001: Monorepo with explicit service boundaries

- Status: Accepted
- Date: 2026-08-02

## Decision

Use a monorepo containing the Next.js application, FastAPI service, analytics assets, infrastructure code, and project documentation. Preserve clear boundaries between presentation, API, domain, integration, analytics, and infrastructure concerns.

## Rationale

The product requires coordinated contracts and a coherent portfolio demonstration, while still needing service boundaries that can later be deployed independently.

## Consequences

- One pull request can update API contracts and the UI together.
- CI can validate each component independently.
- The repository must enforce ownership and avoid cross-layer coupling as scope grows.
