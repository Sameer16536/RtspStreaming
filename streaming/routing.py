from django.urls import path
from .consumers import WebRTCConsumer

websocket_urlpatterns = [
    path('ws/stream/', WebRTCConsumer.as_asgi()),
]
