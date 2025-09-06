# dbt (data build tool) ディレクトリ

このディレクトリには、データ変換処理を行うdbtプロジェクトが含まれています。dbtは、SQL中心でデータパイプラインを構築する現代的なツールです。

## 📁 ファイル構成

```
dbt/
├── Dockerfile              # dbtコンテナの設定
├── dbt_project.yml         # dbtプロジェクト設定
├── profiles.yml            # BigQuery接続設定
├── models/
│   ├── staging/           # ステージング層（生データのクリーニング）
│   │   ├── sources.yml    # ソースデータ定義
│   │   ├── stg_users.sql
│   │   ├── stg_products.sql
│   │   ├── stg_orders.sql
│   │   ├── stg_order_items.sql
│   │   └── stg_access_logs.sql
│   └── marts/            # データマート層（ビジネス分析用）
│       ├── user_summary.sql
│       ├── product_performance.sql
│       ├── daily_sales_summary.sql
│       └── user_behavior_analysis.sql
└── README.md             # このファイル
```

## 🎯 dbtの役割

**dbt (data build tool)** は、データウェアハウス内でのデータ変換に特化したツールです：

- **SQLベース**: 慣れ親しんだSQLでデータ変換
- **モジュラー設計**: 再利用可能なデータモデル
- **テスト機能**: データ品質の自動チェック
- **ドキュメント生成**: 自動でデータ辞書を作成
- **依存関係管理**: モデル間の依存関係を自動解決

## 📊 データアーキテクチャ

### レイヤー構造
```
Raw Data (BigQuery)
    ↓
Staging Layer (dbt)  ← クリーニング・正規化
    ↓
Marts Layer (dbt)    ← ビジネス分析用の集計
    ↓
Analytics & BI       ← Jupyter、Looker Studio等
```

## 📋 各ファイルの詳細説明

### 1. `dbt_project.yml` - プロジェクト設定
```yaml
name: 'ecommerce_analytics'
profile: 'ecommerce_dbt'

models:
  ecommerce_analytics:
    staging:
      +materialized: view     # ステージングはビューとして作成
    marts:
      +materialized: table    # マートはテーブルとして作成
```

**役割**:
- dbtプロジェクトの基本設定
- モデルの物理化方法（view/table）の指定
- 変数・マクロの定義

### 2. `profiles.yml` - 接続設定
```yaml
ecommerce_dbt:
  outputs:
    dev:
      type: bigquery
      project: "{{ env_var('GCP_PROJECT_ID') }}"
      dataset: ecommerce_data_mart
      location: asia-northeast1
```

**役割**:
- BigQueryへの接続情報
- 環境別設定（dev/prod）
- 認証方法の指定

### 3. Staging Layer - データクリーニング

#### `sources.yml` - ソースデータ定義
```yaml
sources:
  - name: ecommerce_raw
    tables:
      - name: users
        columns:
          - name: user_id
            tests:
              - unique
              - not_null
```

**役割**:
- ETLで作成した生データテーブルの定義
- データ品質テスト（一意性、NULL値チェック等）
- ドキュメンテーション

#### `stg_users.sql` - ユーザーステージング
```sql
WITH source_data AS (
    SELECT
        user_id,
        name,
        email,
        age,
        gender,
        registration_date,
        city,
        prefecture,
        CURRENT_TIMESTAMP() AS loaded_at
    FROM {{ source('ecommerce_raw', 'users') }}
)

SELECT * FROM source_data
```

**役割**:
- 生データの基本的なクリーニング
- 一貫性のあるデータ形式への変換
- 監査用のタイムスタンプ追加

### 4. Marts Layer - ビジネス分析用データ

#### `user_summary.sql` - 顧客分析
```sql
WITH user_orders AS (
    SELECT
        u.user_id,
        u.name,
        COUNT(o.order_id) AS total_orders,
        SUM(o.total_amount) AS total_amount,
        AVG(o.total_amount) AS avg_order_value
    FROM {{ ref('stg_users') }} u
    LEFT JOIN {{ ref('stg_orders') }} o ON u.user_id = o.user_id
    GROUP BY 1, 2
)

SELECT
    *,
    CASE
        WHEN total_orders = 0 THEN '未購入'
        WHEN total_orders = 1 THEN '新規顧客'
        WHEN total_orders BETWEEN 2 AND 5 THEN 'リピーター'
        WHEN total_orders > 5 THEN 'ロイヤル顧客'
    END AS customer_segment
FROM user_orders
```

