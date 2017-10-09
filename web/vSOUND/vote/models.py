from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class votable_song(models.Model):
    file_name = models.TextField()
    song_title = models.TextField()
    song_artist = models.TextField()
    song_album = models.TextField()

    def clear_all():
        votable_song.objects.all().delete()
        suspended_song.objects.all().delete()

    def add(filename, title, artist, album):
        votable_song(file_name=filename, song_title=title, song_artist=artist, song_album=album).save()

    def suspend_song(v_song):
        suspended_song(file_name=v_song.file_name, song_title=v_song.song_title, song_artist=v_song.song_artist, song_album=v_song.song_album, s_order=timezone.now()).save()
        v_song.delete()

class suspended_song(models.Model):
    file_name = models.TextField()
    song_title = models.TextField()
    song_artist = models.TextField()
    song_album = models.TextField()
    s_order = models.DateTimeField()

    def check_for_unsuspend():
        if(suspended_song.objects.count() > settings.SUSPENDED_VAL):
            diff = suspended_song.objects.count() - settings.SUSPENDED_VAL
            for x in range(0, diff):
                top = suspended_song.objects.earliest(field_name="s_order")
                votable_song(file_name=top.file_name, song_title=top.song_title, song_artist=top.song_artist, song_album=top.song_album).save()
                top.delete()


class vote_option(models.Model):
    song = models.ForeignKey(votable_song)
    v_count = models.IntegerField(default=0)

class vote(models.Model):
    vote_options = models.ManyToManyField(vote_option)
