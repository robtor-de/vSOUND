from django.shortcuts import render, redirect
from django.http import HttpResponse
from mpd import MPDClient
from django.conf import settings
from vote.models import vote_option as o

# Create your views here.


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


def vote_view(request):
    global cli
    connect_mpd()

    playlist = cli.playlistinfo()
    status = cli.status()

    try:
        current_song = playlist[int(status['song'])]["title"]
        current_artist = playlist[int(status['song'])]["artist"]
    except:
        current_song = ""
        current_artist = ""


    if(o.is_active()):
        options = o.objects.all()

        #calculate percentage values
        per_vals = []
        vote_sum = 0

        for x in options.values("v_count"):
            vote_sum = vote_sum + x["v_count"]



        return render(request, "vote/vote.html", {"active": True, "playlist": playlist, "status": status, "options": options, "song": current_song, "artist": current_artist, "vote_sum": vote_sum})
    else:
        return render(request, "vote/vote_inactive.html")

def vote_for(request, pk_vote):
    o.vote_for(pk_vote)
    return redirect("/vote/")
