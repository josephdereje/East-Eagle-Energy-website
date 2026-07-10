from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Send a test email using the current .env email settings'

    def add_arguments(self, parser):
        parser.add_argument(
            '--to',
            default=settings.CONTACT_RECIPIENT_EMAIL,
            help='Recipient email address (defaults to CONTACT_RECIPIENT_EMAIL)',
        )

    def handle(self, *args, **options):
        recipient = options['to']
        backend = settings.EMAIL_BACKEND

        self.stdout.write(f'Email backend: {backend}')
        self.stdout.write(f'From: {settings.DEFAULT_FROM_EMAIL}')
        self.stdout.write(f'To: {recipient}')

        if 'smtp' in backend and (
            not settings.EMAIL_HOST_USER
            or 'your-email' in settings.EMAIL_HOST_USER
        ):
            self.stderr.write(self.style.ERROR(
                'EMAIL_HOST_USER is not set. Replace your-email@gmail.com in .env with your real Gmail.'
            ))
            return

        if 'smtp' in backend and (
            not settings.EMAIL_HOST_PASSWORD
            or 'app-password' in settings.EMAIL_HOST_PASSWORD
        ):
            self.stderr.write(self.style.ERROR(
                'EMAIL_HOST_PASSWORD is not set. Add your Gmail App Password to .env (see instructions below).'
            ))
            return

        send_mail(
            subject='East Eagle Energy — test email',
            message=(
                'This is a test email from your East Eagle Energy Django site.\n\n'
                'If you received this, your Gmail SMTP settings are working correctly.'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )

        self.stdout.write(self.style.SUCCESS(f'Test email sent successfully to {recipient}'))
