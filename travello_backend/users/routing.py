from django.urls import path
from .consumer import TravelChat
from django.urls import re_path

websocket_urlpatterns = [
     re_path(r'ws/chat/?$', TravelChat.as_asgi()),
]