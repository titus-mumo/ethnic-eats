from rest_framework import serializers
from .models import ChatRoom, ChatMessage

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['id', 'room', 'created_at']

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'room', 'message', 'user', 'timestamp']

