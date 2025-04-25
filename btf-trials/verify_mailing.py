import smtplib
from email.message import EmailMessage

def send_verification_email(sender_email, sender_password, recipient_email):
    """
    Send a test email and verify the sending process
    Returns True if successful, False with error message if failed
    """
    try:
        msg = EmailMessage()
        msg['Subject'] = 'Email Verification Test'
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg.set_content('This is a test email to verify sending functionality')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:  
            server.login(sender_email, sender_password)
            server.send_message(msg)
            
        return True, "Email sent successfully"
    
    except smtplib.SMTPAuthenticationError:
        return False, "Authentication error - check email/password"
    except smtplib.SMTPException as e:
        return False, f"SMTP error occurred: {str(e)}"
    except Exception as e:
        return False, f"General error: {str(e)}"

if __name__ == "__main__":
    YOUR_EMAIL = "f20230254@dubai.bits-pilani.ac.in"
    YOUR_PASSWORD = "zxjeeoqprnxavrxu" 
    RECIPIENT_EMAIL = "f20230006@dubai.bits-pilani.ac.in"
    
    success, message = send_verification_email(
        YOUR_EMAIL,
        YOUR_PASSWORD,
        RECIPIENT_EMAIL
    )

    print(f"Verification result: {success}")
    print(f"Message: {message}")
