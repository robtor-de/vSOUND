from django.db import models

# Create your models here.

class vote_option(models.Model):
    song = models.ForeignKey("votable_song")
    v_count = models.IntegerField(default=0)


class votable_song(models.Model):
    file_name = models.TextField()
    song_title = models.TextField()
    song_artist = models.TextField()
    song_album = models.TextField()
