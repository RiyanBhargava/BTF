import os
import json
import hashlib
import getpass
from dotenv import load_dotenv

load_dotenv()

def get_clubs_data():
    """Load club credentials from JSON file"""
    # Use absolute path for clubs data file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    default_clubs_path = os.path.join(base_dir, "clubs_data.json")
    
    clubs_file = os.getenv("CLUBS_FILE", default_clubs_path)
    
    try:
        with open(clubs_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Create default clubs data if file doesn't exist
        default_clubs = {
            "clubs": [
                {"name": "Linux Users Group", "username": "lug", "password_hash": hash_password("lugbtf"), "events": ["Crack The Penguin"]},
                {"name": "Google Developer Group", "username": "gdg", "password_hash": hash_password("gdgbtf"), "events": ["Hunter AI"]},
                {"name": "Skyline", "username": "skyline", "password_hash": hash_password("skylinebtf"), "events": ["Marshmallow Tower Challenge"]},
                {"name": "IEEE", "username": "ieee", "password_hash": hash_password("ieeebtf"), "events": ["Research Paper Presentation"]},
                {"name": "ACM", "username": "acm", "password_hash": hash_password("acmbtf"), "events": ["Escape The Matrix"]},
                {"name": "AIChE", "username": "aiche", "password_hash": hash_password("aichebtf"), "events": ["Hydro Purity Quest"]},
            ]
        }
        
        # Save default clubs data
        clubs_dir = os.path.dirname(clubs_file)
        if clubs_dir:
            os.makedirs(clubs_dir, exist_ok=True)
            
        with open(clubs_file, 'w') as f:
            json.dump(default_clubs, f, indent=2)
        
        print(f"Created default clubs data file: {clubs_file}")
        return default_clubs

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def authenticate_club():
    """Authenticate a club and return the selected event"""
    clubs_data = get_clubs_data()
    
    print("\nBTF Club Authentication")
    print("------------------------")
    
    max_attempts = 3
    for attempt in range(max_attempts):
        username = input("Username: ").strip()
        password = getpass.getpass("Password: ")
        
        # Find club by username
        club = next((c for c in clubs_data["clubs"] if c["username"] == username), None)
        
        if club and club["password_hash"] == hash_password(password):
            print(f"\nWelcome, {club['name']}!")
            
            # Select event
            if len(club["events"]) == 1:
                selected_event = club["events"][0]
                print(f"Auto-selecting your event: {selected_event}")
            else:
                print("\nSelect an event:")
                for i, event in enumerate(club["events"], 1):
                    print(f"{i}. {event}")
                
                while True:
                    try:
                        choice = int(input("\nEnter event number: "))
                        if 1 <= choice <= len(club["events"]):
                            selected_event = club["events"][choice-1]
                            break
                        else:
                            print("Invalid choice. Try again.")
                    except ValueError:
                        print("Please enter a number.")
            
            return {
                "club_name": club["name"],
                "event_name": selected_event
            }
        
        remaining = max_attempts - attempt - 1
        if remaining > 0:
            print(f"Authentication failed. {remaining} attempts remaining.")
        else:
            print("Authentication failed. Maximum attempts reached.")
    
    return None 