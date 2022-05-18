from django.http import Http404, JsonResponse

from rest_framework.views import APIView
from rest_framework.parsers import JSONParser

from .serializers import MusicSerializer, LibrarySerializer
from .models import Music, Library

import datetime
from collections.abc import Iterable

class MusicListView(APIView):
    def get(self, request):
        return JsonResponse(MusicSerializer(Music.objects.all(), many=True).data, safe=False)

class LibraryListView(APIView):
    def get(self, request):
        return JsonResponse(LibrarySerializer(Music.objects.all(), many=True).data, safe=False)
