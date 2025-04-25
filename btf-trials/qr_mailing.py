import qrcode
import smtplib
from email.message import EmailMessage
from pymongo import MongoClient
from bson.objectid import ObjectId

MONGO_URI = "mongodb+srv://dbadmin:yuvaraj@btf-trials.qkcnwyo.mongodb.net/"
DB_NAME = "btf"
COLLECTION_NAME = "registrations"
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]


EMAIL_ADDRESS = "f20230254@dubai.bits-pilani.ac.in"
EMAIL_PASSWORD = "zxjeeoqprnxavrxu"


def generate_qr_string(user):
    return str(user['_id'])

def send_email(recipient, qr_img_path):
    msg = EmailMessage()
    msg['Subject'] = "Your BTF Registration QR Code"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient
    msg.set_content("Please find attached your QR code for BTF Schools event.")

    with open(qr_img_path, 'rb') as img:
        msg.add_attachment(img.read(), maintype='image', subtype='png', filename="qr.png")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

def main():
    users = collection.find({"qr_sent": False})
    for user in users:
        qr_string = generate_qr_string(user)
        qr_img = qrcode.make(qr_string)
        img_path = f"qr_{user['_id']}.png"
        qr_img.save(img_path)

        collection.update_one(
            {"_id": user['_id']},
            {"$set": {"qr_string": qr_string}}
        )

        try:
            send_email(user['email'], img_path)
            print(f"Sent QR to {user['email']}")
            collection.update_one({"_id": user['_id']},{"$set": {"qr_sent": True}})
        except Exception as e:
            print(f"Failed to send email to {user['email']}: {e}")

if __name__ == "__main__":
    main()
