from django.db import models
from django.conf import settings
from django.utils import timezone
from mpd import MPDClient
from random import randint

cli = MPDClient()

def connect_mpd():
    global cli

    try:
        cli.status()
    except:
        try:
            MPDClient.connect(cli, settings.MPD_ADDRESS, settings.MPD_PORT)
        except:
            #TODO: Add here better support
            print("MPD-Error")

class votable_song(models.Model):
    file_name = models.TextField()
    song_title = models.TextField(default="missing-title")
    song_artist = models.TextField(default="missing-artist")


    def auto_add():
        global cli
        connect_mpd()

        plst = cli.playlistinfo()

        for entry in plst:
            try:
                votable_song(file_name=entry['file'], song_title=entry['title'], song_artist=entry['artist']).save()
            except:
                print("Error adding this song")

    def suspend_song(v_song):
        suspended_song(file_name=v_song.file_name, song_title=v_song.song_title, song_artist=v_song.song_artist, s_order=timezone.now()).save()
        v_song.delete()

class suspended_song(models.Model):
    file_name = models.TextField()
    song_title = models.TextField()
    song_artist = models.TextField()
    s_order = models.DateTimeField()

    def check_for_unsuspend():
        if(suspended_song.objects.count() > settings.SUSPENDED_VAL):
            diff = suspended_song.objects.count() - settings.SUSPENDED_VAL
            for x in range(0, diff):
                top = suspended_song.objects.earliest(field_name="s_order")
                votable_song(file_name=top.file_name, song_title=top.song_title, song_artist=top.song_artist).save()
                top.delete()


class vote_option(models.Model):
    v_count = models.IntegerField(default=0)
    file_name = models.TextField()
    song_title = models.TextField()
    song_artist = models.TextField()

    def vote_setup():
        votable_song.objects.all().delete()
        suspended_song.objects.all().delete()
        votable_song.auto_add()

    def initiate_vote():
        vote_option.objects.all().delete()

        for x in range(0, settings.VOTE_OPTS):
            if(votable_song.objects.count() > 1):
                r_num = randint(0, votable_song.objects.count() - 1)
                v_rand = votable_song.objects.all()
                r_song = v_rand[r_num]
                vote_option.objects.create(file_name=r_song.file_name, song_title=r_song.song_title, song_artist=r_song.song_artist, v_count=0)
                votable_song.suspend_song(r_song)
                suspended_song.check_for_unsuspend()
            else:
                print("Not enough votable songs available, just unsuspending")
                suspended_song.check_for_unsuspend()

    def vote_for(primary_key):
        target = vote_option.objects.get(pk=primary_key)
        n_val = target.v_count + 1
        vote_option.objects.filter(pk=primary_key).update(v_count=n_val)

    def finish_vote():
        o_votes = vote_option.objects.order_by('v_count')
        o_winner = o_votes.last()
        transfer_data = {'file': o_winner.file_name, 'title': o_winner.song_title, 'artist': o_winner.song_artist}

        suspended_song.check_for_unsuspend()
        return transfer_data
