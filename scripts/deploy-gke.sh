#!/usr/bin/env bash
set -euo pipefail
: "${GCP_PROJECT:?Set GCP_PROJECT}"
: "${GCP_REGION:=us-central1}"
echo "Deployment is opt-in. Verify project, cloud billing, IAM, policies and Terraform plan."
terraform -chdir=infra/terraform init
terraform -chdir=infra/terraform plan -var="project_id=$GCP_PROJECT" -var="region=$GCP_REGION" -out=tfplan
echo "Review plan in infra/terraform/tfplan; apply manually only after approvals."
