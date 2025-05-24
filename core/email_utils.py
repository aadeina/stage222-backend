from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings
from django.template.loader import render_to_string

def send_otp_email(to_email, user_name, otp_code, verify_url):
    html_content = render_to_string("emails/verify_email.html", {
        "user_name": user_name,
        "otp_code": otp_code,
        "verify_url": verify_url
    })

    subject = f"{otp_code} is your Stage222 verification code"

    message = Mail(
        from_email=("info@stage222.com", "Stage222"),
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )

    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        sg.send(message)
        return True
    except Exception as e:
        print("SendGrid Error:", e)
        return False
