
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()


def connect_db():
    connection_url = os.getenv("CONNECTION_URL")
    connection_database = os.getenv("CONNECTION_DATABASE")

    client = MongoClient(connection_url)
    db = client[connection_database]
    return db
