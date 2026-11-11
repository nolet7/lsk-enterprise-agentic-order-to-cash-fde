# Test evidence log
2026-11-11: source committed remotely. Runtime validation PENDING: Docker CLI/daemon are unavailable in the current execution container; public GitHub not reachable from its networking sandbox. This is NOT a test pass.
To validate legacy before AI:
```bash
docker compose up --build -d
docker compose exec api pytest -q
curl -H 'Authorization: Bearer demo-buyer-a' http://localhost:18474/api/catalog
curl -H 'Authorization: Bearer demo-buyer-b' http://localhost:18474/api/catalog
docker compose exec api python evals/run.py  # when eval script is copied/mounted and model is configured
```
Check and record actual test result, Postgres transaction behavior, auth isolation, model inference and p95. No measured p95 or model cost is available yet.
