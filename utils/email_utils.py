from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

def send_password_reset_otp_email(email, code):
    message = Mail(
        from_email=('info@stage222.com', 'Stage222'),
        to_emails=email,
        subject=f'{code} is your Stage222 password reset code',
        html_content=f"""
        <p>Hello 👋,</p>
        <p>You requested to reset your password. Use the code below:</p>
        <h2>{code}</h2>
        <p>This OTP is valid for 15 minutes. Do not share it with anyone.</p>
        <p>— The Stage222 Team</p>
        """
    )
    sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
    sg.send(message)
