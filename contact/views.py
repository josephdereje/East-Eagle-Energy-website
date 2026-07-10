from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from .email_utils import send_inquiry_email
from .forms import ContactInquiryForm


def contact_page(request):
    form = ContactInquiryForm()
    return render(request, 'contact/contact.html', {'form': form})


def submit_inquiry(request):
    next_url = request.POST.get('next', '/#quote')

    if request.method != 'POST':
        return redirect('contact:page')

    form = ContactInquiryForm(request.POST)
    if not form.is_valid():
        if next_url == '/contact/':
            return render(request, 'contact/contact.html', {'form': form})
        messages.error(request, 'Please correct the errors and try again.')
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

    messages.success(
        request,
        'Thank you! Your consultation request has been sent. We will contact you soon.',
    )

    return HttpResponseRedirect(next_url if next_url else '/contact/')
