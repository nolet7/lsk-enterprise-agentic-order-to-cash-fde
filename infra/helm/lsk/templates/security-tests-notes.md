# Production Helm security controls — implementation notes

This file is intentionally documentation only, not a rendered Kubernetes resource.
Before rollout, add and validate Pod Security admission enforcement at namespace level,
managed gateway/WAF, strict egress policies, service-to-service authentication,
autoscaling load tests, and image signature admission checks.
Do not claim these controls are enforced merely because this file exists.
