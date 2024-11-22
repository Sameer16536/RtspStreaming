from django.http import JsonResponse
from rest_framework.views import APIView

class VideoStreamView(APIView):
    def get(self, request):
        return JsonResponse({
            "stream_url": "rtsp://localhost:8554/live",
            "status": "active",
        })
