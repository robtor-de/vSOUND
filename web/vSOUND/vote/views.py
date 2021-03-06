from django.shortcuts import render, redirect
from django.http import HttpResponse
from mpd import MPDClient
from django.conf import settings
from vote.models import vote_option as o
from random import randint

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
        act_val = True
        add_val = True

        #calculate percentage values
        per_vals = []

        #calculates the sum of vote_voices
        vote_sum = 0
        for x in options.values("v_count"):
            vote_sum = vote_sum + x["v_count"]

        #calculates a percentage value for each individual progress bar in html template
        for x in options.values("v_count"):
            if(vote_sum > 0):
                percentage = (x["v_count"]/vote_sum)*100
                per_vals.append(int(percentage))
            else:
                per_vals.append(0)


        r_col = []
        avail_col = ["bg-primary", "bg-secondary", "bg-success", "bg-danger", "bg-warning", "bg-info"]
        #generates random colors for displaying the progress
        for obj in options:
            r_col.append(avail_col[randint(0, 5)])

        data = zip(options, per_vals, r_col)

        if(request.session.get("voices", default=0) >= settings.VOICES_PER_SESSION):
            act_val = False
        else:
            act_val = True

        if(o.objects.count() < settings.VOTE_OPTS + settings.USER_ADDABLE):
            add_val = True
        else:
            add_val = False

        return render(request, "vote/vote.html", {"active": act_val, "addable": add_val, "status": status, "song": current_song, "artist": current_artist, "data": data})
    else:
        return render(request, "vote/vote_inactive.html", {"status": status, "song": current_song, "artist": current_artist})


def app_vote_req(request):
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
        act_cal = True

        #calculate percentage values
        per_vals = []

        #calculates the sum of vote_voices
        vote_sum = 0

        for x in options.values("v_count"):
            vote_sum = vote_sum + x["v_count"]

        #calculates a percentage value for each individual progress bar in html template
        for x in options.values("v_count"):
            if(vote_sum > 0):
                percentage = (x["v_count"]/vote_sum)*100
                per_vals.append(int(percentage))
            else:
                per_vals.append(0)


        if(request.session.get("voices", default=0) >= settings.VOICES_PER_SESSION):
            act_val = False
        else:
            act_val = True

        data = zip(options, per_vals)


        return render(request, "vote/app.xml", {"active": act_val, "status": status, "song": current_song, "artist": current_artist, "data": data})
    else:
        return HttpResponse("inactive_ok")

def vote_for(request, pk_vote):
    try:
        o.vote_for(pk_vote)
        request.session["voices"] = request.session.get("voices", default=0) + 1
        return redirect("/vote/")
    except:
        return redirect("/vote/")

def update(request):
    global cli
    connect_mpd()

    try:
        if(o.is_active()):
            playlist = cli.playlistinfo()
            plst_id_active = cli.status()["songid"]


            #TODO: fix this - here!
            plst_id_request = playlist[- settings.RELOAD_SHIFT]['id']

            if(plst_id_active >= plst_id_request):
                result = o.finish_vote()
                cli.add(result["file"])
                return HttpResponse("finished_vote")
            else:
                return HttpResponse("no_vote_needed")
        else:
            return HttpResponse("not_active")
    except:
        return HttpResponse("mpd_error")


#Added custom song search option

def search(request):
    global cli
    connect_mpd()
    if(o.is_active()):
        if(request.method == 'POST'):
            result = cli.search("any", request.POST["search_text"])
            return render(request, 'vote/search.html', {'result': result, 's_text': request.POST['search_text']})
        else:
            return render(request, 'vote/search.html')
    else:
        return render(request, 'error.html', {'error_text': 'Keine Abstimmung aktiv!'})

def add(request):
    if(o.is_active()):
        try:
            if(o.objects.count() < settings.VOTE_OPTS + settings.USER_ADDABLE):
                o.objects.create(file_name=request.POST["file"], song_title=request.POST["song_title"], song_artist=request.POST["song_artist"], v_count=0)
            else:
                return render(request, 'error.html', {'error_text': 'Die bist leider zu spät, es wurden schon zu viele Lieder hinzugefügt'})
        except:
            return render(request, 'error.html', {'error_text': 'Fehler beim Hinzufügen des Liedes'})
        return redirect("/vote/")
    else:
        return render(request, 'error.html', {'error_text': 'Keine Abstimmung aktiv!'})
