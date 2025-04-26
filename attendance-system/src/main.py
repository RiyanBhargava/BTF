# Attendance System - Main Script
from lib.scanner_utils import scan_qr
from lib.csv_handler import write_to_csv
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    print(f"Scanning for event: {os.getenv('EVENT_NAME')}")
    for qr_data in scan_qr():
        write_to_csv(qr_data)

if __name__ == "__main__":
    main()
