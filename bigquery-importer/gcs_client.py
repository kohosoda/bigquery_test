from google.cloud import storage
from google.cloud.exceptions import NotFound
import os
from config import *


class GCSClient:
    """Google Cloud Storage専用クライアント"""

    def __init__(self):
        self.storage_client = storage.Client(project=GCP_PROJECT_ID)
        self.bucket = None

    def setup_gcs_bucket(self):
        """GCSバケットの作成またはアクセス確認"""
        try:
            self.bucket = self.storage_client.bucket(GCS_BUCKET_NAME)
            self.bucket.reload()  # バケットが存在するかチェック
            print(f"Using existing bucket: {GCS_BUCKET_NAME}")
        except NotFound:
            print(f"Creating new bucket: {GCS_BUCKET_NAME}")
            self.bucket = self.storage_client.create_bucket(
                GCS_BUCKET_NAME, location='asia-northeast1')

        return self.bucket

    def upload_to_gcs(self, local_file_path, gcs_file_path):
        """ファイルをGCSにアップロード"""
        if not self.bucket:
            raise ValueError(
                "GCS bucket not initialized. Call setup_gcs_bucket() first.")

        blob = self.bucket.blob(gcs_file_path)
        blob.upload_from_filename(local_file_path)
        print(
            f"Uploaded {local_file_path} to gs://{GCS_BUCKET_NAME}/{gcs_file_path}")

        return f"gs://{GCS_BUCKET_NAME}/{gcs_file_path}"


if __name__ == "__main__":
    # テスト用コード
    print("=== GCS Client Test ===")
    gcs_client = GCSClient()
    gcs_client.setup_gcs_bucket()
