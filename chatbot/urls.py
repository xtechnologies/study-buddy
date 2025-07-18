from django.urls import path
from .views import chat_api as chatbot_api, chat_page, chat_history, file_upload_api

app_name = "chatbot"

urlpatterns = [
    path('', chat_page, name='chat_page'),
    path('api/', chatbot_api, name='chat_api'),
    path('api/upload/', file_upload_api, name='file_upload_api'), 
    path('history/', chat_history, name='chat_history'),
]
