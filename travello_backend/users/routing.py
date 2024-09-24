from django.urls import path
from .consumer import TravelChat
from django.urls import re_path

websocket_urlpatterns = [
     re_path(r'ws/chat/(?P<room_name>\w+)/$', TravelChat.as_asgi()),
]