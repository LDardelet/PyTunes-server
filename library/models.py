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

class Library(models.Model):
    title = models.CharField(max_length=200)
    musics = models.ManyToManyField(Music)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return f"{self.title}, {len(self.musics)} sounds"
