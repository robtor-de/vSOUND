from django.shortcuts import render
from mpd import MPDClient
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseForbidden


def cmd_handler(request, cmd, token):
    cli = MPDClient()

    #Establish Connection to MPDServer or throw Error
    try:
        MPDClient.connect(cli, settings.MPD_ADDRESS, settings.MPD_PORT)
    except:
        return redirect("/static/mpd_conn_error.html")

    #Check if the Admin token exists --> TODO: Change token verification over http request and not via url
    if (token == settings.ADM_TOKEN):
        if (cmd == 'play'):
            cli.play()
        elif (cmd == 'paus'):
            cli.pause()
        elif (cmd == 'next'):
            cli.next()
        else:
            cli.pause()
    else:
        return HttpResponseForbidden("Wrong Admin Token, maybe Token changed or wrong link")

    return HttpResponse("OK")


def vol_handler(request, vol):
    volume = int(vol)

    if(volume >= 0 and volume <= 100):
        cli = MPDClient()

        #Establish Connection to MPDServer or throw Error
        try:
            MPDClient.connect(cli, settings.MPD_ADDRESS, settings.MPD_PORT)
        except:
            return redirect("/static/mpd_conn_error.html")

        cli.setvol(volume)
        cli.close()
    else:
        return HttpResponse("Volume not in Range")
    return HttpResponse(volume)
