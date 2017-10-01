from django.shortcuts import render
from mpd import MPDClient
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseForbidden
from trctl.forms import searchForm

#Command handlers for the Admin Control Page

def cmd_handler(request, cmd):
    if (request.user.is_authenticated):
        cli = MPDClient()
        try:
            MPDClient.connect(cli, settings.MPD_ADDRESS, settings.MPD_PORT)
        except:
            return render(request, 'error.html', {'error_text': 'Konnte leider keine Verbindung zum MPD herstellen'})

        if (cmd == 'play'):
            cli.play()
        elif (cmd == 'paus'):
            cli.pause()
        elif (cmd == 'next'):
            cli.next()
        elif (cmd == 'prev'):
            cli.previous()
        elif (cmd == 'stop'):
            cli.stop()
        elif (cmd == 'clrp'):
            cli.clear()
        elif (cmd == 'updt'):
            cli.update()
        elif (cmd == 'rscn'):
            cli.rescan()
        else:
            return render(request, 'error.html', {'error_text': 'Unbekannter MPD-Befehl'})
    else:
        return redirect("/login/")

    cli.close()
    return redirect("/control/")


def vol_handler(request, vol):
    volume = int(vol)
    if(request.user.is_authenticated):
        if(volume >= 0 and volume <= 100):
            cli = MPDClient()
            try:
                MPDClient.connect(cli, settings.MPD_ADDRESS, settings.MPD_PORT)
            except:
                return render(request, 'error.html', {'error_text': 'Konnte leider keine Verbindung zum MPD herstellen'})
            try:
                cli.setvol(volume)
            except:
                return render(request, 'error.html', {'error_text': 'Fehler beim Sezten der Lautstärke, vielleicht wird aktuell nichts wiedergegeben'})
            cli.close()
        else:
            return render(request, 'error.html', {'error_text': 'Lautstärke nicht im gültigen Bereich'})
    else:
        return redirect("/login/")
    return redirect("/control/")


def id_handler(request, songid):
    if(request.user.is_authenticated):
        cli = MPDClient()
        try:
            MPDClient.connect(cli, settings.MPD_ADDRESS, settings.MPD_PORT)
        except:
            return render(request, 'error.html', {'error_text': 'Konnte leider keine Verbindung zum MPD herstellen'})

        cli.playid(songid)
        cli.close()
        return redirect("/control/")
    else:
        return redirect("/login/")


#View for the Admin Control Site
def admin_site(request):
    if (request.user.is_authenticated):
        cli = MPDClient()
        try:
            MPDClient.connect(cli, settings.MPD_ADDRESS, settings.MPD_PORT)
        except:
            return render(request, 'error.html', {'error_text': 'Konnte leider keine Verbindung zum MPD herstellen'})

        playlist = cli.playlistinfo()
        status = cli.status()
        stats = cli.stats()

        try:
            current_song = playlist[int(status['song'])]["title"]
        except:
            current_song = "--"


        return render(request, 'trctl/admin.html', {"playlist": playlist, "status": status, "stats": stats, "song": current_song})
    else:
        return redirect("/login/")


#Search and add to Playlist function

def search(request):
    if (request.user.is_authenticated):
        if(request.method == 'POST'):
            form = searchForm(request.POST)

            if(form.is_valid()):
                cli = MPDClient()
                try:
                    MPDClient.connect(cli, settings.MPD_ADDRESS, settings.MPD_PORT)
                except:
                    return render(request, 'error.html', {'error_text': 'Konnte leider keine Verbindung zum MPD herstellen'})

                result = cli.search("any", form.cleaned_data["search_text"])
                return HttpResponse(result)
        else:
            form = searchForm()

        return render(request, 'trctl/search.html', {'form': form})

def uri_handler(request, songfile):
    if(request.user.is_authenticated):
        cli = MPDClient()
        try:
            MPDClient.connect(cli, settings.MPD_ADDRESS, settings.MPD_PORT)
        except:
            return render(request, 'error.html', {'error_text': 'Konnte leider keine Verbindung zum MPD herstellen'})
        cli.add(songfile)
        cli.close()
        return HttpResponse(songfile)
    else:
        return redirect("/login/")
