from google.cloud import bigquery
from google.cloud.exceptions import NotFound
import pandas as pd
import json
import os
from config import *


class BigQueryClient:
    """BigQuery専用クライアント"""

    def __init__(self):
        self.bigquery_client = bigquery.Client(project=GCP_PROJECT_ID)
        self.dataset = None

    def setup_bigquery_dataset(self):
        """BigQueryデータセットへのアクセス確認（Terraformで事前作成されている前提）"""
        dataset_id = f"{GCP_PROJECT_ID}.{BIGQUERY_DATASET}"

        try:
            self.dataset = self.bigquery_client.get_dataset(dataset_id)
            print(f"Using existing dataset: {BIGQUERY_DATASET}")
        except NotFound:
            raise ValueError(
                f"Dataset '{BIGQUERY_DATASET}' not found. "
                f"Please create the dataset using Terraform first. "
                f"Run 'cd terraform && terraform apply' to create the dataset."
            )

        return self.dataset

    def upload_csv_to_bigquery(self, csv_file_path, table_name, schema=None):
        """CSVファイルをBigQueryにロード"""
        if not self.dataset:
            raise ValueError(
                "BigQuery dataset not initialized. Call setup_bigquery_dataset() first.")

        table_id = f"{GCP_PROJECT_ID}.{BIGQUERY_DATASET}.{table_name}"

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=True if schema is None else False,
            schema=schema,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
        )

        with open(csv_file_path, "rb") as source_file:
            job = self.bigquery_client.load_table_from_file(
                source_file, table_id, job_config=job_config
            )

        job.result()  # ジョブの完了を待機

        table = self.bigquery_client.get_table(table_id)
        print(f"Loaded {table.num_rows} rows to {table_id}")

        return table

    def load_csv_from_gcs_to_bigquery(self, gcs_uri, table_name, schema=None):
        """GCS上のCSVファイルをBigQueryにロード"""
        if not self.dataset:
            raise ValueError(
                "BigQuery dataset not initialized. Call setup_bigquery_dataset() first.")

        table_id = f"{GCP_PROJECT_ID}.{BIGQUERY_DATASET}.{table_name}"

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=True if schema is None else False,
            schema=schema,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
        )

        # GCS URIから直接ロード（ファイルを読み込む必要なし！）
        load_job = self.bigquery_client.load_table_from_uri(
            gcs_uri, table_id, job_config=job_config
        )

        load_job.result()  # ジョブの完了を待機

        table = self.bigquery_client.get_table(table_id)
        print(f"Loaded {table.num_rows} rows from {gcs_uri} to {table_id}")

        return table

    def load_json_from_gcs_to_bigquery(self, gcs_uri, table_name, schema=None):
        """GCS上のJSONファイルをBigQueryにロード"""
        if not self.dataset:
            raise ValueError(
                "BigQuery dataset not initialized. Call setup_bigquery_dataset() first.")

        table_id = f"{GCP_PROJECT_ID}.{BIGQUERY_DATASET}.{table_name}"

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
            autodetect=True if schema is None else False,
            schema=schema,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
        )

        # GCS URIから直接ロード
        load_job = self.bigquery_client.load_table_from_uri(
            gcs_uri, table_id, job_config=job_config
        )

        load_job.result()  # ジョブの完了を待機

        table = self.bigquery_client.get_table(table_id)
        print(f"Loaded {table.num_rows} rows from {gcs_uri} to {table_id}")

        return table

    def upload_json_to_bigquery(self, json_file_path, table_name, schema=None):
        """JSONファイルをBigQueryにロード"""
        if not self.dataset:
            raise ValueError(
                "BigQuery dataset not initialized. Call setup_bigquery_dataset() first.")

        table_id = f"{GCP_PROJECT_ID}.{BIGQUERY_DATASET}.{table_name}"

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
            autodetect=True if schema is None else False,
            schema=schema,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
        )

        with open(json_file_path, "rb") as source_file:
            job = self.bigquery_client.load_table_from_file(
                source_file, table_id, job_config=job_config
            )

        job.result()  # ジョブの完了を待機

        table = self.bigquery_client.get_table(table_id)
        print(f"Loaded {table.num_rows} rows to {table_id}")

        return table

    def run_query(self, query):
        """BigQueryクエリの実行"""
        query_job = self.bigquery_client.query(query)
        results = query_job.result()
        return results

    def query_to_dataframe(self, query):
        """BigQueryクエリの結果をDataFrameで取得"""
        return self.bigquery_client.query(query).to_dataframe()


if __name__ == "__main__":
    # テスト用コード
    print("=== BigQuery Client Test ===")
    bigquery_client = BigQueryClient()
    bigquery_client.setup_bigquery_dataset()
