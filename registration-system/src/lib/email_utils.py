import qrcode
import smtplib
import os
from email.message import EmailMessage

def send_qr_email(user):
    msg = EmailMessage()
    msg['Subject'] = f"BTF Registration QR - {user['firstName']} {user['registrationId']}"
    msg['From'] = os.getenv("EMAIL_USER")
    msg['To'] = user['email']
    
    # Generate QR code
    img_dir = 'registration-system\qr'
    os.makedirs(img_dir, exist_ok=True)
    img_path = f"{img_dir}/temp_qr_{user['registrationId']}.png"
    qr = qrcode.make(user['registrationId'])
    qr.save(img_path)

    
    # Email content
    body = f"""Hi {user['firstName']},
    
Your registration details:
ID: {user['registrationId']}
Events: {', '.join(user.get('interestedEvents', []))}"""
    
    msg.set_content(body)
    
    # Attach QR
    with open(img_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="image", subtype="png", filename="btf_qr.png")
    
    # Send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"))
        server.send_message(msg)
        server.quit()
    print(f"Email sent to {user['email']} with QR code attached.")
    
