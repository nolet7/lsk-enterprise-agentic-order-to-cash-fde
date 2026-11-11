# Architecture and customer journey
## POC
```mermaid
flowchart LR
Buyer --> Portal[Legacy portal and AI chat]
CSR --> Dashboard[CSR queue]
Portal --> API[FastAPI authenticated BFF]
Dashboard --> API
API --> DB[(PostgreSQL)]
API --> Adapters[ERP CRM WMS Billing simulators]
Portal --> Agent[LangGraph]
Agent --> Model[Configurable real model endpoint]
Agent --> Tools[Allowlisted tool gateway]
Tools --> API
Agent --> RAG[Policy docs and citations]
```
## Pilot
```mermaid
flowchart LR
Users --> Keycloak[OIDC Keycloak]
Users --> API[RBAC tenant API]
API --> PG[(PostgreSQL)]
API --> Redis
API --> Temporal
API --> Observability[Prometheus Grafana]
API --> Reviews[Human approval queue]
```
## Production target—not deployed
```mermaid
flowchart LR
Buyers --> LB[HTTPS load balancer]
LB --> GKE[GKE ingress portal APIs HPA]
GKE --> SQL[(Cloud SQL)]
GKE --> Cache[(Memorystore)]
GKE --> SM[Secret Manager]
GKE --> External[ERP CRM WMS Billing gateways]
GKE --> AI[Model gateway and RAG]
ArgoCD --> GKE
```
## Journey
Login -> verified account -> catalogue/contract price/availability -> order tracking/invoices -> draft -> review snapshot -> explicit nonce and idempotency confirmation -> server-side revalidation -> authoritative order ID -> delivery updates/ticket or human handoff.