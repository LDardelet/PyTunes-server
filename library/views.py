from django.http import Http404, JsonResponse

from rest_framework.views import APIView
from rest_framework.parsers import JSONParser

import datetime
from collections.abc import Iterable

from third_party import MainHandler
from .serializers import MusicSerializer, LibrarySerializer, YtRefSerializer
from .models import Music, Library, YtRef

Handler = MainHandler()

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
        yt_id = data['yt_id']
        ref = self.get_ref_from_id(yt_id)

        status = 201
        metadata = False
        download = False
        ans = {}

        if ref is None:
            serializer = YtRefSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                ans = serializer.data
                if data.get('downloaded', False):
                    download, metadata = Handler.add(yt_id)
            else:
                ans = serializer.errors
                status = 400
        else:
            already_downloaded = ref.downloaded
            serializer = YtRefSerializer(ref, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                ans = serializer.data
                if not already_downloaded and data.get('downloaded', False):
                    download, metadata = Handler.download(yt_id)
            else:
                ans = serializer.errors
                status = 400
        if metadata:
            new_ref = self.get_ref_from_id(yt_id) # We reload that ref, as music field was updated by the handler. Not very elegant though.
            ans = YtRefSerializer(new_ref).data
        ans.update({'download':download, 'metadata':metadata})
        return JsonResponse(ans, status=status)

    @staticmethod
    def get_ref_from_id(yt_id):
        try:
            return YtRef.objects.get(yt_id=yt_id)
        except YtRef.DoesNotExist:
            return None

class RefView(APIView):
    def get(self, request, yt_id):
        print(f'Requested {yt_id}')
        return JsonResponse(YtRefSerializer(self.get_ref_from_id(yt_id)).data, safe=False)

    def delete(self, request, yt_id):
        ref = self.get_ref_from_id(yt_id)
        if ref.downloaded:
            if not ref.music is None:
                Handler.remove(ref.music.filename)
        ref.delete()
        return JsonResponse({'message': f"reference {yt_id} deleted"}, status=200)

    @staticmethod
    def get_ref_from_id(yt_id):
        try:
            return YtRef.objects.get(yt_id=yt_id)
        except YtRef.DoesNotExist:
            return None
