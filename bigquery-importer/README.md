# BigQuery Importer ディレクトリ

このディレクトリには、BigQueryへのデータインポート処理を行うPythonスクリプトが含まれています。

## 📁 ファイル構成

```
bigquery-importer/
├── Dockerfile          # BigQueryインポーターコンテナの設定
├── requirements.txt    # Python依存パッケージ
├── config.py          # 設定管理
├── data_generator.py  # サンプルデータ生成
├── bigquery_client.py # BigQuery操作クライアント
├── gcs_client.py      # GCS操作クライアント
├── bigquery_schemas.py # BigQueryスキーマ定義
├── main.py           # メインインポート処理
├── upload_only.py    # GCSアップロード専用スクリプト
└── README.md         # このファイル
```

## 🎯 BigQuery Importerの役割

**BigQuery Importer**は、データをBigQueryに効率的にインポートするためのツールです：
- **データ生成**: サンプルデータの生成
- **GCS アップロード**: データファイルをCloud Storageにアップロード
- **BigQuery ロード**: GCSからBigQueryにデータをインポート

## 📋 各ファイルの詳細説明

### 1. `config.py` - 設定管理
```python
# 設定を一元管理
GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID', 'your-project-id')
GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME', 'your-bucket-name')
NUM_USERS = 1000  # 生成するユーザー数
```

**役割**:
- 環境変数の読み込み
- データ生成パラメータの管理
- GCP接続情報の一元管理

### 2. `data_generator.py` - サンプルデータ生成
```python
class SampleDataGenerator:
    def generate_users(self):      # ユーザーデータ生成
    def generate_products(self):   # 商品データ生成
    def generate_orders(self):     # 注文データ生成
    def generate_access_logs(self): # アクセスログ生成
```

**役割**:
- **リアルなECサイトデータを生成**
- Fakerライブラリで日本語データ作成
- CSVとJSONファイルとして出力

**生成データ**:
- **users.csv**: 1,000人のユーザー情報（名前、年齢、住所等）
- **products.csv**: 100商品の情報（商品名、価格、カテゴリ等）
- **orders.csv**: 5,000件の注文情報
- **order_items.csv**: 注文詳細（約15,000件）
- **access_logs.json**: 10,000件のWebアクセスログ

### 3. `gcp_client.py` - GCP操作クライアント
```python
class GCPClient:
    def setup_gcs_bucket(self):        # GCSバケット作成
    def setup_bigquery_dataset(self):  # BigQueryデータセット作成
    def upload_to_gcs(self):          # ファイルアップロード
    def upload_csv_to_bigquery(self):  # CSVロード
    def upload_json_to_bigquery(self): # JSONロード
```

**役割**:
- **Google Cloud Storage**: ファイル保存
- **BigQuery**: データウェアハウスへのロード
- **自動インフラ作成**: バケット・データセットの自動作成
- **エラーハンドリング**: 堅牢な例外処理

### 4. `main.py` - メインインポート処理
```python
def main():
    # Step 1: サンプルデータの生成
    # Step 2: GCP環境のセットアップ  
    # Step 3: データファイルのGCSアップロード
    # Step 4: BigQueryへのデータロード
    # Step 5: データ検証
```

**処理フロー**:
1. **データ生成**: ローカルでサンプルデータ作成
2. **GCP準備**: バケット・データセット自動作成
3. **ファイル転送**: GCSにデータアップロード
4. **データロード**: BigQueryにテーブル作成・データロード
5. **検証**: 正しくロードされたかチェック

## 🚀 実行方法

### 基本的な実行
```bash
# BigQueryインポーターコンテナ内で実行
docker compose exec bigquery-importer python main.py
```

### 個別スクリプト実行
```bash
# データ生成のみ
docker compose exec bigquery-importer python -c "
from data_generator import SampleDataGenerator
generator = SampleDataGenerator()
generator.generate_all_data()
"

# GCP接続テスト
docker compose exec bigquery-importer python -c "
from bigquery_client import BigQueryClient
from gcs_client import GCSClient
bigquery_client = BigQueryClient()
gcs_client = GCSClient()
gcs_client.setup_gcs_bucket()
bigquery_client.setup_bigquery_dataset()
"
```

## 📊 実行結果

### 成功時の出力例
```
=== BigQuery Data Import Pipeline ===

Step 1: Generating sample data...
✅ Sample data generation completed

Step 2: Setting up GCP environment...
Creating new bucket: your-bucket-name
Creating new dataset: ecommerce_data
✅ GCP environment setup completed

Step 3: Uploading files to Google Cloud Storage...
✅ Files uploaded to GCS

Step 4: Loading data to BigQuery...
Loaded 1000 rows to project.ecommerce_data.users
Loaded 100 rows to project.ecommerce_data.products
Loaded 5000 rows to project.ecommerce_data.orders
Loaded 14930 rows to project.ecommerce_data.order_items
Loaded 10000 rows to project.ecommerce_data.access_logs
✅ Data loaded to BigQuery

Step 5: Validating loaded data...
✅ Data validation completed

🎉 BigQuery Import Pipeline completed successfully!
```

## 🔧 技術的なポイント

### データモデル設計
- **正規化**: users, products, ordersの関係を適切に設計
- **リアルなデータ**: Fakerで実際のビジネスに近いデータ生成
- **スキーマ定義**: BigQueryの型に最適化

### エラーハンドリング
```python
try:
    gcp_client.setup_gcs_bucket()
    print("✅ GCS setup completed")
except Exception as e:
    print(f"❌ GCS setup failed: {e}")
    return False
```

### パフォーマンス最適化
- **バッチ処理**: 大量データの効率的な処理
- **スキーマ指定**: BigQueryロード時の型指定で高速化
- **並列処理**: 複数ファイルの同時アップロード

## 🎓 学習ポイント

### データエンジニアリング基礎
1. **データインポートパイプライン設計**: データの流れを設計
2. **データ品質管理**: バリデーション・エラーハンドリング
3. **クラウド連携**: GCP APIの活用

### Python技術
1. **オブジェクト指向**: クラス設計とメソッド分割
2. **外部ライブラリ**: pandas, google-cloud-*の活用
3. **設定管理**: 環境変数・設定ファイルの管理

### 実務スキル
1. **インフラ自動化**: 必要なリソースの自動作成
2. **ログ出力**: 処理状況の可視化
3. **エラー対応**: 問題の特定と解決

## 🔍 トラブルシューティング

### よくある問題と解決方法

**1. GCP認証エラー**
```bash
# 解決方法
gcloud auth login
gcloud auth application-default login
```

**2. 権限エラー**
- BigQuery Admin または BigQuery User ロールが必要
- Storage Admin または Storage Object Admin ロールが必要

**3. CSV形式エラー**
- data_generator.pyでカラム順序を確認
- BigQueryスキーマとの一致を確認

**4. 環境変数未設定**
```bash
# .envファイルの確認
cat .env

# コンテナ再起動
docker compose down && docker compose up -d
```

## 🎯 次のステップ

BigQueryインポートが成功したら、次はdbtでのデータ変換に進みます：
1. **dbtモデル実行**: ステージング→データマート変換
2. **データ品質テスト**: dbtテストの実行

このBigQueryインポート処理により、分析可能な状態でデータがBigQueryに格納され、本格的なデータ分析の基盤が完成します。
