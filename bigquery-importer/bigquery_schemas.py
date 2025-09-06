from google.cloud import bigquery


class BigQuerySchemas:
    """BigQueryテーブルのスキーマ定義を管理するクラス"""

    @staticmethod
    def get_schemas():
        """BigQueryテーブルのスキーマ定義を返す"""
        schemas = {
            'users': [
                bigquery.SchemaField("user_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("email", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("age", "INTEGER", mode="NULLABLE"),
                bigquery.SchemaField("gender", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("registration_date",
                                     "DATE", mode="NULLABLE"),
                bigquery.SchemaField("city", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("prefecture", "STRING", mode="NULLABLE"),
            ],
            'products': [
                bigquery.SchemaField("product_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("category", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("price", "INTEGER", mode="NULLABLE"),
                bigquery.SchemaField("created_date", "DATE", mode="NULLABLE"),
                bigquery.SchemaField("brand", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("rating", "FLOAT", mode="NULLABLE"),
            ],
            'orders': [
                bigquery.SchemaField("order_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("user_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField(
                    "order_date", "TIMESTAMP", mode="NULLABLE"),
                bigquery.SchemaField(
                    "total_amount", "INTEGER", mode="NULLABLE"),
                bigquery.SchemaField("status", "STRING", mode="NULLABLE"),
                bigquery.SchemaField(
                    "payment_method", "STRING", mode="NULLABLE"),
            ],
            'order_items': [
                bigquery.SchemaField(
                    "order_item_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("order_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("product_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("quantity", "INTEGER", mode="NULLABLE"),
                bigquery.SchemaField("unit_price", "INTEGER", mode="NULLABLE"),
            ],
            'access_logs': [
                bigquery.SchemaField(
                    "timestamp", "TIMESTAMP", mode="NULLABLE"),
                bigquery.SchemaField("user_id", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("page_url", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("session_id", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("user_agent", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("ip_address", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("referrer", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("device_type", "STRING", mode="NULLABLE"),
            ]
        }
        return schemas

    @staticmethod
    def get_schema_for_table(table_name):
        """特定のテーブルのスキーマを取得"""
        schemas = BigQuerySchemas.get_schemas()
        return schemas.get(table_name)

    @staticmethod
    def get_available_tables():
        """利用可能なテーブル名のリストを取得"""
        return list(BigQuerySchemas.get_schemas().keys())
