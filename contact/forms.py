from django import forms

from .models import ContactInquiry


class ContactInquiryForm(forms.ModelForm):
    class Meta:
        model = ContactInquiry
        fields = ['name', 'phone', 'company', 'address', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your full name',
                'id': 'quote-name',
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': '+251 93 321 9802',
                'id': 'quote-phone',
                'type': 'tel',
            }),
            'company': forms.TextInput(attrs={
                'placeholder': 'Company name',
                'id': 'quote-company',
            }),
            'address': forms.TextInput(attrs={
                'placeholder': 'City, region, or full address',
                'id': 'quote-address',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'your.email@example.com',
                'id': 'quote-email',
            }),
            'message': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Tell us about your project, power needs, or products you are interested in...',
                'id': 'quote-message',
            }),
        }


class SupportChatStartForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'placeholder': 'your.email@example.com',
            'autocomplete': 'email',
        }),
    )
    name = forms.CharField(
        max_length=120,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your name (optional)',
            'autocomplete': 'name',
        }),
    )
    page_url = forms.CharField(max_length=500, required=False)


class SupportChatSendForm(forms.Form):
    session_id = forms.UUIDField()
    message = forms.CharField(min_length=2, max_length=2000)
