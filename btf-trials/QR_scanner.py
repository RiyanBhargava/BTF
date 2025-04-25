import cv2
from pyzbar.pyzbar import decode
from pymongo import MongoClient
from datetime import datetime

MONGO_URI = "mongodb+srv://dbadmin:yuvaraj@btf-trials.qkcnwyo.mongodb.net/"
DB_NAME = "btf"
REG_COLLECTION = "registrations"
ATTEND_COLLECTION = "attendance"
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
reg_col = db[REG_COLLECTION]
attend_col = db[ATTEND_COLLECTION]

def mark_attendance(qr_string):
    user = reg_col.find_one({"qr_string": qr_string})
    if user:
        if attend_col.find_one({"qr_string": qr_string}):
            print(f"Already marked: {user['name']}")
            return
        attend_col.insert_one({
            '_id': user['_id'],
            "qr_string": qr_string,
            "name": user['name'],
            "email": user['email'],
            "timestamp": datetime.now()
        })
        print(f"Attendance marked for {user['name']}")
    else:
        print("Invalid QR code!")

def scan_qr():
    cap = cv2.VideoCapture(0)
    print("Scanning for QR codes. Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        for barcode in decode(frame):
            qr_string = barcode.data.decode('utf-8')
            print(f"Scanned: {qr_string}")
            mark_attendance(qr_string)
            cv2.waitKey(1000)  
        cv2.imshow('QR Scanner', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    scan_qr()
