from pymongo import MongoClient
import os

# Connect to the database
database = os.getenv("DB_NAME")
username = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
db_host = os.getenv("DB_HOST")
# client = MongoClient(f"mongodb://{db_host}/{database}")
client = MongoClient(f"mongodb://{username}:{password}@{db_host}/{database}?authSource=admin&authMechanism=SCRAM-SHA-256")
db = client[database]
