from django.shortcuts import render
from django.http import Http404, JsonResponse, HttpResponse

from rest_framework.views import APIView

class PlaylistView(APIView):
    def get(self, request, playlist_id):
        pass
