from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from east_eagle_site.seo import contact_schema_json

from .ai_bot import ai_enabled, get_bot_reply
from .chat_utils import WELCOME_MESSAGE
from .email_utils import send_inquiry_email, send_support_chat_email
from .forms import ContactInquiryForm, SupportChatSendForm, SupportChatStartForm
from .models import SupportChatMessage, SupportChatSession


def contact_page(request):
    form = ContactInquiryForm()
    return render(request, 'contact/contact.html', {
        'form': form,
        'seo_title': 'Contact Us | East Eagle Energy',
        'seo_description': (
            'Contact East Eagle Energy for solar inverters, battery storage, and energy '
            'system quotes. Based in Addis Ababa, Ethiopia.'
        ),
        'page_schema_json': contact_schema_json(),
    })


def submit_inquiry(request):
    next_url = request.POST.get('next', '/#quote')

    if request.method != 'POST':
        return redirect('contact:page')

    form = ContactInquiryForm(request.POST)
    if not form.is_valid():
        if next_url == '/contact/':
            return render(request, 'contact/contact.html', {
                'form': form,
                'seo_title': 'Contact Us | East Eagle Energy',
                'seo_description': (
                    'Contact East Eagle Energy for solar inverters, battery storage, and energy '
                    'system quotes. Based in Addis Ababa, Ethiopia.'
                ),
                'page_schema_json': contact_schema_json(),
            })
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


def _serialize_message(message):
    return {
        'id': message.pk,
        'role': message.role,
        'body': message.body,
        'created_at': message.created_at.isoformat(),
    }


def _serialize_session_messages(session):
    return [_serialize_message(m) for m in session.messages.all()]


@require_POST
def chat_start(request):
    form = SupportChatStartForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'ok': False, 'errors': form.errors}, status=400)

    session = SupportChatSession.objects.create(
        email=form.cleaned_data['email'],
        name=form.cleaned_data.get('name', ''),
        page_url=form.cleaned_data.get('page_url', ''),
    )
    welcome = SupportChatMessage.objects.create(
        session=session,
        role=SupportChatMessage.ROLE_BOT,
        body=WELCOME_MESSAGE,
    )

    return JsonResponse({
        'ok': True,
        'session_id': str(session.pk),
        'email': session.email,
        'messages': [_serialize_message(welcome)],
        'ai_enabled': ai_enabled(),
    })


@require_GET
def chat_history(request, session_id):
    session = get_object_or_404(SupportChatSession, pk=session_id)
    return JsonResponse({
        'ok': True,
        'session_id': str(session.pk),
        'email': session.email,
        'messages': _serialize_session_messages(session),
        'ai_enabled': ai_enabled(),
    })


@require_POST
def chat_send(request):
    form = SupportChatSendForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'ok': False, 'errors': form.errors}, status=400)

    session = get_object_or_404(
        SupportChatSession,
        pk=form.cleaned_data['session_id'],
    )

    user_message = SupportChatMessage.objects.create(
        session=session,
        role=SupportChatMessage.ROLE_USER,
        body=form.cleaned_data['message'].strip(),
    )

    try:
        send_support_chat_email(session, user_message)
        user_message.email_sent = True
        user_message.save(update_fields=['email_sent'])
    except Exception:
        user_message.email_sent = False
        user_message.save(update_fields=['email_sent'])

    bot_body = get_bot_reply(session, user_message.body)
    bot_message = SupportChatMessage.objects.create(
        session=session,
        role=SupportChatMessage.ROLE_BOT,
        body=bot_body,
    )

    return JsonResponse({
        'ok': True,
        'messages': [
            _serialize_message(user_message),
            _serialize_message(bot_message),
        ],
        'email_sent': user_message.email_sent,
    })
