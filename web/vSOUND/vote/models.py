from django.db import models
from django.conf import settings
from django.utils import timezone
from mpd import MPDClient
from random import randint
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

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

        if(len(plst) <= settings.SUSPENDED_VAL):
            raise ValueError("Number of Playlist items is smaller than Suspended Val in settings")

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


    #Sets up the database for a voting session made from the current playlist
    def vote_setup():
        votable_song.objects.all().delete()
        suspended_song.objects.all().delete()
        votable_song.auto_add()
        vote_option.initiate_vote()

    def vote_destroy():
        vote_option.objects.all().delete()

    def initiate_vote():
        vote_option.objects.all().delete()

        #Clear all session vote values, that each user can leave votes
        session_data = Session.objects.all()
        session_keys = []

        for session in session_data:
            session_keys.append(session.session_key)

        for key in session_keys:
            s = SessionStore(session_key=key)
            s["voices"] = 0
            s.save()


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

        #check if other same_level votes are availabla and make random choice
        s_val_opts = o_votes.filter(v_count__exact=o_winner.v_count)
        if(s_val_opts.count() > 1):
            r_num = randint(0, s_val_opts.count() - 1)
            o_winner = s_val_opts[r_num]

        transfer_data = {'file': o_winner.file_name, 'title': o_winner.song_title, 'artist': o_winner.song_artist}

        suspended_song.check_for_unsuspend()
        vote_option.initiate_vote()
        return transfer_data

    def is_active():
        if(vote_option.objects.count() > 0):
            return True
        else:
            return False
