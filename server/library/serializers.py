from rest_framework import serializers
from .models import Music, Library, YtRef
from rest_framework.exceptions import APIException

class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ['title', 'artist', 'album', 'from_yt', 'url_yt']

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ['title', 'musics', 'modified_on']

class YtRefSerializer(serializers.ModelSerializer):
    class Meta:
        model = YtRef
        fields = ['yt_id', 'downloaded', 'remind']

    def update(self, instance, validated_data):
        if instance.downloaded:
            return instance
        if validated_data.get('downloaded', False):
            setattr(instance, 'downloaded', True)
            instance.save()
            return instance
        setattr(instance, 'remind', getattr(instance, 'remind')+1)
        instance.save()
        return instance
