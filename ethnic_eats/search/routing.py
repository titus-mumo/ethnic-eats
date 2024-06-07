# urls.py
from django.urls import path
from .consumers import CuisineConsumer

websocket_urlpatterns = [
    path('ws/cuisine/', CuisineConsumer.as_asgi()),
]