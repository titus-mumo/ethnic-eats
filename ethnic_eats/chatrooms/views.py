from rest_framework import generics
from .models import ChatRoom, ChatMessage
from .serializers import ChatRoomSerializer, ChatMessageSerializer

class ChatRoomListCreate(generics.ListCreateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

class ChatRoomDetail(generics.RetrieveAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

class ChatMessageListCreate(generics.ListCreateAPIView):
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        room_name = self.kwargs['room']
        return ChatMessage.objects.filter(room=room_name).order_by('-timestamp')

    def perform_create(self, serializer):
        room_name = self.kwargs['room']
        room = ChatRoom.objects.get(room=room_name)
        serializer.save(room=room)
