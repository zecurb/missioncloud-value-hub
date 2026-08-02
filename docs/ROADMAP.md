# Delivery Roadmap

## Phase 1 — Foundation and executive vertical slice

- Monorepo and reproducible development environment
- Typed API and dashboard
- Demo value summary and optimization backlog
- Tests, linting, type checking, and CI

## Phase 2 — Persistence and tenant model

- PostgreSQL schema and migrations
- Organizations, business units, accounts, services, teams, users, roles
- Repository and service layers
- Audit events

## Phase 3 — Cost ingestion and normalization

- Azure Cost Management export adapter
- Idempotent ingestion jobs
- Raw, normalized, and curated datasets
- Polars/PyArrow transformations and DuckDB validation

## Phase 4 — Allocation and unit economics

- Tag and account ownership rules
- Shared-cost allocation engine
- Allocation coverage dashboard
- Cost per customer, workload, transaction, and environment

## Phase 5 — Optimization workflow

- Recommendation evidence and scoring
- Approval, assignment, exception, and verification workflow
- Realized-savings ledger
- Engineering action views

## Phase 6 — Budgets, forecasting, and anomalies

- Budget plans and variance
- Forecasting baselines and scenarios
- Cost anomaly detection and triage
- Alert routing

## Phase 7 — Kusto, Kion, and governance integrations

- Azure Data Explorer queries
- Kion REST API and webhook adapters
- Azure Policy compliance and exceptions
- Integration health monitoring

## Phase 8 — Enterprise security and operations

- OIDC/Entra ID authentication
- RBAC and least privilege
- Secret management
- OpenTelemetry and SLOs
- Backup, recovery, and resilience testing

## Phase 9 — Training and adoption package

- Executive, finance, engineer, and administrator runbooks
- Guided demo tenant
- Workshops and exercises
- Adoption metrics and operating model

## Phase 10 — Release hardening

- Performance and security tests
- Accessibility review
- Deployment automation
- Release notes, architecture diagrams, screenshots, and portfolio case study
