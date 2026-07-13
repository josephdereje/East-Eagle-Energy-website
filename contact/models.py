import uuid

from django.db import models


class ContactInquiry(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    company = models.CharField(max_length=150)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    email_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Contact inquiries'

    def __str__(self):
        return f'{self.name} — {self.email} ({self.created_at:%Y-%m-%d})'


class SupportChatSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    name = models.CharField(max_length=120, blank=True)
    page_url = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-last_active']
        verbose_name = 'Support chat session'

    def __str__(self):
        label = self.name or self.email
        return f'{label} ({self.created_at:%Y-%m-%d %H:%M})'


class SupportChatMessage(models.Model):
    ROLE_USER = 'user'
    ROLE_BOT = 'bot'
    ROLE_CHOICES = [
        (ROLE_USER, 'User'),
        (ROLE_BOT, 'Bot'),
    ]

    session = models.ForeignKey(
        SupportChatSession,
        on_delete=models.CASCADE,
        related_name='messages',
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    body = models.TextField()
    email_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Support chat message'

    def __str__(self):
        return f'{self.get_role_display()} — {self.body[:48]}'
