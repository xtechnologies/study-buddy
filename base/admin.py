from django.contrib import admin
from .models import Room, Topic, Message, ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("user", "short_message", "short_response", "timestamp")
    search_fields = ("user__username", "message", "response")
    list_filter = ("timestamp",)
    ordering = ("-timestamp",)

    def short_message(self, obj):
        return obj.message[:50] + ("..." if len(obj.message) > 50 else "")
    short_message.short_description = "Message"

    def short_response(self, obj):
        return obj.response[:50] + ("..." if len(obj.response) > 50 else "")
    short_response.short_description = "Response"


admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
