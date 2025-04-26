# Registration System
from lib.db_utils import get_unprocessed_users
from lib.email_utils import send_qr_email
from lib.db_utils import bulk_write 
from pymongo import UpdateOne

def main():
    db = get_unprocessed_users()
    bulk_ops = []
    
    for user in db:
        try:
            send_qr_email(user)
            bulk_ops.append(
                UpdateOne(
                    {"_id": user["_id"]},
                    {"$set": {"qr_sent": True}}
                )
            )
        except Exception as e:
            print(f"Failed {user['email']}: {str(e)}")
    
    # Bulk update in MongoDB
    if bulk_ops:
        bulk_write(bulk_ops)

if __name__ == "__main__":
    main()
