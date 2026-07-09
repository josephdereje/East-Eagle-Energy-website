from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from .email_utils import send_inquiry_email
from .forms import ContactInquiryForm


def submit_inquiry(request):
    if request.method != 'POST':
        return redirect('home')

    form = ContactInquiryForm(request.POST)
    if not form.is_valid():
        messages.error(request, 'Please correct the errors in the form and try again.')
        return HttpResponseRedirect('/#quote')

    inquiry = form.save(commit=False)
    try:
        send_inquiry_email(inquiry)
        inquiry.email_sent = True
    except Exception:
        inquiry.email_sent = False
        messages.warning(
            request,
            'Your message was saved but email could not be sent. We will still review it.',
        )
    inquiry.save()

    if inquiry.email_sent:
        messages.success(
            request,
            'Thank you! Your quote request has been sent. We will contact you soon.',
        )

    return HttpResponseRedirect('/#quote')
