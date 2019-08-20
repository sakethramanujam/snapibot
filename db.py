from pymongo import MongoClient
import os

# Connect to the database
database = os.getenv("DB_NAME")
db_host = os.getenv("DB_HOST")
client = MongoClient(f"{db_host}")
db = client[database]
