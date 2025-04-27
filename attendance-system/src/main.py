# Attendance System - Main Script
from lib.scanner_utils import scan_qr
from lib.csv_handler import register_attendance, handle_spot_registration
from lib.auth_utils import authenticate_club
from dotenv import load_dotenv
import os
import sys
import traceback

load_dotenv()

def main():
    """Main function to run the attendance system"""
    print("\n====================================")
    print("   BITS Tech Fest Attendance System   ")
    print("====================================\n")
    
    try:
        # Verify required environment variables
        required_vars = ["MONGO_URI", "DB_NAME"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            print(f"ERROR: Missing required environment variables: {', '.join(missing_vars)}")
            print("Please update your .env file with the required variables.")
            sys.exit(1)
            
        # Authenticate club and get event
        print("Starting club authentication...")
        club_data = authenticate_club()
        if not club_data:
            print("Authentication failed. Exiting.")
            sys.exit(1)
        
        event_name = club_data["event_name"]
        club_name = club_data["club_name"]
        
        print(f"\n📋 Taking attendance for: {event_name}")
        print(f"📋 Club: {club_name}")
        print("------------------------------------")
        print("Press 's' for spot registration during scanning")
        print("Press 'q' to quit the scanner")
        print("------------------------------------\n")
        
        # Set the event name environment variable for backward compatibility
        os.environ["EVENT_NAME"] = event_name
        
        # Track statistics
        registrations = {
            "total": 0,
            "pre_registered": 0,
            "spot_registered": 0,
            "failed": 0
        }
        
        # Scan QR codes
        try:
            for reg_id in scan_qr():
                if reg_id.lower() == 's':
                    # Handle spot registration
                    print("\nProcessing on-spot registration...")
                    try:
                        spot_reg_id, user_data = handle_spot_registration()
                        success = register_attendance(event_name, spot_reg_id, user_data, is_spot_registration=True)
                        
                        if success:
                            registrations["total"] += 1
                            registrations["spot_registered"] += 1
                    except Exception as e:
                        print(f"Error during spot registration: {str(e)}")
                        registrations["failed"] += 1
                        
                elif reg_id.lower() == 'q':
                    print("\nExiting attendance system by user request.")
                    break
                else:
                    # Regular attendance
                    print(f"\nProcessing registration ID: {reg_id}")
                    try:
                        success = register_attendance(event_name, reg_id)
                        
                        if success:
                            registrations["total"] += 1
                            registrations["pre_registered"] += 1
                    except Exception as e:
                        print(f"Error processing registration: {str(e)}")
                        registrations["failed"] += 1
            
        except KeyboardInterrupt:
            print("\nExiting attendance system (Keyboard Interrupt).")
        
        # Display summary
        print("\n--- Attendance Summary ---")
        print(f"Event: {event_name}")
        print(f"Total registrations processed: {registrations['total']}")
        print(f"Pre-registered attendees: {registrations['pre_registered']}")
        print(f"On-spot registrations: {registrations['spot_registered']}")
        print(f"Failed registrations: {registrations['failed']}")
        
    except Exception as e:
        print(f"\nCritical error: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