**役割**:
- 顧客の購買行動分析
- 顧客セグメンテーション
- LTV（顧客生涯価値）計算

#### `product_performance.sql` - 商品分析
```sql
WITH product_sales AS (
    SELECT
        p.product_id,
        p.name AS product_name,
        p.category,
        SUM(oi.quantity) AS total_quantity_sold,
        SUM(oi.line_total) AS total_revenue,
        COUNT(DISTINCT oi.order_id) AS total_orders
    FROM {{ ref('stg_products') }} p
    LEFT JOIN {{ ref('stg_order_items') }} oi ON p.product_id = oi.product_id
    GROUP BY 1, 2, 3
)

SELECT
    *,
    ROW_NUMBER() OVER (PARTITION BY category ORDER BY total_revenue DESC) 
        AS revenue_rank_in_category
FROM product_sales
```

**役割**:
- 商品別売上分析
- カテゴリ別パフォーマンス
- 在庫最適化のための洞察

#### `daily_sales_summary.sql` - 日次売上分析
```sql
WITH daily_metrics AS (
    SELECT
        DATE(o.order_date) AS order_date,
        COUNT(DISTINCT o.order_id) AS total_orders,
        COUNT(DISTINCT o.user_id) AS unique_customers,
        SUM(o.total_amount) AS total_revenue,
        AVG(o.total_amount) AS avg_order_value
    FROM {{ ref('stg_orders') }} o
    WHERE o.status = '完了'
    GROUP BY 1
)

SELECT
    *,
    AVG(total_revenue) OVER (
        ORDER BY order_date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS revenue_7day_avg
FROM daily_metrics
```

**役割**:
- 売上トレンド分析
- 季節性の把握
- ビジネスKPIの日次監視

#### `user_behavior_analysis.sql` - 行動分析
```sql
WITH user_web_activity AS (
    SELECT
        user_id,
        COUNT(*) AS total_page_views,
        COUNT(DISTINCT session_id) AS total_sessions,
        COUNT(CASE WHEN page_url = '/checkout' THEN 1 END) AS checkout_views
    FROM {{ ref('stg_access_logs') }}
    WHERE user_id IS NOT NULL
    GROUP BY 1
),

user_purchase_activity AS (
    SELECT
        user_id,
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(total_amount) AS total_spent
    FROM {{ ref('stg_orders') }}
    WHERE status = '完了'
    GROUP BY 1
)

SELECT
    w.user_id,
    w.total_page_views,
    w.total_sessions,
    p.total_orders,
    CASE 
        WHEN w.total_sessions > 0 THEN 
            ROUND(p.total_orders / w.total_sessions * 100, 2)
        ELSE 0
    END AS session_conversion_rate
FROM user_web_activity w
LEFT JOIN user_purchase_activity p ON w.user_id = p.user_id
```

**役割**:
- コンバージョン率分析
- ユーザージャーニー分析
- UX改善のための洞察

## 🚀 実行方法

### 基本的なdbt実行
```bash
# dbtコンテナに入る
docker compose exec dbt bash

# 依存関係のインストール（初回のみ）
dbt deps

# 全モデルの実行
dbt run

# 特定モデルの実行
dbt run --select user_summary

# テストの実行
dbt test

# ドキュメント生成
dbt docs generate
dbt docs serve --port 8080
```

### 段階別実行
```bash
# ステージング層のみ実行
dbt run --select staging

# マート層のみ実行
dbt run --select marts

# 特定のモデルとその依存関係
dbt run --select +user_summary

# 特定モデル以降のすべて
dbt run --select user_summary+
```

## 📊 実行結果

### 成功時の出力例
```
Running with dbt=1.7.4
Found 9 models, 8 tests, 0 snapshots, 0 analyses, 548 macros, 0 operations, 0 seed files, 1 source, 0 exposures, 0 metrics, 0 groups

Completed successfully

Done. PASS=9 WARN=0 ERROR=0 SKIP=0 TOTAL=9
```

### 作成されるテーブル・ビュー
```
BigQuery Dataset: ecommerce_data_mart
├── Views (Staging)
│   ├── stg_users
│   ├── stg_products  
│   ├── stg_orders
│   ├── stg_order_items
│   └── stg_access_logs
└── Tables (Marts)
    ├── user_summary
    ├── product_performance
    ├── daily_sales_summary
    └── user_behavior_analysis
```

