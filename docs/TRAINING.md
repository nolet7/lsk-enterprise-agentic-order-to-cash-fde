# Training guide (fictional synthetic tenants)
Buyer: sign in with a bound account; read contract catalog, order history and invoices. Draft is non-binding; review SKU/qty/price/total before sending the nonce with a unique idempotency key through the confirmation API. If stock/price changed, create a new draft. Never interpret chat text as proof of confirmation.
CSR: review tenant-scoped tickets and approval queue at /csr.html, inspect audit actions, choose approve/reject only for same-tenant items; unexpected status or finance data goes to ERP/billing owner.
Admin/SRE: configure OIDC and environment secrets, verify alerts, disable AI on degraded authority, run tenant isolation and rollback rehearsals.
