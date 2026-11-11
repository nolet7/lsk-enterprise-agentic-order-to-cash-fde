# LSK Enterprise Agentic Order-to-Cash FDE
Synthetic multi-tenant wholesale food-ingredients commercial platform. **No manufacturing systems, no real customer data, no real transactions.**

## Branch progression
- `main`: charter, ADRs, workflows, safety contract
- `poc`: working legacy commerce API + portal and optional real-model LangGraph assistant
- `pilot`: tenant-aware pilot control additions, Keycloak configuration, evaluations and operations
- `production`: GCP/GKE IaC, Helm, Argo CD and release/operations documentation **(not deployed)**

Each successor branch inherits its predecessor. Switching branches is necessary to see the increment.

## Business invariant
Server-side commerce functions own prices, inventory, order and invoice state. The assistant cannot mint transactional facts. Order confirmation requires a previously created draft, an authenticated authorized actor, an exact nonce/confirmation and an idempotency key. RAG is for policy text, **not commercial truth**.

## Quick start
See `docs/SETUP.md` on each implementation branch. Use only synthetic fixture tenants. This project is a portfolio/reference environment; no demonstrated production cloud deployment.
