# Import required Django path utility and our WebRTC consumer
from django.urls import path
from .consumers import WebRTCConsumer

# Define WebSocket URL patterns for the application
# This maps the ws/stream/ endpoint to our WebRTC consumer
websocket_urlpatterns = [
    path('ws/stream/', WebRTCConsumer.as_asgi()),
]
