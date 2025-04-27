# Registration System
from lib.db_utils import get_unprocessed_users
from lib.email_utils import send_qr_email
from lib.db_utils import bulk_write
from lib.qr_utils import prepare_qr_update_operation
from dotenv import load_dotenv
import os
import sys
import traceback

load_dotenv()

def main():
    """Main function to process registrations, generate QR codes, and send emails"""
    print("\n====================================")
    print("   BITS Tech Fest Registration System   ")
    print("====================================\n")
    
    print("Starting QR code generation and email sending process...")
    
    try:
        # Verify required environment variables
        required_vars = ["MONGO_URI", "DB_NAME", "EMAIL_USER", "EMAIL_PASSWORD"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            print(f"ERROR: Missing required environment variables: {', '.join(missing_vars)}")
            print("Please update your .env file with the required variables.")
            sys.exit(1)
            
        # Get unprocessed users
        users = get_unprocessed_users()
        bulk_ops = []
        
        success_count = 0
        failure_count = 0
        
        for user in users:
            try:
                # Generate QR and send email
                qr_data = send_qr_email(user)
                
                # Prepare database update operation
                op = prepare_qr_update_operation(user, qr_data)
                bulk_ops.append(op)
                
                print(f"✅ Processed user: {user['email']} ({user['registrationId']})")
                success_count += 1
                
            except Exception as e:
                print(f"❌ Failed {user.get('email', 'Unknown email')}: {str(e)}")
                failure_count += 1
        
        # Bulk update in MongoDB
        if bulk_ops:
            try:
                result = bulk_write(bulk_ops)
                print(f"\nUpdated {len(bulk_ops)} users with QR codes in database")
            except Exception as e:
                print(f"\nERROR: Failed to update database: {str(e)}")
                print("QR codes were generated and emails were sent, but database was not updated.")
                
        else:
            print("\nNo users to process")
            
        # Summary
        print("\n--- Summary ---")
        print(f"Total users processed: {success_count + failure_count}")
        print(f"Successful: {success_count}")
        print(f"Failed: {failure_count}")
        
    except Exception as e:
        print(f"\nCritical error: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
