# 出力値定義ファイル

output "bigquery_dataset_id" {
  description = "作成されたBigQueryデータセットのID"
  value       = google_bigquery_dataset.ecommerce_dataset.dataset_id
}

output "bigquery_dataset_location" {
  description = "BigQueryデータセットのロケーション"
  value       = google_bigquery_dataset.ecommerce_dataset.location
}

output "bigquery_dataset_friendly_name" {
  description = "BigQueryデータセットの表示名"
  value       = google_bigquery_dataset.ecommerce_dataset.friendly_name
}
