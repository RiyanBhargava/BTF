from pymongo import MongoClient
from bson.objectid import ObjectId

MONGO_URI = "mongodb+srv://dbadmin:yuvaraj@btf-trials.qkcnwyo.mongodb.net/"
DB_NAME = "btf"
COLLECTION_NAME = "registrations"
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collectiondb = db[COLLECTION_NAME]
#print(collection)
collection = collectiondb.find()  

for user in collection:
    collection.update_one(
            {"name": user['name']},
            {"$set": {"_id":'btf000sch'}}
        )
    
for user in collection:
    print(user)
    