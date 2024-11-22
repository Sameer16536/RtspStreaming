from django.http import JsonResponse
from rest_framework.views import APIView

class VideoStreamView(APIView):
    def get(self, request):
        # Returns stream configuration details as JSON response
        # Includes RTSP stream URL and current status
        return JsonResponse({
            "stream_url": "rtsp://localhost:8554/live",
            "status": "active",
        })
