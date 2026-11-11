# LangGraph AI workflow
Authenticated buyer -> FastAPI identity -> LangGraph model call -> model selects approved JSON-schema LangChain tool -> deterministic tool code checks actor/tenant/customer -> DB contract/order/fulfillment/invoice or cited policy file -> model composes reply; cannot write.
Allowed auto tools: lookup_catalog, lookup_orders, lookup_order, lookup_invoices, lookup_support, search_policy.
Forbidden: arbitrary SQL, transaction confirmation, payment posting, impersonation, writes to external systems.
The model is a configurable OpenAI-compatible real inference API and MUST be running for /api/chat. Endpoint never switches to fake canned responses. If model is unavailable, return HTTP 503.
Draft and confirmation are deterministic legacy API paths, not model tools. Customer must perform explicit review and confirmation. See docs/API_CONTRACT.md.
POC policy retrieval uses a tiny deterministic document ranker and source IDs; it is NOT embedding/vector RAG. Upgrade to authenticated vector retrieval and citation attribution before pilot acceptance.
