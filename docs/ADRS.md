# ADRs
ADR-001: ERP price/order, WMS inventory/fulfillment, CRM tickets, billing invoices are authoritative; AI never changes source-of-truth.
ADR-002: tenant/customer filtered SQL and membership-enforced writes. Production add RLS and independent roles.
ADR-003: LangGraph orchestrator and only registered typed tools, no arbitrary SQL or direct DB writes from model.
ADR-004: RAG is policy-only with citations; never quote price, stock or settlement from embeddings.
ADR-005: order confirmation requires a draft, nonce, authenticated user, current price/stock revalidation and idempotency uniqueness.
ADR-006: Docker Compose local POC, Keycloak and Temporal pilot, GKE/Cloud SQL/Memorystore target; infra templates are not proof of deployment.