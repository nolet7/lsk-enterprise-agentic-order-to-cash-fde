# POC security boundary
The POC deliberately uses static demo tokens to exercise isolated synthetic identities and local API flows. It is **not suitable for public exposure**. Bind only to loopback/restrict firewall in development. Portal CORS trusts localhost:18473 solely for local development.
Before the pilot: signed Keycloak JWT (issuer/audience/expiry and JWKS), server-derived tenant membership, bounded CSR customer selection, rate limiting, HTTPS, secret rotation, and Postgres RLS. Do not treat documentation/configuration alone as an implemented authentication safeguard.
