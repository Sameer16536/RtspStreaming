# Django URL configuration for the server project

# Import required Django modules and views
from django.contrib import admin
from django.urls import path, include
from streaming.views import VideoStreamView

# Define URL patterns for the entire project
urlpatterns = [
    # URL for Django admin interface
    path('admin/', admin.site.urls),
    # URL for video streaming REST API endpoint
    path('api/stream/', VideoStreamView.as_view(), name='stream-api'),  
]
