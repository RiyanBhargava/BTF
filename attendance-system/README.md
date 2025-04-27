# BTF Attendance System

This system handles attendance tracking for BITS Tech Fest 2025 events, supporting both QR code scanning and manual registration.

## Features

- Club authentication system for event organizers
- QR code scanning interface for quick check-ins
- Manual registration ID entry option
- On-spot registration for walk-in attendees
- CSV-based attendance records by event

## Setup

1. Create a virtual environment:
```
python -m venv venv
```

2. Activate the virtual environment:
- On Windows: `venv\Scripts\activate`
- On macOS/Linux: `source venv/bin/activate`

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Create a `.env` file in the `src` directory with the following variables:
```
# MongoDB Connection (for validating registrations)
MONGO_URI=mongodb://username:password@host:port/database
DB_NAME=your_database_name

# Attendance Configuration
CSV_DIR=attendance_records
CLUBS_FILE=clubs_data.json
```

## Usage

### Command-line Interface

Run the main script to start the attendance system:

```
cd src
python main.py
```

Follow the prompts to:
1. Authenticate as a club organizer
2. Select your event
3. Scan QR codes or enter registration IDs manually
4. Register on-spot attendees if needed

### Web Interface

The system also includes a web interface for easier usage:

1. Start a local web server from the `src/templates` directory
2. Open `index.html` in a browser
3. Log in with club credentials
4. Use the scanner interface to track attendance

## Structure

- `src/main.py`: Main script that coordinates all operations
- `src/lib/scanner_utils.py`: Utilities for QR code scanning
- `src/lib/csv_handler.py`: Utilities for CSV data operations
- `src/lib/auth_utils.py`: Authentication utilities for clubs
- `attendance_records/`: Directory where attendance CSV files are stored
- `src/templates/`: Directory containing the web interface files 