from django.db import models
from django.contrib.auth.models import User

class YtRef(models.Model):
    yt_id = models.CharField(max_length=200)
    downloaded = models.BooleanField()
    remind = models.IntegerField(default=1)

class Music(models.Model):
    title = models.CharField(max_length=200)
    filename = models.CharField(max_length=40)

    artist = models.CharField(max_length=200, default="", blank=True)
    album = models.CharField(max_length=200, default="", blank=True)

#    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#    added_on = models.DateTimeField()
#
    yt_ref = models.ForeignKey(YtRef, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return f"{self.title} - {self.artist}"

class Library(models.Model):
    title = models.CharField(max_length=200)
    musics = models.ManyToManyField(Music)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#    modified_on = models.DateTimeField()
    def __str__(self):
        return f"{self.title}, {len(self.musics)} sounds"
