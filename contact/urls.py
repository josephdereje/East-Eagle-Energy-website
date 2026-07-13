from django.urls import path

from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.contact_page, name='page'),
    path('submit/', views.submit_inquiry, name='submit'),
    path('chat/start/', views.chat_start, name='chat_start'),
    path('chat/send/', views.chat_send, name='chat_send'),
    path('chat/history/<uuid:session_id>/', views.chat_history, name='chat_history'),
]
