from pymongo import MongoClient
from bson.objectid import ObjectId

MONGO_URI = "mongodb+srv://dbadmin:yuvaraj@btf-trials.qkcnwyo.mongodb.net/"
DB_NAME = "btf"
COLLECTION_NAME = "registrations"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]
#print(collection)

for user in collection.find({"_id": 'btf001sch'}):
    collection.update_one(
            {"_id": user['_id']},
            {"$set": {"qr_sent": True}}
        )
    
for user in collection.find():
    print(user)

    
