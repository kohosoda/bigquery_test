import os
from dotenv import load_dotenv

load_dotenv()

# GCP Configuration
GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID', 'your-project-id')
GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME', 'your-bucket-name')
BIGQUERY_DATASET = os.getenv('BIGQUERY_DATASET', 'ecommerce_data')

# Data Configuration
DATA_DIR = '/app/data'
RAW_DATA_DIR = f'{DATA_DIR}/raw'
PROCESSED_DATA_DIR = f'{DATA_DIR}/processed'

# Sample Data Configuration
NUM_USERS = 1000
NUM_PRODUCTS = 100
NUM_ORDERS = 5000
NUM_ACCESS_LOGS = 10000

# Date Range for Sample Data
START_DATE = '2023-01-01'
END_DATE = '2024-01-31'



