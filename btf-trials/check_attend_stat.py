from pymongo import MongoClient
import pandas as pd

MONGO_URI = "mongodb+srv://dbadmin:yuvaraj@btf-trials.qkcnwyo.mongodb.net/"
DB_NAME = "btf"
COLLECTION_NAME = "attendance"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

data = list(collection.find())

if data:
    df = pd.DataFrame(data)
    print(df)
else:
    print("No data found in the collection.")
