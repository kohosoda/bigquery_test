# Terraform設定
terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

# Google Cloud Provider設定
provider "google" {
  project = var.gcp_project_id
  region  = var.region
}

# BigQueryデータセット
resource "google_bigquery_dataset" "ecommerce_dataset" {
  dataset_id                  = var.bigquery_dataset_id
  friendly_name              = "E-commerce Data"
  description                = "E-commerce sample data for learning data engineering"
  location                   = var.region
  default_table_expiration_ms = null

  # アクセス制御（必要に応じて調整）
  access {
    role          = "OWNER"
    user_by_email = var.dataset_owner_email
  }

  # 削除保護（本番環境では true に設定することを推奨）
  delete_contents_on_destroy = true

  labels = {
    environment = var.environment
    purpose     = "data-engineering"
  }
}
