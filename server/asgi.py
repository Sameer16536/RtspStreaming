import os
# Import Django's ASGI application handler
from django.core.asgi import get_asgi_application
# Import Channels routing utilities for WebSocket support
from channels.routing import ProtocolTypeRouter, URLRouter
# Import WebSocket URL patterns from our streaming app
from streaming.routing import websocket_urlpatterns

# Set Django settings module for the project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

# Configure ASGI application with protocol routing
application = ProtocolTypeRouter({
    # Handle traditional HTTP requests
    "http": get_asgi_application(),
    # Handle WebSocket connections using our URL patterns
    "websocket": URLRouter(websocket_urlpatterns),
})
