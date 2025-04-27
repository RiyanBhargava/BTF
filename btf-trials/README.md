# btf_backend
This repository contains scripts for handling registration and attendance using QR codes for BTF Schools.
### Directory Structure
```
BTF-TRIALS/
│
├── add_data.py           # Script to add user data to MongoDB
├── change_data.py        # Script to modify existing user data
├── check_attend_stat.py  # Check attendance status of participants
├── qr_mailing.py         # Main script: generates QR codes, sends to users via email, updates DB
├── QR_scanner.py         # Main script: scans QR codes, verifies and logs attendance in DB
├── reset_qr_sent.py      # Resets QR sent status for users
├── verify_data.py        # Testing script: checks MongoDB connection and data retrieval
├── verify_mailing.py     # Testing script: checks email sending functionality
```
### Main Scripts
- **qr_mailing.py**:  
  Generates QR codes from MongoDB user data, emails the QR to users, and updates the database with the QR string.
- **QR_scanner.py**:  
  Scans participant QR codes on event day, verifies data against MongoDB, and logs attendance in a separate collection.
### Testing Scripts
- **verify_data.py**:  
  Checks MongoDB connection and verifies data access.
- **verify_mailing.py**:  
  Tests email sending setup and delivery.
---
