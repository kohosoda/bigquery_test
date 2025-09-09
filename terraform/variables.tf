# 変数定義ファイル

variable "gcp_project_id" {
  description = "GCPプロジェクトID"
  type        = string
}

variable "bigquery_dataset_id" {
  description = "BigQueryデータセットID"
  type        = string
  default     = "ecommerce_data"
}

variable "region" {
  description = "GCPリージョン"
  type        = string
  default     = "asia-northeast1"
}

variable "environment" {
  description = "環境名（dev, staging, prod など）"
  type        = string
  default     = "dev"
}

variable "dataset_owner_email" {
  description = "データセットのオーナーメールアドレス"
  type        = string
}
