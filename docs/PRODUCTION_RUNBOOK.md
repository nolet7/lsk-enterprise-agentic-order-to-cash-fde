# Production readiness and handover — NOT DEPLOYED
## Preconditions
Dedicated GCP project, billing approval, VPC/cloud firewall/egress policy, infrastructure owner, SOC review, approved OIDC issuer, approved model data policy, backup owner, live adapter credentials, signed container images, verified database migrations and golden evaluation pass.
## Build and deployment
1. Pin approved immutable container digest and scan SBOM/dependencies.
2. `bash scripts/validate.sh` (requires Terraform/Helm/Python).
3. `GCP_PROJECT=... bash scripts/deploy-gke.sh` to generate a PLAN only; manually review/apply after change approval.
4. Configure Cloud SQL secret via External Secrets/CSI integration and Workload Identity; manually create initial DB and run Alembic migrations. No literal database credentials in Git.
5. Update Helm values with environment-specific image digest, IdP, origins, service account; `helm lint`, `helm template`.
6. Bootstrap Argo CD by approved change, restrict sync permissions, integrate rollout controller and canary analysis. Current Argo Application alone is NOT canary automation.
7. Verify health checks, customer isolation, model/tool safety, end-to-end transaction, 5xx alerts and ERP outage drill.
## Canary and rollback strategy
Proposed 1% -> 5% -> 25% -> 100% traffic after >=30m stable/error-budget windows, require approval between steps. Separate rollout controller is a prerequisite; not installed by this repository. Roll back image/flags on increased error ratio, p95 or any unsafe write. DB migrations must be backward-compatible.
## SLOs
Suggested API availability >=99.9%/30d, p95 read <500ms excluding model, customer chat p95 <5s on defined model, unauthorized writes =0, tenant crossover =0. Burn-rate alert 14.4x/1h and 6x/6h after sufficient traffic. These are targets, not measured performance.
## DR
Cloud SQL regional HA and PITR with 14-day retained backups configured in Terraform; perform an observed restore into isolated project before claiming RPO/RTO. Proposed RPO<=15min and RTO<=4h contingent on rehearsals. Redis cache reconstructible, rehydrate Temporal workflows separately.
## On-call and escalation
CSR -> application on-call -> platform/SRE -> ERP/WMS/Billing owners. Treat unexpected price mismatch, cross-tenant information and unintended writes as SEV1. Disable agent feature flag and preserve audit evidence.
## Operator handover
Transfer architecture, versioned API schema, cloud IaC state backend, secrets ownership, dashboards, paging, backups, legal/vendor data agreements, UAT/evaluation signoffs and support/training artifacts. No production acceptance is claimed.
