import csv
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

def get_db():
    client = MongoClient(os.getenv("MONGO_URI"))
    return client[os.getenv("DB_NAME")]

def check_registration_id_DB(registration_id):
    db = get_db()
    return db.registrations.find_one({"registrationId": registration_id}) is not None
def check_registration_id_csv(registration_id):
    try:
        with open(f'{os.getenv("CSV_DIR")}/{os.getenv("EVENT_NAME")}.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[2] == registration_id and row[1] == os.getenv("EVENT_NAME"):
                    return True
    except FileNotFoundError:
        return False
    return False

def write_to_csv(registration_id):
    if check_registration_id_DB(registration_id):
        if not check_registration_id_csv(registration_id):
            os.makedirs(os.getenv("CSV_DIR"), exist_ok=True)
            file_exists = os.path.exists(os.getenv("CSV_DIR"))
            with open(f'{os.getenv("CSV_DIR")}/{os.getenv("EVENT_NAME")}.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["Timestamp", "Event", "RegistrationID"])
                writer.writerow([datetime.now(), os.getenv("EVENT_NAME"), registration_id])
                print(f"Registered: {registration_id}")
        else:
            print(f'ID {registration_id} already registered for {os.getenv("EVENT_NAME")} in CSV.')
    else:
        print(f"Registration ID {registration_id} not found in DB.")
    
