from rest_framework import serializers
from .models import Music, Library
from rest_framework.exceptions import APIException

class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ['title', 'artist', 'album', 'from_yt', 'url_yt']

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ['title', 'musics', 'modified_on']
