# Enterprise FDE upgrade evidence — November 16, 2026
Repository: `nolet7/lsk-enterprise-agentic-order-to-cash-fde`, branch `production`.

## What changed
- **Security**: non-local `APP_ENV=pilot|production` now requires OIDC rather than demo bearer tokens. Production requires PostgreSQL. Runtime rejects demo credentials in non-local environments. Helm sets `APP_ENV=production`.
- **Database governance**: pilot/production starts only when Alembic migration metadata exists; no runtime `create_all` and no demo customer seeding outside local development. SQLAlchemy fixture startup now flushes product rows ahead of dependent contracts. This fixes a PostgreSQL foreign-key error not visible with SQLite-only tests.
- **Transaction concurrency**: draft order is `SELECT ... FOR UPDATE` locked before confirmation checks, guarding against independent simultaneous idempotency keys. PostgreSQL concurrency test asserts one confirmed outcome and exactly one stock decrement.
- **Operations**: added DB-backed `/ready` endpoint; Kubernetes readiness uses `/ready`, liveness stays on `/health`.
- **Container security**: Docker image runs UID/GID 10001 (not root); local demo Compose ports are bound to loopback.
- **CI**: production workflow includes SQLite unit job, PostgreSQL-16 service with Alembic upgrade, Postgres execution tests, OCI image build/user check and Python compile.

## Observed CI results
- First PostgreSQL run failed: `contracts_product_id_fkey` because fixture product inserts had not yet been flushed. This is an **observed and fixed defect**.
- After the fix: [GitHub Actions run 43984239736](https://github.com/nolet7/lsk-enterprise-agentic-order-to-cash-fde/actions/runs/43984239736) **all four jobs passed**; PostgreSQL integration showed **8 tests passed in 1.62 seconds**.
- Follow-up release migration startup change: [GitHub Actions run 43984304046](https://github.com/nolet7/lsk-enterprise-agentic-order-to-cash-fde/actions/runs/43984304046) passed.
- Latest workflow URL should be checked independently before final signoff. CI is not a live cloud deployment or model benchmark.

## Useful operator commands
```bash
git checkout production
cp .env.example .env
# local POC mode only: APP_ENV=local AUTH_MODE=demo
docker compose up --build -d
docker compose exec api python -m pytest -q
curl http://localhost:18474/ready
```
For PostgreSQL migration before pilot/production service startup:
```bash
cd services/api
DATABASE_URL='postgresql+psycopg://<user>:<password>@<host>:5432/<database>' alembic upgrade head
```
The above is a template. Do not paste production passwords in a shared shell history or commit them.

## Still not verified or fully implemented
- Authenticated live Keycloak browser login and tenant membership provisioning
- Working MCP transport / strict server capability authorization
- Embedding-backed ACL-filtered RAG and independent retrieval ground-truth scores
- Separate ERP/CRM/WMS/Billing simulators wired into every commercial transaction
- Live Temporal workflow worker and complete supplier compliance workflow
- Real model inference / tool-call traces / model cost and latency baselines
- Terraform/GKE deployment, Helm render on cloud target, canary and disaster recovery drills
- End-user UAT, on-call signoff and business ROI

**Classification:** strengthened production-oriented implementation with passing CI; not yet a deployed enterprise production system.
