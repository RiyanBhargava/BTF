import qrcode
import os
import uuid
import base64
from io import BytesIO
from pymongo import UpdateOne

def generate_qr_code(data):
    """Generate QR code and return both the image and base64 text version"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save to file
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    img_dir = os.path.join(current_dir, os.getenv("QR_DIR", "qr"))
    os.makedirs(img_dir, exist_ok=True)
    img_path = os.path.join(img_dir, f"qr_{data}.png")
    img.save(img_path)
    
    # Create base64 encoded version
    buffered = BytesIO()
    img.save(buffered)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return {
        "img_path": img_path,
        "img_base64": img_str
    }

def prepare_qr_update_operation(user, qr_data):
    """Create MongoDB update operation for storing QR data"""
    return UpdateOne(
        {"_id": user["_id"]},
        {"$set": {
            "qr_sent": True,
            "qr_base64": qr_data["img_base64"],
            "qr_generated_at": {"$date": {"$numberLong": str(int(user.get('registrationDate', 0)))}}
        }}
    ) 