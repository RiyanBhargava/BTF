from pymongo import MongoClient

MONGO_URI = "mongodb+srv://dbadmin:yuvaraj@btf-trials.qkcnwyo.mongodb.net/"
DB_NAME = "btf"
COLLECTION_NAME = "registrations"


client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

collection.insert_one(
    {
        "_id": 'btf001sch',
        "name": "John Doe",
        "email": "john@example.com",
        "qr_string": "to be generated",
        "qr_sent": False}
)