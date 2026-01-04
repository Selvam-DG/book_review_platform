import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

MAIL_HOST = os.getenv("MAIL_HOST")
MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() == "true"


def send_email(to_email: str, subject: str, body: str):
    msg = MIMEMultipart()
    msg["From"] = MAIL_FROM
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(MAIL_HOST, MAIL_PORT) as server:
        if MAIL_USE_TLS:
            server.starttls()
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        server.send_message(msg)


# ==========================
# HIGH-LEVEL EMAIL HELPERS
# ==========================

def send_admin_new_user_email(user):
    subject = "New user registration pending approval"
    body = f"""
A new user has registered and is awaiting approval.

Username: {user.username}
Email: {user.email}

Please review and approve the account in the admin panel.
"""
    send_email(ADMIN_EMAIL, subject, body)


def send_user_approved_email(user):
    subject = "Your account has been activated 🎉"
    body = f"""
Hello {user.username},

Your account has been approved by the admin.

You can now log in and add/edit/delete your book reviews.

Happy reading!
"""
    send_email(user.email, subject, body)


def send_user_rejected_email(user):
    subject = "Account registration update"
    body = f"""
Hello {user.username},

Thank you for registering.

Unfortunately, your account was not approved at this time.

Regards,
Book Review Platform
"""
    send_email(user.email, subject, body)
