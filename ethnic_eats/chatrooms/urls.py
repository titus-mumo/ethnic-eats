from django.urls import path

from django.urls import path
from .views import ChatMessageListCreate

urlpatterns = [
    path('api/chat/<str:room_name>/', ChatMessageListCreate.as_view()),
]
