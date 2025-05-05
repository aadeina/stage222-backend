from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings

def send_verification_email(user, request, token):
    uid = str(user.pk)
    verify_url = request.build_absolute_uri(
        reverse('verify-email', kwargs={'uid': uid, 'token': token})
    )

    subject = 'Verify Your Email for Stage222'
    message = f'Hello {user.email},\n\nPlease verify your email by clicking the link below:\n{verify_url}\n\nThank you!'
    
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )
