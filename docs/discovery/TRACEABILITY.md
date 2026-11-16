# Requirements-to-delivery traceability

This is a **planning matrix, not a test report**. Supply-compliance functions are proposed, not verified implemented. Link every completed row to a commit, automated test run and accountable approval.

| ID | Target | POC evidence required | Pilot evidence required | Production evidence required | Verification status |
|---|---|---|---|---|---|
| BR-001 | Contract price and catalogue | ERP fixture parity | Signed contract/UAT | Live reconciliation | Not independently verified |
| BR-002 | Inventory/ATP freshness | WMS stale-source simulation | WMS contract/load test | Freshness SLI & alert | Not independently verified |
| BR-003 | Consent and idempotent order create | Duplicate/price-change tests | Concurrency + auth tests | Replay/rollback drill | Not independently verified |
| BR-004 | Fulfillment exception workflow | Split shipment fixture | Carrier/WMS event replay | Exception backlog/ownership | Planned extension |
| BR-005 | Invoice and case management | Billing/CRM fixture tests | Finance/CSR UAT | Outage & access evidence | Not independently verified |
| BR-006 | Supplier eligibility/hold | Missing/expired evidence mock tests | Quality-signed QMS contract and UAT | Revocation control audit | Proposed; not verified built |
| BR-007 | Quality approval and escalation | Unauthorized release denied | Dual control / scoped exception UAT | Periodic audit samples | Proposed; not verified built |
| BR-008 | Tenant audit | Cross-tenant negative test | IAM/access review and audit test | Retention/audit verification | Stage-dependent |
| BR-009 | Durable recovery and replay | Adapter timeout simulation | DLQ/consumer replay drill | DR & runbook exercise | Planned extension |
| BR-010 | Cited policy retrieval | Golden citation evaluation | Red-team prompt-injection evaluation | Regression metrics | Stage-dependent |
| NFR-001 | OIDC/RBAC/tenant isolation | Permission tests | Pen test and access review | Security approval | Stage-dependent |
| NFR-002 | Secrets/privacy | No secrets in Git/logs | PII/retention review | Rotation and deletion evidence | Stage-dependent |
| NFR-003 | SLOs, cost, latency | Baseline capture | Load & error-budget UAT | Monitored SLO history | Stage-dependent |
| NFR-004 | API version/rollback | Schema contract tests | Migration and rollback rehearsal | Controlled rollout logs | Stage-dependent |
| NFR-005 | Supplier override safety | Deny-on-missing evidence test | Quality signoff | Control effectiveness review | Proposed; not verified built |

## Evidence record template

Requirement ID: ___; issue / PR: ___; branch and SHA: ___; environment: ___; test command and run link: ___; expected: ___; observed: ___; date: ___; owner: ___; PASS/FAIL: ___; signoff: ___; waiver and expiry (if any): ___.

## Stage exit gates

**POC:** functioning synthetic demonstration, verified permissions/price correctness, reproducible tests, failure-path notes. **Pilot:** signed stakeholder interface contracts, supplier policy authorization before any QMS activation, measured workload UAT and security review. **Production:** actual deployment and disaster-recovery proof, supply-chain/Quality/IT signoff, monitoring and ownership. Documentation alone never qualifies a branch as production deployed.
