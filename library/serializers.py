from rest_framework import serializers
from .models import Music, Library, YtRef
from rest_framework.exceptions import APIException

class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ['title', 'filename', 'artist', 'album']

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ['title', 'musics', 'modified_on']

class YtRefSerializer(serializers.ModelSerializer):
    class Meta:
        model = YtRef
        fields = ['yt_id', 'downloaded', 'ignored', 'remind', 'music']

    def update(self, instance, validated_data):
        if (instance.ignored or instance.downloaded) and (not instance.yt_id == 'test'):
            return instance
        if validated_data.get('downloaded', False):
            setattr(instance, 'downloaded', True)
            instance.save()
            return instance
        if validated_data.get('ignored', False):
            setattr(instance, 'ignored', True)
            instance.save()
            return instance
        setattr(instance, 'remind', getattr(instance, 'remind')+1)
        instance.save()
        return instance
