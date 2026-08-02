# Security Baseline

## Phase 1 controls

- No production credentials or customer data
- Fictional deterministic demo tenant
- Environment-based configuration
- Restricted CORS origin
- Dependency and static-analysis CI foundations
- Exact decimal handling for financial values

## Planned controls

- Entra ID authentication and token validation
- Role-based authorization by tenant and business scope
- Managed identity and Key Vault
- Signed webhook validation and replay protection
- Database row-level tenant isolation
- Immutable audit events
- Rate limiting and abuse protection
- Software bill of materials, provenance, and signed releases
- Threat model and penetration-test plan
