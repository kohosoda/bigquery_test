# データエンジニアリング学習プロジェクト - 構成・実装方針

## プロジェクト概要

ローカルDockerとGCP BigQueryを活用した最小構成でのデータ基盤構築を目指す。

### 目標
- BigQueryへのデータインポート処理の実装
- dbtを使ったデータ変換処理の体験
- BigQueryを活用したデータ分析基盤の構築

## システム構成

### 全体アーキテクチャ

```
[データ生成] → [ローカルDocker] → [GCS] → [BigQuery] → [レポート/ダッシュボード]
     ↓              ↓              ↓         ↓              ↓
サンプルデータ  データインポート  データレイク   DWH      可視化・分析
  (Python)    (Python/dbt)   (JSON/CSV)  (SQL/dbt)   (Looker Studio)
```

### 詳細構成

#### 1. データソース層
- **サンプルデータ**: ECサイトの模擬データ
  - ユーザー情報（users.csv）
  - 商品情報（products.csv）
  - 注文情報（orders.csv）
  - 注文詳細（order_items.csv）
  - アクセスログ（access_logs.json）

#### 2. データ収集・処理層（ローカルDocker）
- **Python BigQueryインポーターコンテナ**
  - データ生成スクリプト
  - データ前処理・クレンジング
  - GCSへのアップロード
  - BigQueryへのロード
- **dbtコンテナ**
  - データ変換処理
  - BigQuery上でのSQLベース変換
  - データマート作成

#### 3. データストレージ層（GCP）
- **Google Cloud Storage**
  - Raw Data Store（生データ）
  - Processed Data Store（処理済みデータ）
- **BigQuery**
  - Data Warehouse
  - データマート

#### 4. 可視化層
- **Looker Studio**（無料）
  - ダッシュボード作成
  - レポート出力

## 技術スタック詳細

### コア技術
- **言語**: Python 3.11
- **コンテナ**: Docker Compose
- **DWH**: BigQuery
- **ストレージ**: Google Cloud Storage
- **データ変換**: dbt-bigquery

### Pythonライブラリ
```
pandas          # データ操作
faker           # サンプルデータ生成
google-cloud-storage  # GCS操作
google-cloud-bigquery # BigQuery操作
streamlit       # 簡易ダッシュボード（オプション）
```

### Docker構成
```
services:
  bigquery-importer:
    # Pythonベースのデータインポート処理
  dbt:
    # dbtでのデータ変換
```

## データモデル設計

### 1. Raw Data（生データ）
```sql
-- users テーブル
user_id, name, email, age, gender, registration_date, city

-- products テーブル  
product_id, name, category, price, created_date

-- orders テーブル
order_id, user_id, order_date, total_amount, status

-- order_items テーブル
order_item_id, order_id, product_id, quantity, unit_price

-- access_logs テーブル（JSON）
timestamp, user_id, page_url, session_id, user_agent, ip_address
```

### 2. Data Mart（分析用）
```sql
-- user_summary
user_id, total_orders, total_amount, avg_order_value, last_order_date

-- product_performance  
product_id, total_sales, total_quantity, avg_price, category

-- daily_sales_summary
date, total_orders, total_revenue, unique_users, avg_order_value

-- user_behavior_analysis
user_id, page_views, session_count, conversion_rate
```

