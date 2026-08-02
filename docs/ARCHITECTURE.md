# Architecture

## Logical flow

```text
Azure Cost exports / Kion / Kusto / Policy / Observability
                         |
                    Ingestion jobs
                         |
              Raw and normalized datasets
                         |
      DuckDB / Polars / PyArrow analytical transforms
                         |
              PostgreSQL serving and workflow data
                         |
                 FastAPI domain services
                         |
                  Next.js Value Hub UI
```

## Bounded contexts

- **Cost ingestion:** provider and platform source adapters
- **Allocation:** ownership, tags, business dimensions, shared-cost rules
- **Optimization:** recommendations, evidence, confidence, effort, risk
- **Value realization:** approved, implemented, verified, and realized savings
- **Budgeting and forecasting:** plans, actuals, variance, scenarios
- **Governance:** Azure Policy state, exceptions, remediation ownership
- **Identity and administration:** organizations, users, roles, integrations, audit

## Data principles

- Preserve source lineage for every financial metric.
- Use immutable reporting snapshots for reproducibility.
- Keep currency and decimal values exact; never use binary floating point for money.
- Separate estimated, approved, implemented, and realized value.
- Attach an owner and evidence to every actionable recommendation.

## Deployment direction

The initial local system runs Next.js, FastAPI, and PostgreSQL. Production phases add Azure Container Apps or Kubernetes, managed PostgreSQL, Key Vault, managed identity, OpenTelemetry, private networking, and Bicep-based deployment.
