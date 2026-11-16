# Measurable FDE release gates
| Gate | Requirement | Evidence |
|---|---|---|
| No unauthorized order confirmation | 100% denied in adversarial test corpus | pytest + external security review |
| Tenant isolation | No access across 2+ tenants including CSR, chat tools and RAG | signed OIDC E2E + Postgres RLS probes |
| Price fidelity | 100% equal authoritative ERP contract in golden set | contract fixture comparison |
| Order idempotency | Concurrent same/different idempotency keys => at most one business order and one stock decrement | Postgres parallel worker test |
| Model-grounded tool calls | 100% of commercial numbers from authorized tools | captured tool audit and independent eval |
| RAG source attribution | >=95% of policy claims with verifiable tenant-allowed citations | annotated golden QA |
| End-to-end inquiries | >=90% supported tasks passed, zero misleading transaction claims | recorded UAT |
| Latency/cost | publish measured p50/p95/p99 and per interaction token cost, not just targets | load run metadata and model billing |
| Outage | during ERP/WMS outage, no order commit and explicit fallback/handoff | fault injection |
| Operational | observed rollback, backup restore, incident and SLO alerting | signed runbook drills |
All targets are acceptance thresholds, not achieved metrics. Synthetic environment only.
