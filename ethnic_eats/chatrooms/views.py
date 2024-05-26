from rest_framework import generics
from .models import ChatMessage
from .serializers import ChatMessageSerializer

class ChatMessageListCreate(generics.ListCreateAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        room_name = self.kwargs['room_name']
        return ChatMessage.objects.filter(room_name=room_name).order_by('-timestamp')
