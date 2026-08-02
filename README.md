# MissionCloud Value Hub

MissionCloud Value Hub is a production-oriented FinOps portfolio platform that turns cloud billing, utilization, commitments, governance, and operational signals into decision-ready business value.

> Portfolio project by Nehemiah Boyce. This repository is not affiliated with, endorsed by, or an official product of Mission Cloud Services, Inc.

## Why this project exists

Cloud cost data is usually fragmented across provider exports, finance spreadsheets, observability tools, and governance platforms. Value Hub provides one internal portal for executives, finance, program managers, engineers, security teams, and administrators to answer:

- What are we spending and where?
- How much value are optimization initiatives producing?
- Which teams, services, and accounts are driving variance?
- Which recommendations are actionable now?
- Are governance controls improving cost efficiency without increasing risk?

## Phase 1 vertical slice

The starter implementation includes:

- Executive value summary API
- Ranked optimization opportunities API
- Next.js dashboard with KPI cards and opportunity table
- Typed domain models and deterministic demo data
- API unit/integration tests
- Python and web CI workflows
- Docker Compose for PostgreSQL and the API
- Nix flake development shell
- Architecture, roadmap, security, and demo documentation

## Target architecture

| Layer | Technology |
|---|---|
| Web application | TypeScript, React, Next.js App Router |
| API and orchestration | Python, FastAPI, Pydantic |
| Analytics | Polars, PyArrow, DuckDB |
| Operational database | PostgreSQL |
| Azure analytics integration | Azure Data Explorer / Kusto |
| Cloud governance | Azure Policy, Bicep |
| FinOps platform integration | Kion REST APIs and webhooks |
| Observability | OpenTelemetry-compatible logs, metrics, traces |

## Start on NixOS

```bash
nix develop
cp .env.example .env
make api-install
make web-install
```

Run the API:

```bash
make api-dev
```

In a second terminal:

```bash
nix develop
make web-dev
```

Open:

- Dashboard: `http://localhost:3000`
- API documentation: `http://localhost:8000/docs`
- Health endpoint: `http://localhost:8000/health`

## Run quality checks

```bash
make test
make lint
make typecheck
```

## Repository layout

```text
apps/web/                 Next.js dashboard
services/api/             FastAPI service
analytics/sql/            Analytical model prototypes
infra/bicep/              Azure infrastructure modules
security/                 Future threat-model assets
docs/                     Architecture, roadmap, ADRs, demo guide
.github/workflows/         Continuous integration
```

## Current implementation status

**Implemented:** Phase 1 starter vertical slice and project foundation.

**Planned:** PostgreSQL persistence, cost-ingestion pipelines, Azure/Kusto connectors, Kion integration, identity/RBAC, budgets, unit economics, anomaly detection, showback/chargeback, policy compliance, forecasting, and production deployment.

## License

This repository uses a protective source-available license. Review `LICENSE` before using the code.
