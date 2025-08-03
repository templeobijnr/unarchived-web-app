from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse

def send_verification_email(user, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    link = request.build_absolute_uri(
        reverse("users:activate", kwargs={"uidb64": uid, "token": token})
    )
    domain = request.get_host()

    verify_link = f"http://{domain}/api/users/verify-email/?uid={uid}/token={token}"
    subject = "Verify your email address"
    message = f"""
Hi {user.username},

Thanks for registering at Unarchived.

Please verify your email by clicking the link below:
{verify_link}

If you didn’t request this, you can ignore this email.

– Unarchived Team
"""

    send_mail(
        subject,
        message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
