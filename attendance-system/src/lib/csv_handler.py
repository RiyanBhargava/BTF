import csv
import os
import random
import string
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def get_db():
    """Get MongoDB database connection"""
    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("DB_NAME")
    
    if not mongo_uri:
        raise ValueError("MONGO_URI environment variable is not set")
    if not db_name:
        raise ValueError("DB_NAME environment variable is not set")
        
    client = MongoClient(mongo_uri)
    return client[db_name]

def get_user_by_registration_id(registration_id):
    """Get user data from MongoDB by registration ID"""
    try:
        db = get_db()
        return db.registrations.find_one({"registrationId": registration_id})
    except Exception as e:
        print(f"Database error: {str(e)}")
        return None

def generate_registration_id():
    """Generate a unique registration ID for on-spot registrations"""
    # Format: BTF-SPOT-XXXX where X is alphanumeric
    while True:
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        reg_id = f"BTF-SPOT-{random_part}"
        
        # Check if already exists
        if get_user_by_registration_id(reg_id) is None:
            return reg_id

def get_csv_path(event_name):
    """Get the path to the CSV file for an event"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    default_csv_dir = os.path.join(base_dir, "attendance_records")
    csv_dir = os.getenv("CSV_DIR", default_csv_dir)
    os.makedirs(csv_dir, exist_ok=True)
    return os.path.join(csv_dir, f"{event_name}.csv")

def check_already_registered(event_name, registration_id):
    """Check if a registration ID is already registered for an event"""
    csv_path = get_csv_path(event_name)
    
    try:
        with open(csv_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 3 and row[2] == registration_id:
                    return True
    except FileNotFoundError:
        return False
        
    return False

def register_attendance(event_name, registration_id, user_data=None, is_spot_registration=False):
    """Register attendance for an event"""
    csv_path = get_csv_path(event_name)
    
    # Check if already registered
    if check_already_registered(event_name, registration_id):
        print(f"⚠️ ID {registration_id} already registered for {event_name}")
        return False
    
    # Get user data if not provided (for pre-registered users)
    if not is_spot_registration and user_data is None:
        user_data = get_user_by_registration_id(registration_id)
        if user_data is None:
            print(f"❌ Registration ID {registration_id} not found in database.")
            return False
    
    # Write to CSV
    file_exists = os.path.exists(csv_path)
    try:
        with open(csv_path, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Timestamp", "Event", "RegistrationID", "Name", "Email", "Phone", "IsSpotRegistration"])
            
            if is_spot_registration:
                writer.writerow([
                    datetime.now(), 
                    event_name, 
                    registration_id,
                    user_data.get("firstName", "") + " " + user_data.get("lastName", ""),
                    user_data.get("email", ""),
                    user_data.get("phone", ""),
                    "Yes"
                ])
            else:
                writer.writerow([
                    datetime.now(), 
                    event_name, 
                    registration_id,
                    user_data.get("firstName", "") + " " + user_data.get("lastName", ""),
                    user_data.get("email", ""),
                    user_data.get("phone", ""),
                    "No"
                ])
        
        print(f"✅ Successfully registered: {registration_id} for {event_name}")
        return True
    except Exception as e:
        print(f"Error writing to CSV: {str(e)}")
        return False

def handle_spot_registration():
    """Handle on-spot registration"""
    print("\n--- On-Spot Registration ---")
    
    # Collect participant information
    first_name = input("First Name: ").strip()
    last_name = input("Last Name: ").strip()
    email = input("Email: ").strip()
    phone = input("Phone: ").strip()
    
    # Generate registration ID
    reg_id = generate_registration_id()
    
    # Create user data
    user_data = {
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "phone": phone
    }
    
    return reg_id, user_data

def check_registration_id_DB(registration_id):
    db = get_db()
    return db.registrations.find_one({"registrationId": registration_id}) is not None

# Legacy function - kept for backward compatibility
def check_registration_id_csv(registration_id):
    event_name = os.getenv("EVENT_NAME", "")
    if not event_name:
        print("Warning: EVENT_NAME environment variable not set")
        return False
        
    csv_path = get_csv_path(event_name)
    try:
        with open(csv_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 3 and row[2] == registration_id and row[1] == event_name:
                    return True
    except FileNotFoundError:
        return False
    return False

# Legacy function - kept for backward compatibility
def write_to_csv(registration_id):
    event_name = os.getenv("EVENT_NAME", "")
    if not event_name:
        print("Warning: EVENT_NAME environment variable not set")
        return
        
    if check_registration_id_DB(registration_id):
        if not check_registration_id_csv(registration_id):
            csv_path = get_csv_path(event_name)
            file_exists = os.path.exists(csv_path)
            with open(csv_path, 'a', newline='') as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["Timestamp", "Event", "RegistrationID"])
                writer.writerow([datetime.now(), event_name, registration_id])
                print(f"Registered: {registration_id}")
        else:
            print(f'ID {registration_id} already registered for {event_name} in CSV.')
    else:
        print(f"Registration ID {registration_id} not found in DB.")
    
