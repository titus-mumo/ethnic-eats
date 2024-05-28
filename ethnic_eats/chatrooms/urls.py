from django.urls import path
from .views import ChatRoomListCreate, ChatRoomDetail, ChatMessageListCreate

urlpatterns = [
    path('api/chatrooms/', ChatRoomListCreate.as_view(), name='chatroom-list-create'),
    path('api/chatrooms/<int:pk>/', ChatRoomDetail.as_view(), name='chatroom-detail'),
    path('api/chatrooms/<str:room>/messages/', ChatMessageListCreate.as_view(), name='chatmessage-list-create'),
]
