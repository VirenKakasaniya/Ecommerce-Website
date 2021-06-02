from django.core.mail import EmailMessage
from django.conf import settings


def send_review_email(name, email, msg_body):

    context = {
        'name': name,
        'email': email,
    }

    email_subject = 'Status OF your order'
    email_body = msg_body

    email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email, ],
    )
    return email.send(fail_silently=False)