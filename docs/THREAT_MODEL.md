# STRIDE threat model
Spoofing: signed JWT issuer/audience/expiry validation at pilot and production; POC demo auth not production-grade.
Tampering: Pydantic schemas, database constraints, request signatures and webhook replay protection.
Repudiation: audit actor/tenant/action/decision and correlation ID, export records to remote retention.
Information disclosure: enforced tenant scoping, object membership, no model or logs containing credentials.
Denial of service: rate limit, timeouts, retries only for safe requests, circuit breakers and quotas.
Elevation of privilege: allowlisted tools and fine-grained authorization, human approval for writes.
Prompt injection: untrusted user and document text, deterministic tool checks. Residual threats require security testing before real customers.