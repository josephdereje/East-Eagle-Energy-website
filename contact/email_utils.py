from django.conf import settings
from django.core.mail import send_mail


def send_inquiry_email(inquiry):
    subject = f'New quote request from {inquiry.name}'
    body = (
        f'New contact inquiry — East Eagle Energy\n\n'
        f'Name: {inquiry.name}\n'
        f'Telephone: {inquiry.phone}\n'
        f'Company: {inquiry.company}\n'
        f'Address: {inquiry.address}\n'
        f'Email: {inquiry.email}\n\n'
        f'Message:\n{inquiry.message}\n'
    )

    recipient = settings.CONTACT_RECIPIENT_EMAIL
    from_email = settings.DEFAULT_FROM_EMAIL

    send_mail(
        subject=subject,
        message=body,
        from_email=from_email,
        recipient_list=[recipient],
        fail_silently=False,
    )
