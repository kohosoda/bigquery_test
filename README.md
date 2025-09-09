# BigQuery学習プロジェクト

ローカルDockerとGCP BigQueryを活用した最小構成でのデータ基盤構築を行います。

## 🎯 プロジェクトの目標

- BigQueryへのデータインポート処理の実装
- dbtを使ったデータ変換処理の体験
- BigQueryを活用したデータ分析基盤の構築
- データ可視化とレポート作成

## 🏗️ システム構成

```
[データ生成] → [ローカルDocker] → [GCS] → [BigQuery] → [レポート/ダッシュボード]
     ↓              ↓              ↓         ↓              ↓
サンプルデータ  データインポート  データレイク   DWH      可視化・分析
  (Python)    (Python/dbt)   (JSON/CSV)  (SQL/dbt)   (Looker Studio)
```

## 🛠️ 技術スタック

- **言語**: Python 3.11
- **コンテナ**: Docker Compose
- **データ変換**: dbt-bigquery
- **インフラ管理**: Terraform
- **クラウド**: Google Cloud Platform (BigQuery, Cloud Storage)
- **分析**: Jupyter Notebook, Looker Studio

## 📊 データモデル

### Raw Data（生データ）
- **users**: ユーザー情報（1,000件）
- **products**: 商品情報（100件）
- **orders**: 注文情報（5,000件）
- **order_items**: 注文詳細
- **access_logs**: アクセスログ（10,000件）

### Data Mart（分析用）
- **user_summary**: ユーザー集計データ
- **product_performance**: 商品パフォーマンス分析
- **daily_sales_summary**: 日次売上サマリー
- **user_behavior_analysis**: ユーザー行動分析

## 🚀 セットアップ手順

### 1. 前提条件

- Docker & Docker Compose
- Terraform（v1.0以上）
- Google Cloud Platform アカウント
- gcloud CLI のインストールと認証

### 2. GCP認証設定

```bash
# gcloud CLI で認証
gcloud auth login
gcloud auth application-default login

# プロジェクトの設定
gcloud config set project YOUR_PROJECT_ID
```

### 3. 環境変数の設定

```bash
# 環境変数ファイルの作成
cp env.example .env

# .env ファイルを編集して、あなたのGCPプロジェクト情報を設定
vi .env
```

### 4. Terraformでインフラ構築

```bash
# Terraformディレクトリに移動
cd terraform

# Terraform設定ファイルの作成
cp terraform.tfvars.example terraform.tfvars

# terraform.tfvars を編集して実際の値を設定
vi terraform.tfvars

# Terraformの初期化と実行
terraform init
terraform plan
terraform apply
```

### 5. Docker環境の起動

```bash
# プロジェクトルートに戻る
cd ..

# コンテナのビルドと起動
docker compose up -d

# BigQueryインポーターコンテナで作業
docker compose exec bigquery-importer bash
```

## 📋 実行手順

### Phase 1: BigQueryデータインポート処理

```bash
# BigQueryインポーターコンテナ内で実行
python main.py
```

このコマンドで以下が実行されます：
1. サンプルデータの生成
2. GCS バケットの作成とBigQuery データセットの確認
3. データファイルのGCSアップロード
4. BigQueryへのデータロード
5. データ検証

**注意**: BigQueryデータセットは事前にTerraformで作成されている必要があります。

### Phase 2: dbt によるデータ変換

```bash
# dbtコンテナで作業
docker compose exec dbt bash

# dbt の初期化と実行
dbt deps
dbt run
dbt test

# ドキュメント生成
dbt docs generate
dbt docs serve --port 8080
```

## 📈 作成されるデータマート

### 1. user_summary
ユーザーごとの購買行動サマリー
- 顧客セグメント（新規、リピーター、ロイヤル顧客）
- アクティビティステータス（アクティブ、休眠気味、休眠顧客）

### 2. product_performance
商品別のパフォーマンス分析
- 売上ランキング
- カテゴリ別順位
- パフォーマンス階層

### 3. daily_sales_summary
日次売上サマリーとトレンド分析
- 前日比較
- 7日移動平均
- 曜日別分析

### 4. user_behavior_analysis
ユーザーの行動分析
- コンバージョン率
- エンゲージメント指標
- 行動セグメント

## 📊 分析例

### 基本的なSQL分析

```sql
-- 月次売上トレンド
SELECT 
    FORMAT_DATE('%Y-%m', order_date) AS month,
    SUM(total_revenue) AS monthly_revenue,
    COUNT(DISTINCT order_date) AS active_days
FROM `your-project.ecommerce_data_mart.daily_sales_summary`
GROUP BY 1
ORDER BY 1;

-- 顧客セグメント分析
SELECT 
    customer_segment,
    COUNT(*) AS user_count,
    AVG(total_amount) AS avg_spent,
    AVG(total_orders) AS avg_orders
FROM `your-project.ecommerce_data_mart.user_summary`
GROUP BY 1;
```

### dbt モデルの依存関係

```
staging/
├── stg_users.sql
├── stg_products.sql
├── stg_orders.sql
├── stg_order_items.sql
└── stg_access_logs.sql

marts/
├── user_summary.sql
├── product_performance.sql
├── daily_sales_summary.sql
└── user_behavior_analysis.sql
```

## 🔄 拡張案

余裕があれば以下の機能を追加検討：

1. **Apache Airflow**: ワークフロー管理
2. **リアルタイム処理**: Pub/Sub + Cloud Functions


