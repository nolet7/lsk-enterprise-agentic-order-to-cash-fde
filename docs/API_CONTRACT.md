# Legacy API contract
OpenAPI: GET /openapi.json; interactive GET /docs. Header Authorization: Bearer demo-buyer-a or demo-buyer-b (POC synthetic only).
GET /api/catalog : authorized contract prices and inventory.
GET /api/orders, /api/orders/{id} : customer-scope order + WMS fulfillment.
GET /api/invoices : customer-scope billing.
GET /api/tickets : customer support queue; POST /api/tickets {subject}.
POST /api/orders/drafts {product_id, quantity} : prices and stock deterministic; returns nonce.
POST /api/orders/drafts/{id}/confirm {confirmation_nonce,idempotency_key} : explicit server confirmation; DB idempotency.
GET /api/audit : CSR only; GET /metrics : metrics.
Error codes: 401 authentication, 403 authorization, 404 masked cross-tenant object, 409 changed terms or unavailable inventory, 503 missing production IdP config.
POC demo token is *insecure* and must never be exposed publicly or used with real data.
