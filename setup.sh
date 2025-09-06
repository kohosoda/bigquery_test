#!/bin/bash

# データエンジニアリングプロジェクトのセットアップスクリプト

echo "🚀 データエンジニアリング学習プロジェクトのセットアップを開始します..."

# 1. 環境変数ファイルの確認
if [ ! -f ".env" ]; then
    echo "📝 環境変数ファイルを作成しています..."
    cp env.example .env
    echo "⚠️  .env ファイルを編集して、あなたのGCPプロジェクト情報を設定してください"
    echo "   必要な設定項目："
    echo "   - GCP_PROJECT_ID: あなたのGCPプロジェクトID"
    echo "   - GCS_BUCKET_NAME: 使用するGCSバケット名（ユニークな名前）"
    echo ""
    read -p "設定が完了したらEnterキーを押してください..."
fi

# 2. GCP認証の確認
echo "🔐 GCP認証を確認しています..."
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ GCP認証が必要です。以下のコマンドを実行してください："
    echo "   gcloud auth login"
    echo "   gcloud auth application-default login"
    exit 1
else
    echo "✅ GCP認証が確認できました"
fi

# 3. Dockerの確認
echo "🐳 Docker環境を確認しています..."
if ! command -v docker &> /dev/null; then
    echo "❌ Dockerがインストールされていません"
    exit 1
fi

if ! docker compose version &> /dev/null; then
    echo "❌ docker compose がインストールされていません"
    echo "   最新の Docker では 'docker compose' コマンドを使用します。"
    exit 1
fi

echo "✅ Docker環境が確認できました"

# 4. Dockerイメージのビルド
echo "🔨 Dockerイメージをビルドしています..."
docker compose build

if [ $? -eq 0 ]; then
    echo "✅ Dockerイメージのビルドが完了しました"
else
    echo "❌ Dockerイメージのビルドに失敗しました"
    exit 1
fi

# 5. コンテナの起動
echo "🚀 コンテナを起動しています..."
docker compose up -d

if [ $? -eq 0 ]; then
    echo "✅ コンテナの起動が完了しました"
else
    echo "❌ コンテナの起動に失敗しました"
    exit 1
fi

# 6. セットアップ完了メッセージ
echo ""
echo "🎉 セットアップが完了しました！"
echo ""
echo "次のステップ："
echo "1. BigQueryインポート処理の実行:"
echo "   docker compose exec bigquery-importer python main.py"
echo ""
echo "2. dbtでのデータ変換:"
echo "   docker compose exec dbt dbt run"
echo ""
echo "3. Jupyter Notebookでの分析:"
echo "   ブラウザで http://localhost:8888 にアクセス"
echo ""
echo "詳細な手順はREADME.mdを確認してください。"
