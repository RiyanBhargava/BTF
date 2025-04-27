# BTF Registration System

This system processes registrations for BITS Tech Fest 2025, generates QR codes for attendees, and emails them to participants.

## Features

- Reads unprocessed user registrations from MongoDB
- Generates QR codes for each registration
- Stores QR code data in the database
- Emails QR codes to registered participants

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
# MongoDB Connection
MONGO_URI=mongodb://username:password@host:port/database
DB_NAME=your_database_name

# Email Configuration
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

# QR Code Configuration
QR_DIR=qr
```

## Usage

Run the main script to process unprocessed registrations:

```
cd src
python main.py
```

The system will:
1. Fetch all unprocessed registrations from MongoDB
2. Generate QR codes for each registration
3. Email QR codes to registrants
4. Update the MongoDB records with QR code information

## Structure

- `src/main.py`: Main script that coordinates all operations
- `src/lib/db_utils.py`: Utilities for database operations
- `src/lib/email_utils.py`: Utilities for email operations
- `src/lib/qr_utils.py`: Utilities for QR code generation
- `qr/`: Directory where QR codes are stored 