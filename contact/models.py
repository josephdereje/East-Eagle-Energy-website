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
