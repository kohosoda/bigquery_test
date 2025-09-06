#!/usr/bin/env python3
"""
GCSアップロード専用スクリプト
ローカルファイルをGCSにアップロードするだけの処理
"""

import os
import sys
from gcs_client import GCSClient
from config import *


def main():
    print("=== GCS Upload Only ===\n")

    # GCP環境のセットアップ
    print("Setting up GCP environment...")
    try:
        gcs_client = GCSClient()
        gcs_client.setup_gcs_bucket()
        print("✅ GCP environment setup completed\n")
    except Exception as e:
        print(f"❌ GCP setup failed: {e}")
        print("Please check your GCP credentials and configuration.")
        return False

    # データファイルのGCSアップロード
    print("Uploading files to Google Cloud Storage...")
    try:
        files_to_upload = [
            ('users.csv', 'raw/users.csv'),
            ('products.csv', 'raw/products.csv'),
            ('orders.csv', 'raw/orders.csv'),
            ('order_items.csv', 'raw/order_items.csv'),
            ('access_logs.json', 'raw/access_logs.json')
        ]

        uploaded_files = []

        for local_file, gcs_path in files_to_upload:
            local_path = f"{RAW_DATA_DIR}/{local_file}"
            if os.path.exists(local_path):
                gcs_uri = gcs_client.upload_to_gcs(local_path, gcs_path)
                uploaded_files.append((local_file, gcs_uri))
            else:
                print(f"⚠️  File not found: {local_path}")

        print("✅ Files uploaded to GCS\n")

        # アップロード結果の表示
        print("Uploaded files:")
        for filename, uri in uploaded_files:
            print(f"  {filename} → {uri}")

        print(f"\n🎉 Upload completed successfully!")
        print(f"Files are now available in GCS bucket: {GCS_BUCKET_NAME}")

    except Exception as e:
        print(f"❌ GCS upload failed: {e}")
        return False

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
