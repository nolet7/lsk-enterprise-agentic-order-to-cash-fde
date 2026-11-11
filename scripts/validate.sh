#!/usr/bin/env bash
set -euo pipefail
python -m compileall -q services/api/app
(cd services/api && pytest -q)
if command -v terraform >/dev/null; then terraform -chdir=infra/terraform fmt -check -recursive && terraform -chdir=infra/terraform init -backend=false && terraform -chdir=infra/terraform validate; else echo "terraform unavailable: NOT VALIDATED"; fi
if command -v helm >/dev/null; then helm lint infra/helm/lsk && helm template lsk infra/helm/lsk >/dev/null; else echo "helm unavailable: NOT VALIDATED"; fi
