from django.http import Http404, JsonResponse, HttpResponse
import mimetypes

from rest_framework.views import APIView
from rest_framework.parsers import JSONParser

import datetime
from enum import Enum
from collections.abc import Iterable

from third_party import MainHandler
from .serializers import MusicSerializer, LibrarySerializer, YtRefSerializer, ProfileSerializer
from .models import Music, Library, YtRef, Profile

Handler = MainHandler()

class MusicListView(APIView):
    def get(self, request):
        return JsonResponse(MusicSerializer(Music.objects.all(), many=True).data, safe=False)

class RefListView(APIView):
    def get(self, request):
        return JsonResponse(YtRefSerializer(YtRef.objects.all(), many=True).data, safe=False)

    def post(self, request):
        data = JSONParser().parse(request)
        yt_id = data['yt_id']
        ref = get_ref_from_id(yt_id)

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
            new_ref = get_ref_from_id(yt_id) # We reload that ref, as music field was updated by the handler. Not very elegant though.
            ans = YtRefSerializer(new_ref).data
        ans.update({'download':download, 'metadata':metadata})
        return JsonResponse(ans, status=status)

class LibraryListView(APIView):
    def get(self, request):
        return JsonResponse(LibrarySerializer(Library.objects.all(), many=True).data, safe=False)

class MusicView(APIView):
    def get(self, request, music_id):
        music = get_music_from_id(music_id)
        if music is None:
            raise Http404(f"Music {music_id} does not exist")
        return JsonResponse(MusicSerializer(music).data, safe=False)

class MusicFileView(APIView):
    def get(self, request, music_id):
        music = get_music_from_id(music_id)
        if music is None:
            raise Http404(f"Music {music_id} does not exist")
        absolute_path = Handler.get_filename(music)
        
        try:
            with open(absolute_path, 'rb') as music_file:
                mime_type, _ = mimetypes.guess_type(absolute_path)
                response = HttpResponse(music_file, content_type=mime_type)
                response['Content-Disposition'] = f"attachment; filename={music.filename.replace('/', '#')}"
                return response
        except FileNotFoundError:
            raise Http404(f"Music {music_id} file missing")

class RefView(APIView):
    def get(self, request, yt_id):
        ref = get_ref_from_id(yt_id)
        if ref is None:
            JsonResponse({}, status=201)
        data = YtRefSerializer(ref).data
        return JsonResponse(YtRefSerializer(ref).data, safe=False, status=201)

    def delete(self, request, yt_id):
        ref = get_ref_from_id(yt_id)
        if ref.downloaded and not ref.music is None:
            file_removed = Handler.remove(ref.music)
        ref.delete()
        return JsonResponse({'message': f"reference {yt_id} deleted, {int(file_removed)} file removed"}, status=200)

class LibraryView(APIView):
    def get(self, request, library_id):
        library = get_library_from_id(library_id)
        if library is None:
            raise Http404(f"Library {library_id} does not exist")
        return JsonResponse(LibrarySerializer(library).data, safe=False)

    def put(self, requets, library_id):
        library = get_library_from_id(library_id)
        if library is None:
            raise Http404(f"Library {library_id} does not exist")
        data = JSONParser().parse(request)
        
        Update = False
        songs_updates = data.get('songs_updates', [])
        for music_id, in_library in songs_updates:
            music = get_music_from_id(music_id)
            if music is None:
                raise HttpResponse(f"Music {music_id} does not exist", status = 204)
            if in_library:
                if not library.musics.contains(music):
                    library.musics.add(music)
                else:
                    raise HttpResponse(f"Music {music_id} already in this library", status = 204)
            else:
                if library.musics.contains(music):
                    library.musics.remove(music)
                else:
                    raise HttpResponse(f"Music {music_id} not in this library", status = 204)
            Update = True
        name_update = data.get('name', None)
        if not name_update is None:
            Update = True
            library.name = name_update

        if Update:
            library.current_version += 1
            library.save()
            return HttpResponse("Updated", status=200)
        else:
            raise HttpResponse(f"No update", status = 204)

class ProfileView(APIView):
    def get(self, request, username):
        try:
            profile = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            raise Http404(f"No user named {username}")
        return JsonResponse(ProfileSerializer(profile).data, safe=False)

class TestsCleanerView(APIView):
    def delete(self, request):
        refs_deletions = 0
        files_deletions = 0
        for ref in YtRef.objects.filter(is_test=True):
            if not ref.music is None:
                files_deletions += int(Handler.remove(ref.music))
            ref.delete()
            refs_deletions += 1
        return JsonResponse({'message': f"{refs_deletions} references deleted, {files_deletions} files deleted"}, status=200)

def get_library_from_id(library_id):
    try:
        return Library.objects.get(id=library_id)
    except Library.DoesNotExist:
        return None
def get_music_from_id(music_id):
    try:
        return Music.objects.get(id=music_id)
    except Music.DoesNotExist:
        return None
def get_ref_from_id(yt_id):
    try:
        return YtRef.objects.get(yt_id=yt_id)
    except YtRef.DoesNotExist:
        return None

