import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def get_db():
    client = MongoClient(os.getenv("MONGO_URI"))
    return client[os.getenv("DB_NAME")]

def get_unprocessed_users():
    db = get_db()
    return db.registrations.find({ "qr_sent": False , "registrationId": {"$exists": True}})

def bulk_write(operations):
    db = get_db()
    result = db.registrations.bulk_write(operations)
    print(f"Bulk write completed: {result.bulk_api_result}")