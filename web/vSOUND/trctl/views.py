from django.shortcuts import render
from mpd import MPDClient
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseForbidden


def cmd_handler(request, cmd):
    cli = MPDClient()

    #Establish Connection to MPDServer or throw Error
    try:
        MPDClient.connect(cli, settings.MPD_ADDRESS, settings.MPD_PORT)
    except:
        return render(request, 'error.html', {'error_text': 'Konnte leider keine Verbindung zum MPD herstellen'})

    if (request.user.is_authenticated):
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
            cli.setvol(volume)
            cli.close()
        else:
            return render(request, 'error.html', {'error_text': 'Lautstärke nicht im gültigen Bereich'})
    else:
        return redirect("/login/")
    return redirect("/control/")


def admin_site(request):
    if request.user.is_authenticated():
        return render(request, 'trctl/admin.html')
    else:
        return redirect("/login/")

def playlist(request):
    cli = MPDClient()
    try:
        MPDClient.connect(cli, settings.MPD_ADDRESS, settings.MPD_PORT)
    except:
        return render(request, 'error.html', {'error_text': 'Konnte leider keine Verbindung zum MPD herstellen'})

    if(request.user.is_authenticated):
        info = cli.playlistinfo()
        return render(request, "trctl/playlist.html", {"playlist": info})

    return HttpResponse(info)
