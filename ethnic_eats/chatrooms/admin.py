from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.ChatMessage)
class ChatMessageModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.ChatMessage._meta.fields]


@admin.register(models.ChatRoom)
class ChatRoomModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.ChatRoom._meta.fields]