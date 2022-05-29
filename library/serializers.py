from rest_framework import serializers
from .models import Music, Playlist, YtRef, Profile
from rest_framework.exceptions import APIException

class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ['id', 'title', 'filename', 'artist', 'album']

    def to_representation(self, value):
        default_repr = super().to_representation(value)
        refs = value.ytref_set.all().values('yt_id')
        if refs:
            default_repr['yt_id'] = refs[0]['yt_id']
        else:
            default_repr['yt_id'] = None
        default_repr['id'] = value.id
        print(default_repr)
        return default_repr

class PlaylistSerializer(serializers.ModelSerializer):
    musics = MusicSerializer(many=True, read_only=True)
    class Meta:
        model = Playlist
        fields = ['name', 'musics', 'current_version']

class YtRefSerializer(serializers.ModelSerializer):
    music = MusicSerializer(read_only=True)
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

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['current_playlist']
