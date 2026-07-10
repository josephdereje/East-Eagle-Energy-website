from django.contrib import admin
from django.utils.html import format_html

from .models import ContactInquiry


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'phone', 'email', 'company',
        'status_badge', 'created_at',
    )
    list_filter = ('email_sent', 'created_at')
    search_fields = ('name', 'email', 'phone', 'company', 'message')
    readonly_fields = ('created_at', 'email_sent', 'formatted_message')
    ordering = ('-created_at',)

    fieldsets = (
        ('Contact Details', {
            'fields': ('name', 'phone', 'email', 'company', 'address'),
        }),
        ('Message', {
            'fields': ('formatted_message',),
        }),
        ('Status', {
            'fields': ('email_sent', 'created_at'),
        }),
    )

    def status_badge(self, obj):
        if obj.email_sent:
            return format_html(
                '<span style="background:#dcfce7;color:#166534;padding:3px 10px;'
                'border-radius:12px;font-size:0.78rem;font-weight:600;">✓ Email sent</span>'
            )
        return format_html(
            '<span style="background:#fef9c3;color:#854d0e;padding:3px 10px;'
            'border-radius:12px;font-size:0.78rem;font-weight:600;">⚠ Not sent</span>'
        )
    status_badge.short_description = 'Email'

    def formatted_message(self, obj):
        return format_html(
            '<div style="background:#f8fafc;padding:1rem;border-radius:8px;'
            'border:1px solid #dde6f0;white-space:pre-wrap;line-height:1.7;">{}</div>',
            obj.message,
        )
    formatted_message.short_description = 'Message'

    def has_add_permission(self, request):
        return False
