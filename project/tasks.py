
from celery import shared_task
from django.conf import settings


@shared_task
def send_email(email_subject, email_body, reciver):
    '''Send email using Celery'''
    from django.core.mail import send_mail

    send_mail(email_subject, email_body,str(settings.DEFAULT_FROM_EMAIL),
              [reciver], fail_silently=False)
