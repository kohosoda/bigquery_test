#!/usr/bin/env python3
"""
メインETL処理スクリプト
サンプルデータ生成 → GCSアップロード → BigQueryロード
"""

from inspect import _void
import os
import sys
from data_generator import SampleDataGenerator
from gcs_client import GCSClient
from bigquery_client import BigQueryClient
from bigquery_schemas import BigQuerySchemas
from config import *


def main():
    """
    パイプラインのメイン処理

    前提条件：
    - BigQueryデータセットがTerraformで事前作成されていること

    実行される処理の流れ：
    1. サンプルデータの生成
    2. GCP環境の確認（データセット存在確認等）
    3. データファイルのGCSアップロード
    4. GCSからBigQueryへのデータロード

    Returns:
        bool: 処理が成功した場合True、失敗した場合False
    """
    print("=== Data Engineering ETL Pipeline ===\n")

    # 1. サンプルデータの生成
    print("Step 1: Generating sample data...")
    generator = SampleDataGenerator()
    generator.generate_all_data()
    print("✅ Sample data generation completed\n")

    # 2. GCP環境の確認
    print("Step 2: Verifying GCP environment...")
    try:
        gcs_client = GCSClient()
        bigquery_client = BigQueryClient()
        gcs_client.setup_gcs_bucket()
        bigquery_client.setup_bigquery_dataset()  # データセット存在確認のみ
        print("✅ GCP environment verification completed\n")
    except Exception as e:
        print(f"❌ GCP environment verification failed: {e}")
        print("Please check your GCP credentials and ensure the BigQuery dataset is created using Terraform.")
        return False

    # 3. データファイルのGCSアップロード
    try:
        gcs_uris = _upload_files_to_gcs(gcs_client)
    except Exception as e:
        print(f"❌ GCS upload failed: {e}")
        return False

    # 4. GCSからBigQueryへのデータロード
    try:
        _load_data_from_gcs_to_bigquery(bigquery_client, gcs_uris)
    except Exception as e:
        print(f"❌ BigQuery load from GCS failed: {e}")
        return False

    print("🎉 ETL Pipeline completed successfully!")
    print(f"Data is now available in BigQuery dataset: {BIGQUERY_DATASET}")
    print(f"You can start querying the data using BigQuery console or dbt.")

    return True


def _upload_files_to_gcs(gcs_client: GCSClient) -> dict:
    """ローカルファイルをGCSにアップロード"""
    print("Step 3: Uploading files to Google Cloud Storage...")

    files_to_upload = [
        ('users.csv', 'raw/users.csv'),
        ('products.csv', 'raw/products.csv'),
        ('orders.csv', 'raw/orders.csv'),
        ('order_items.csv', 'raw/order_items.csv'),
        ('access_logs.json', 'raw/access_logs.json')
    ]

    gcs_uris = {}  # GCS URIを保存

    for local_file, gcs_path in files_to_upload:
        local_path = f"{RAW_DATA_DIR}/{local_file}"
        if os.path.exists(local_path):
            gcs_uri = gcs_client.upload_to_gcs(local_path, gcs_path)
            gcs_uris[local_file] = gcs_uri
        else:
            print(f"⚠️  File not found: {local_path}")

    print("✅ Files uploaded to GCS\n")
    return gcs_uris


def _load_data_from_gcs_to_bigquery(bigquery_client: BigQueryClient, gcs_uris: dict) -> None:
    """GCSからBigQueryにデータをロード"""
    print("Step 4: Loading data from GCS to BigQuery...")

    schemas = BigQuerySchemas.get_schemas()

    # CSVファイルのロード（GCS経由）
    csv_tables = [
        ('users.csv', 'users'),
        ('products.csv', 'products'),
        ('orders.csv', 'orders'),
        ('order_items.csv', 'order_items')
    ]

    for csv_file, table_name in csv_tables:
        if csv_file in gcs_uris:
            bigquery_client.load_csv_from_gcs_to_bigquery(
                gcs_uris[csv_file],
                table_name,
                schema=schemas.get(table_name)
            )
        else:
            print(f"⚠️  GCS URI not found for: {csv_file}")

    # JSONファイルのロード（GCS経由）
    json_file = 'access_logs.json'
    if json_file in gcs_uris:
        bigquery_client.load_json_from_gcs_to_bigquery(
            gcs_uris[json_file],
            'access_logs',
            schema=schemas.get('access_logs')
        )
    else:
        print(f"⚠️  GCS URI not found for: {json_file}")

    print("✅ Data loaded from GCS to BigQuery\n")


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
