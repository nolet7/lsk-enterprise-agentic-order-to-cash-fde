# Verification results — 2026-11-11
## Verified by GitHub Actions (actual execution)
- POC: CI green: https://github.com/nolet7/lsk-enterprise-agentic-order-to-cash-fde/actions/runs/43062903264
- Pilot: CI green: https://github.com/nolet7/lsk-enterprise-agentic-order-to-cash-fde/actions/runs/43062909728
- Production configuration branch: CI green: https://github.com/nolet7/lsk-enterprise-agentic-order-to-cash-fde/actions/runs/43062917850
- Production Python job log: **4 passed in 1.58s** (SQLite tests); manifests Python compilation passed.
- Tests cover legacy catalog and invoice fidelity, tenant denial on known identifiers, draft nonce and idempotency flow, CSR permissions, webhook signature checks, and agent 503 when real model is not configured.
- Initial CI failed due to import invocation; corrected by using `python -m pytest -q`. Final runs above succeeded.

## Not executed or not established
- Docker Compose startup and browser E2E (Docker unavailable here)
- Real model inference, tool-selection golden evaluation, full agent E2E and RAG groundedness
- Full Postgres concurrency, migration upgrade, OIDC/Keycloak end-to-end sign-in and Temporal worker execution
- Terraform validate/plan, Helm lint/render, security scanning, GKE provision and restore/canary
- No actual achieved p95 latency, model cost or business ROI metrics

**CI passing is not evidence of full functional or cloud deployment acceptance.** See issues #1–#5 for remaining P0/P1 gates.
