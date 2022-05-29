from django.db import models
from django.contrib.auth.models import User

class Music(models.Model):
    title = models.CharField(max_length=200)
    filename = models.CharField(max_length=40)

    artist = models.CharField(max_length=200, default="", blank=True)
    album = models.CharField(max_length=200, default="", blank=True)

    def __str__(self):
        return f"{self.title} - {self.artist}"

class YtRef(models.Model):
    yt_id = models.CharField(max_length=200)
    downloaded = models.BooleanField()
    ignored = models.BooleanField()
    remind = models.IntegerField(default=1)
    music = models.ForeignKey(Music, null=True, on_delete=models.SET_NULL)
    is_test = models.BooleanField(default=False)

class Playlist(models.Model):
    name = models.CharField(max_length=200)
    musics = models.ManyToManyField(Music, blank=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    current_version = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.name}, {self.musics.count()} sounds"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_playlist = models.ForeignKey(Playlist, null=True, on_delete=models.SET_NULL, default=None, blank=True)
