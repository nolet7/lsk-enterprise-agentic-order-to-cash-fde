resource "google_project_service" "apis" {
  for_each = toset(["compute.googleapis.com","container.googleapis.com","sqladmin.googleapis.com","redis.googleapis.com","secretmanager.googleapis.com","servicenetworking.googleapis.com","artifactregistry.googleapis.com"])
  project = var.project_id
  service = each.key
  disable_on_destroy = false
}
resource "google_compute_network" "vpc" {
  name = "lsk-otc-vpc"
  auto_create_subnetworks = false
  depends_on = [google_project_service.apis]
}
resource "google_compute_subnetwork" "gke" {
  name = "lsk-otc-subnet"
  ip_cidr_range = "10.70.0.0/20"
  region = var.region
  network = google_compute_network.vpc.id
  private_ip_google_access = true
  secondary_ip_range {
    range_name = "pods"
    ip_cidr_range = "10.80.0.0/16"
  }
  secondary_ip_range {
    range_name = "services"
    ip_cidr_range = "10.90.0.0/20"
  }
}
resource "google_compute_router" "router" {
  name = "lsk-otc-router"
  region = var.region
  network = google_compute_network.vpc.id
}
resource "google_compute_router_nat" "nat" {
  name = "lsk-otc-nat"
  router = google_compute_router.router.name
  region = var.region
  nat_ip_allocate_option = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"
}
resource "google_container_cluster" "primary" {
  name = var.cluster_name
  location = var.region
  network = google_compute_network.vpc.id
  subnetwork = google_compute_subnetwork.gke.id
  remove_default_node_pool = true
  initial_node_count = 1
  deletion_protection = var.deletion_protection
  networking_mode = "VPC_NATIVE"
  ip_allocation_policy {
    cluster_secondary_range_name = "pods"
    services_secondary_range_name = "services"
  }
  private_cluster_config {
    enable_private_nodes = true
    enable_private_endpoint = false
    master_ipv4_cidr_block = "172.16.2.0/28"
  }
  workload_identity_config { workload_pool = "${var.project_id}.svc.id.goog" }
  release_channel { channel = "REGULAR" }
  depends_on = [google_project_service.apis]
}
resource "google_container_node_pool" "workers" {
  name = "lsk-workers"
  cluster = google_container_cluster.primary.id
  location = var.region
  initial_node_count = 1
  autoscaling {
    min_node_count = 1
    max_node_count = 3
  }
  node_config {
    machine_type = "e2-standard-4"
    service_account = google_service_account.gke_nodes.email
    oauth_scopes = ["https://www.googleapis.com/auth/cloud-platform"]
    workload_metadata_config { mode = "GKE_METADATA" }
    shielded_instance_config { enable_secure_boot = true enable_integrity_monitoring = true }
  }
}
resource "google_service_account" "gke_nodes" {
  account_id = "lsk-otc-gke-nodes"
}
resource "google_project_iam_member" "node_log" {
  project = var.project_id
  role = "roles/logging.logWriter"
  member = "serviceAccount:${google_service_account.gke_nodes.email}"
}
resource "google_project_iam_member" "node_metric" {
  project = var.project_id
  role = "roles/monitoring.metricWriter"
  member = "serviceAccount:${google_service_account.gke_nodes.email}"
}
resource "google_compute_global_address" "private_sql" {
  name = "lsk-otc-private-sql"
  purpose = "VPC_PEERING"
  address_type = "INTERNAL"
  prefix_length = 16
  network = google_compute_network.vpc.id
}
resource "google_service_networking_connection" "private" {
  network = google_compute_network.vpc.id
  service = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_sql.name]
}
resource "google_sql_database_instance" "postgres" {
  name = "lsk-otc-postgres"
  region = var.region
  database_version = "POSTGRES_16"
  deletion_protection = var.deletion_protection
  settings {
    tier = "db-custom-2-7680"
    availability_type = "REGIONAL"
    backup_configuration {
      enabled = true
      point_in_time_recovery_enabled = true
      backup_retention_settings { retained_backups = 14 }
    }
    ip_configuration {
      ipv4_enabled = false
      private_network = google_compute_network.vpc.id
    }
  }
  depends_on = [google_service_networking_connection.private]
}
resource "google_sql_database" "app" {
  name = "lsk"
  instance = google_sql_database_instance.postgres.name
}
resource "google_sql_user" "app" {
  name = "lsk_app"
  instance = google_sql_database_instance.postgres.name
  password = var.db_password
}
resource "google_redis_instance" "cache" {
  name = "lsk-otc-cache"
  tier = "STANDARD_HA"
  memory_size_gb = 1
  region = var.region
  authorized_network = google_compute_network.vpc.id
  redis_version = "REDIS_7_0"
  depends_on = [google_project_service.apis]
}
resource "google_secret_manager_secret" "model_key" {
  secret_id = "lsk-otc-model-key"
  replication { auto {} }
  depends_on = [google_project_service.apis]
}
resource "google_service_account" "app" {
  account_id = "lsk-otc-api"
}
resource "google_service_account_iam_member" "wi" {
  service_account_id = google_service_account.app.name
  role = "roles/iam.workloadIdentityUser"
  member = "serviceAccount:${var.project_id}.svc.id.goog[lsk/lsk-api]"
}
resource "google_secret_manager_secret_iam_member" "read_model_key" {
  secret_id = google_secret_manager_secret.model_key.id
  role = "roles/secretmanager.secretAccessor"
  member = "serviceAccount:${google_service_account.app.email}"
}
resource "google_artifact_registry_repository" "images" {
  location = var.region
  repository_id = "lsk-otc"
  format = "DOCKER"
}
