from django.http import Http404, JsonResponse

from rest_framework.views import APIView
from rest_framework.parsers import JSONParser

from .serializers import MusicSerializer, LibrarySerializer, YtRefSerializer
from .models import Music, Library, YtRef

import datetime
from collections.abc import Iterable

class MusicListView(APIView):
    def get(self, request):
        return JsonResponse(MusicSerializer(Music.objects.all(), many=True).data, safe=False)

class LibraryListView(APIView):
    def get(self, request):
        return JsonResponse(LibrarySerializer(Library.objects.all(), many=True).data, safe=False)

class RefListView(APIView):
    def get(self, request):
        return JsonResponse(YtRefSerializer(YtRef.objects.all(), many=True).data, safe=False)

    def post(self, request):
        data = JSONParser().parse(request)
        ref = self.get_ref_from_id(data['yt_id'])

        if ref is None:
            serializer = YtRefSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        else:
            serializer = YtRefSerializer(ref, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)

    @staticmethod
    def get_ref_from_id(yt_id):
        try:
            return YtRef.objects.get(yt_id=yt_id)
        except YtRef.DoesNotExist:
            return None
