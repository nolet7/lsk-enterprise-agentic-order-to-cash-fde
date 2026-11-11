# CTO mandate -> POC -> pilot -> production
1. Discovery: buyer/CSR journeys, ERP/CRM/WMS/Billing as authorities, synthetic-only data, baseline metrics.
2. Legacy-first: tenant-scoped catalogue, contract pricing, inventory, orders, fulfillment, invoices, tickets, customer portal, migrations, tests.
3. POC: configurable real inference LangGraph, authenticated tool gateway, source-cited RAG, deterministic draft and confirmation barrier, Docker Compose/evaluations.
4. Pilot: Keycloak JWT validation, tenant membership, RBAC, approvals, audit and flags; UAT, golden/adversarial tests, synthetic load and metrics.
5. Production readiness: GKE Terraform, Helm/Argo CD, secrets, HPA, backups, SLOs, CI/CD, rollback; cloud deployment is NOT implied.
Stage gates require executed tests, artifacts and owner signoff.