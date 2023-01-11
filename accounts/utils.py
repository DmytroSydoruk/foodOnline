from .models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage, send_mail
from django.conf import settings


def detectUser(user: User):
    if user.role == 1:
        redirectUrl = 'vendorDashboard'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'custDashboard'
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl


def send_verification_email(request, user: User, email_subject: str, email_template: str) -> None:
    """Send email to specified user. Args are not optional"""

    template: str = 'accounts/emails/' + email_template
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = user.email
    current_site = get_current_site(request)

    message = render_to_string(template, {
        "user": user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    send_mail(email_subject, message, from_email,
              [to_email], fail_silently=False)


def send_notification(email_subject: str, email_template: str, context: dict):
    template: str = 'accounts/emails/' + email_template
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = context['user'].email
    message = render_to_string(template, context)
    send_mail(email_subject, message, from_email,
              [to_email], fail_silently=False)