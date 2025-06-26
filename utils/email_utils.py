import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_password_reset_email(email, reset_link):
    message = Mail(
        from_email=('info@stage222.com', 'Stage222'),
        to_emails=email,
        subject='Reset Your Stage222 Password',
        html_content=f"""
        <p>Hello 👋,</p>
        <p>You requested a password reset. Click the link below to set a new password:</p>
        <p><a href="{reset_link}">Reset Password</a></p>
        <br>
        <p>If you didn't request this, ignore this email.</p>
        <p>– Stage222 Team</p>
        """
    )
    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        print(f"❌ SendGrid error: {e}")
        return None
