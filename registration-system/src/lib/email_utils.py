import smtplib
import os
from email.message import EmailMessage
from .qr_utils import generate_qr_code
from dotenv import load_dotenv

load_dotenv()

def send_qr_email(user):
    """
    Generates QR code for a user and sends it via email
    Returns the QR code data for database storage
    """
    if 'email' not in user or not user['email']:
        raise ValueError("User does not have a valid email address")
        
    if 'registrationId' not in user or not user['registrationId']:
        raise ValueError("User does not have a valid registration ID")
        
    msg = EmailMessage()
    msg['Subject'] = f"BTF Registration QR - {user['firstName']} {user['registrationId']}"
    msg['From'] = os.getenv("EMAIL_USER")
    msg['To'] = user['email']
    
    # Generate QR code
    qr_data = generate_qr_code(user['registrationId'])
    
    # Email content
    event_list = ', '.join(user.get('interestedEvents', []))
    
    body = f"""Hi {user['firstName']},
    
Thank you for registering for BITS Tech Fest 2025!

Your registration details:
ID: {user['registrationId']}
Events: {event_list}

Please bring this QR code with you to the event for a quick check-in experience.
We look forward to seeing you at BTF 2025!
"""
    
    msg.set_content(body)
    
    # Attach QR
    try:
        with open(qr_data["img_path"], "rb") as f:
            msg.add_attachment(f.read(), maintype="image", subtype="png", filename="btf_qr.png")
        
        # Send email
        email_user = os.getenv("EMAIL_USER")
        email_password = os.getenv("EMAIL_PASSWORD")
        
        if not email_user or not email_password:
            raise ValueError("Email credentials are not properly configured in .env file")
            
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(email_user, email_password)
            server.send_message(msg)
            
        print(f"Email sent to {user['email']} with QR code attached.")
        
    except FileNotFoundError:
        print(f"Warning: QR code file not found at {qr_data['img_path']}")
        # Continue without the attachment
    except smtplib.SMTPAuthenticationError:
        raise Exception("Email authentication failed. Check your username and password.")
    except smtplib.SMTPException as e:
        raise Exception(f"SMTP error: {str(e)}")
    
    return qr_data
    
