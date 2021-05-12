import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

# root path
ROOT_PATH = os.getenv('ROOT_PATH')

# crawling
CRAWLING_QUERY = os.getenv('CRAWLING_QUERY')
CRAWLING_LIMIT = os.getenv('CRAWLING_LIMIT')

# DB
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = os.getenv('DB_PORT')
