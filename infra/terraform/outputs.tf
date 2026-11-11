output "cluster_name" { value = google_container_cluster.primary.name }
output "cluster_region" { value = google_container_cluster.primary.location }
output "cloudsql_connection_name" { value = google_sql_database_instance.postgres.connection_name }
output "redis_host" { value = google_redis_instance.cache.host }
output "service_account_email" { value = google_service_account.app.email }
output "artifact_registry" { value = google_artifact_registry_repository.images.id }
