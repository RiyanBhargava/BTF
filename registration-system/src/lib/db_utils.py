import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def get_db():
    """Get MongoDB client and database connection"""
    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("DB_NAME")
    
    if not mongo_uri:
        raise ValueError("MONGO_URI environment variable is not set")
    if not db_name:
        raise ValueError("DB_NAME environment variable is not set")
    
    try:
        client = MongoClient(mongo_uri)
        # Test connection
        client.admin.command('ping')
        return client[db_name]
    except Exception as e:
        raise ConnectionError(f"Failed to connect to MongoDB: {str(e)}")

def get_unprocessed_users():
    """Get all users that haven't been processed yet"""
    try:
        db = get_db()
        cursor = db.registrations.find({
            "qr_sent": False,
            "registrationId": {"$exists": True}
        })
        
        # Convert cursor to list to avoid cursor timeout issues
        users = list(cursor)
        print(f"Found {len(users)} unprocessed users")
        return users
    except Exception as e:
        print(f"Error getting unprocessed users: {str(e)}")
        raise

def bulk_write(operations):
    """Perform bulk write operations to the database"""
    if not operations:
        print("No operations to perform")
        return None
        
    try:
        db = get_db()
        result = db.registrations.bulk_write(operations)
        return result.bulk_api_result
    except Exception as e:
        print(f"Error during bulk write: {str(e)}")
        raise