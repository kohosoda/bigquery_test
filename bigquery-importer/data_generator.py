import pandas as pd
import json
from faker import Faker
from datetime import datetime, timedelta
import random
import os
from config import *

fake = Faker('ja_JP')  # 日本のデータを生成
Faker.seed(42)  # 再現可能性のためのシード値設定

class SampleDataGenerator:
    def __init__(self):
        self.users_df = None
        self.products_df = None
        self.orders_df = None
        self.order_items_df = None
        self.access_logs = []
        
        # データディレクトリの作成
        os.makedirs(RAW_DATA_DIR, exist_ok=True)
        os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    
    def generate_users(self):
        """ユーザーデータの生成"""
        print("Generating users data...")
        
        users_data = []
        for i in range(NUM_USERS):
            user = {
                'user_id': f'user_{i+1:06d}',
                'name': fake.name(),
                'email': fake.email(),
                'age': random.randint(18, 80),
                'gender': random.choice(['男性', '女性', 'その他']),
                'registration_date': fake.date_between(
                    start_date=datetime.strptime(START_DATE, '%Y-%m-%d'),
                    end_date=datetime.strptime(END_DATE, '%Y-%m-%d')
                ),
                'city': fake.city(),
                'prefecture': fake.prefecture()
            }
            users_data.append(user)
        
        self.users_df = pd.DataFrame(users_data)
        return self.users_df
    
    def generate_products(self):
        """商品データの生成"""
        print("Generating products data...")
        
        categories = ['エレクトロニクス', 'ファッション', '本・雑誌', 'ホーム&キッチン', 
                     'スポーツ・アウトドア', '美容・健康', 'おもちゃ・ゲーム', '食品・飲料']
        
        products_data = []
        for i in range(NUM_PRODUCTS):
            category = random.choice(categories)
            product = {
                'product_id': f'prod_{i+1:06d}',
                'name': self._generate_product_name(category),
                'category': category,
                'price': random.randint(500, 50000),
                'created_date': fake.date_between(
                    start_date=datetime.strptime(START_DATE, '%Y-%m-%d'),
                    end_date=datetime.strptime(END_DATE, '%Y-%m-%d')
                ),
                'brand': fake.company(),
                'rating': round(random.uniform(3.0, 5.0), 1)
            }
            products_data.append(product)
        
        self.products_df = pd.DataFrame(products_data)
        return self.products_df
    
    def _generate_product_name(self, category):
        """カテゴリに応じた商品名の生成"""
        product_names = {
            'エレクトロニクス': ['スマートフォン', 'ノートPC', 'タブレット', 'イヤホン', 'デジタルカメラ'],
            'ファッション': ['Tシャツ', 'ジーンズ', 'スニーカー', 'バッグ', 'アクセサリー'],
            '本・雑誌': ['小説', '技術書', '雑誌', 'マンガ', '実用書'],
            'ホーム&キッチン': ['調理器具', '食器', '掃除用品', 'インテリア', '家電'],
            'スポーツ・アウトドア': ['ランニングシューズ', 'トレーニングウェア', 'アウトドアグッズ', 'スポーツ用品'],
            '美容・健康': ['化粧品', 'スキンケア', 'サプリメント', 'ヘアケア'],
            'おもちゃ・ゲーム': ['ボードゲーム', 'おもちゃ', 'パズル', 'ゲーム'],
            '食品・飲料': ['お茶', 'コーヒー', 'お菓子', '調味料', '冷凍食品']
        }
        base_name = random.choice(product_names[category])
        return f"{fake.company()} {base_name} {random.choice(['プレミアム', 'スタンダード', 'ライト', 'プロ'])}"
    
    def generate_orders(self):
        """注文データの生成"""
        print("Generating orders data...")
        
        if self.users_df is None:
            raise ValueError("Users data must be generated first")
        
        orders_data = []
        order_items_data = []
        
        for i in range(NUM_ORDERS):
            user_id = random.choice(self.users_df['user_id'].tolist())
            order_date = fake.date_time_between(
                start_date=datetime.strptime(START_DATE, '%Y-%m-%d'),
                end_date=datetime.strptime(END_DATE, '%Y-%m-%d')
            )
            
            order = {
                'order_id': f'order_{i+1:08d}',
                'user_id': user_id,
                'order_date': order_date,
                'total_amount': 0,  # 後で計算
                'status': random.choice(['完了', '処理中', 'キャンセル', '返品']),
                'payment_method': random.choice(['クレジットカード', '銀行振込', 'コンビニ決済', '代金引換'])
            }
            
            # 注文アイテムの生成（1-5個のアイテム）
            num_items = random.randint(1, 5)
            total_amount = 0
            
            for j in range(num_items):
                product = self.products_df.sample(1).iloc[0]
                quantity = random.randint(1, 3)
                unit_price = product['price']
                
                order_item = {
                    'order_item_id': f'item_{i+1:08d}_{j+1:02d}',
                    'order_id': order['order_id'],
                    'product_id': product['product_id'],
                    'quantity': quantity,
                    'unit_price': unit_price
                }
                order_items_data.append(order_item)
                total_amount += unit_price * quantity
            
            order['total_amount'] = total_amount
            orders_data.append(order)
        
        self.orders_df = pd.DataFrame(orders_data)
        self.order_items_df = pd.DataFrame(order_items_data)
        
        return self.orders_df, self.order_items_df
    
    def generate_access_logs(self):
        """アクセスログデータの生成"""
        print("Generating access logs data...")
        
        if self.users_df is None:
            raise ValueError("Users data must be generated first")
        
        pages = [
            '/home', '/products', '/product/{product_id}', '/cart', 
            '/checkout', '/user/profile', '/search', '/category/{category}',
            '/login', '/register', '/about', '/contact'
        ]
        
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X)',
            'Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/88.0'
        ]
        
        access_logs_data = []
        
        for i in range(NUM_ACCESS_LOGS):
            user_id = random.choice(self.users_df['user_id'].tolist()) if random.random() > 0.1 else None
            timestamp = fake.date_time_between(
                start_date=datetime.strptime(START_DATE, '%Y-%m-%d'),
                end_date=datetime.strptime(END_DATE, '%Y-%m-%d')
            )
            
            page_url = random.choice(pages)
            if '{product_id}' in page_url:
                page_url = page_url.replace('{product_id}', random.choice(self.products_df['product_id'].tolist()))
            elif '{category}' in page_url:
                page_url = page_url.replace('{category}', random.choice(self.products_df['category'].unique()))
            
            log = {
                'timestamp': timestamp.isoformat(),
                'user_id': user_id,
                'page_url': page_url,
                'session_id': fake.uuid4(),
                'user_agent': random.choice(user_agents),
                'ip_address': fake.ipv4(),
                'referrer': random.choice([None, 'https://google.com', 'https://yahoo.co.jp', 'direct']),
                'device_type': random.choice(['desktop', 'mobile', 'tablet'])
            }
            access_logs_data.append(log)
        
        self.access_logs = access_logs_data
        return access_logs_data
    
    def save_to_files(self):
        """データをファイルに保存"""
        print("Saving data to files...")
        
        # CSV ファイルとして保存
        if self.users_df is not None:
            self.users_df.to_csv(f'{RAW_DATA_DIR}/users.csv', index=False, encoding='utf-8')
            print(f"Saved users data: {len(self.users_df)} records")
        
        if self.products_df is not None:
            self.products_df.to_csv(f'{RAW_DATA_DIR}/products.csv', index=False, encoding='utf-8')
            print(f"Saved products data: {len(self.products_df)} records")
        
        if self.orders_df is not None:
            self.orders_df.to_csv(f'{RAW_DATA_DIR}/orders.csv', index=False, encoding='utf-8')
            print(f"Saved orders data: {len(self.orders_df)} records")
        
        if self.order_items_df is not None:
            self.order_items_df.to_csv(f'{RAW_DATA_DIR}/order_items.csv', index=False, encoding='utf-8')
            print(f"Saved order items data: {len(self.order_items_df)} records")
        
        # JSON ファイルとして保存（アクセスログ）
        if self.access_logs:
            with open(f'{RAW_DATA_DIR}/access_logs.json', 'w', encoding='utf-8') as f:
                for log in self.access_logs:
                    f.write(json.dumps(log, ensure_ascii=False) + '\n')
            print(f"Saved access logs: {len(self.access_logs)} records")
    
    def generate_all_data(self):
        """全てのサンプルデータを生成"""
        print("Starting sample data generation...")
        
        self.generate_users()
        self.generate_products()
        self.generate_orders()
        self.generate_access_logs()
        self.save_to_files()
        
        print("\nData generation completed!")
        print(f"Users: {len(self.users_df)}")
        print(f"Products: {len(self.products_df)}")
        print(f"Orders: {len(self.orders_df)}")
        print(f"Order Items: {len(self.order_items_df)}")
        print(f"Access Logs: {len(self.access_logs)}")

if __name__ == "__main__":
    generator = SampleDataGenerator()
    generator.generate_all_data()
