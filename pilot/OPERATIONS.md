# Pilot operations
Run with `docker compose -f docker-compose.yml -f pilot/docker-compose.pilot.yml up --build` after configuring an actual Keycloak realm and database permissions. If enabling AUTH_MODE=oidc without a configured IdP, the API fails closed.
Prometheus scrape file in pilot/observability/prometheus.yml; alert rules in alerts.yml. Configure external Prometheus/Grafana services; the supplied files alone do not create a running dashboard.
Ramp tenants incrementally by PILOT_AI_ENABLED feature flag; disable model integration on regression. Record model/tool traces with tenant-safe redaction and cost/latency.
Exit criteria: all auth, isolation, UAT, outage, golden/adversarial and observability tests executed and documented; production cannot advance on documentation alone.