## 🔧 技術的なポイント

### dbtの主要機能

#### 1. Jinja テンプレート
```sql
-- 再利用可能なマクロ
{% macro calculate_conversion_rate(numerator, denominator) %}
    CASE 
        WHEN {{ denominator }} > 0 THEN 
            ROUND({{ numerator }} / {{ denominator }} * 100, 2)
        ELSE 0
    END
{% endmacro %}

-- 条件分岐
{% if var('include_test_data') %}
    WHERE user_id NOT LIKE 'test_%'
{% endif %}
```

#### 2. ref() 関数
```sql
-- モデル間の参照（依存関係を自動管理）
FROM {{ ref('stg_users') }}
JOIN {{ ref('stg_orders') }} ON ...

-- ソースデータの参照
FROM {{ source('ecommerce_raw', 'users') }}
```

#### 3. データテスト
```sql
-- schema.ymlでテスト定義
tests:
  - unique
  - not_null
  - accepted_values:
      values: ['完了', '処理中', 'キャンセル', '返品']
  - relationships:
      to: ref('stg_users')
      field: user_id
```

### パフォーマンス最適化

#### 1. Materialization戦略
- **view**: 軽量、リアルタイム更新、ステージング向け
- **table**: 高速クエリ、バッチ更新、マート向け
- **incremental**: 大容量データの差分更新

#### 2. パーティショニング
```sql
{{ config(
    materialized='table',
    partition_by={
        'field': 'order_date',
        'data_type': 'date'
    }
) }}
```

## 🎓 学習ポイント

### dbtの概念
1. **Analytics Engineering**: データチームとビジネスチームの橋渡し
2. **Modeling**: ビジネスロジックをSQLで表現
3. **Testing**: データ品質の自動検証

### SQLスキル向上
1. **Window関数**: 移動平均、ランキング
2. **CTE**: 複雑なロジックの構造化
3. **集約関数**: 分析に必要な統計計算

### データモデリング
1. **Kimball手法**: ディメンション・ファクトテーブル設計
2. **正規化**: データの一貫性確保
3. **非正規化**: パフォーマンス重視の設計

## 🔍 トラブルシューティング

### よくある問題と解決方法

**1. dbt接続エラー**
```bash
# プロファイル確認
dbt debug

# 環境変数確認
echo $GCP_PROJECT_ID
```

**2. モデル実行エラー**
```bash
# 詳細ログ表示
dbt run --debug

# 特定モデルのSQL確認
dbt compile --select user_summary
```

**3. テスト失敗**
```bash
# 失敗詳細確認
dbt test --store-failures

# 失敗データの確認
SELECT * FROM dbt_test_failures.unique_stg_users_user_id
```

## 🎯 分析例

### 作成されるデータを使った分析例

#### 1. 顧客セグメント分析
```sql
SELECT 
    customer_segment,
    COUNT(*) as user_count,
    AVG(total_amount) as avg_spent,
    AVG(total_orders) as avg_orders
FROM ecommerce_data_mart.user_summary
GROUP BY customer_segment
ORDER BY avg_spent DESC;
```

#### 2. 商品カテゴリ売上分析
```sql
SELECT 
    category,
    SUM(total_revenue) as category_revenue,
    COUNT(*) as product_count,
    AVG(total_revenue) as avg_product_revenue
FROM ecommerce_data_mart.product_performance
GROUP BY category
ORDER BY category_revenue DESC;
```

#### 3. 月次売上トレンド
```sql
SELECT 
    FORMAT_DATE('%Y-%m', order_date) as month,
    SUM(total_revenue) as monthly_revenue,
    AVG(total_revenue) as avg_daily_revenue
FROM ecommerce_data_mart.daily_sales_summary
GROUP BY month
ORDER BY month;
```

## 🎯 次のステップ

dbtモデルが成功したら：
1. **Jupyter分析**: 作成されたデータマートを使用した高度な分析
2. **ダッシュボード**: Looker StudioでのKPI可視化
3. **拡張**: 追加のビジネスメトリクス作成

dbtにより、生データが分析可能なビジネスインサイトに変換され、意思決定に活用できるデータ基盤が完成します。
