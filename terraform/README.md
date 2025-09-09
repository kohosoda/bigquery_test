# Terraform設定

このディレクトリには、BigQueryデータセットを管理するためのTerraform設定が含まれています。

## 前提条件

1. Terraformがインストールされていること（v1.0以上）
2. Google Cloud SDKがインストールされ、認証が完了していること
3. GCPプロジェクトでBigQuery APIが有効になっていること

## セットアップ

1. 設定ファイルの作成:
```bash
cp terraform.tfvars.example terraform.tfvars
```

2. `terraform.tfvars`ファイルを編集し、実際の値を設定:
```
gcp_project_id = "your-actual-project-id"
dataset_owner_email = "your-actual-email@example.com"
```

3. Terraformの初期化:
```bash
terraform init
```

4. 設定の確認:
```bash
terraform plan
```

5. リソースの作成:
```bash
terraform apply
```

## ファイル構成

- `main.tf`: メインのTerraform設定（BigQueryデータセット定義）
- `variables.tf`: 変数定義
- `outputs.tf`: 出力値定義
- `terraform.tfvars.example`: 設定例ファイル
- `terraform.tfvars`: 実際の設定ファイル（git管理対象外）

## 管理されるリソース

- `google_bigquery_dataset.ecommerce_dataset`: E-commerceデータ用のBigQueryデータセット
  - デフォルトデータセット名: `ecommerce_data`
  - ロケーション: `asia-northeast1`
  - 説明: "E-commerce sample data for learning data engineering"

## 注意事項

- `terraform.tfvars`ファイルは機密情報を含むため、gitリポジトリにコミットしないでください
- 本番環境では、`delete_contents_on_destroy`を`false`に設定してデータの誤削除を防ぐことを推奨します
- データセットのアクセス権限は必要に応じて調整してください
