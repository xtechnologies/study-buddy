from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('chat/', include('chatbot.urls')),
    path('api/', include('base.api.urls')),
    path('accounts/', include('allauth.urls')),
    path("chatbot/", include("chatbot.urls", namespace="chatbot")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)