variable "project_id" { type = string }
variable "region" { type = string default = "us-central1" }
variable "zone" { type = string default = "us-central1-a" }
variable "cluster_name" { type = string default = "lsk-otc" }
variable "db_password" { type = string sensitive = true }
variable "deletion_protection" { type = bool default = true }
