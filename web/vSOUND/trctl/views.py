from django.shortcuts import render
from mpd import MPDClient
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login

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


#Show the login page eventually with additional infos
def login_screen(request):
    if (request.user.is_authenticated):
        #if user is logged in redirect to admin site
        return redirect("/control/")
    else:
        #return the login screen if the user isn't logged in
        return render(request, 'trctl/admin_login.html')
    return render(request, 'trctl/admin_login.html')

#hander for the login form, log the user in
def auth_handler(request):
    #read the username and password from the request
    username = request.POST['username']
    password = request.POST['password']
    #authenticate the user
    user = authenticate(username=username, password=password)

    #login the user if the password is correct or redirect to the error pages
    if user is not None:
        if user.is_active:
            login(request, user)
            #start first mpd connection after login
            connect_mpd()
            return redirect("/control/")
        else:
            return render(request, 'trctl/admin_login.html', {'error_text': 'Benutzerkonto gesperrt!'})
    else:
        return render(request, 'trctl/admin_login.html', {'error_text': 'Benutzername oder Passwort falsch'})


#Command handlers for the Admin Control Page, execute mpd_Client commands and then redirect to the admin page
def cmd_handler(request, cmd):
    global cli
    connect_mpd()
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
    return redirect("/control/")

#command handler for the volume, connect the mpd_cli and change the volume
def vol_handler(request, vol):
    global cli
    connect_mpd()
    if(request.user.is_authenticated):
        if(vol == 'u' or vol == 'd' or vol == 'm'):
            status = cli.status()
            old_vol = int(status['volume'])
            try:
                if(vol == 'u'):
                    cli.setvol(old_vol + settings.VOL_STEP)
                elif(vol == 'd'):
                    cli.setvol(old_vol - settings.VOL_STEP)
                elif(vol == 'm'):
                    cli.setvol(0)
                else:
                    return render(request, 'error.html', {'error_text': 'Unbekannter Befehl'})
            except:
                return render(request, 'error.html', {'error_text': 'Fehler beim Sezten der Lautstärke, vielleicht wird aktuell nichts wiedergegeben'})
        else:
            return render(request, 'error.html', {'error_text': 'Lautstärke nicht im gültigen Bereich'})
    else:
        return redirect("/login/")
    return redirect("/control/")

#command handler for the direct id player, is called when the admin clicks an entry on the playlist
def id_handler(request, action, songid):
    global cli
    connect_mpd()
    if(request.user.is_authenticated):
        if(action == 'p'):
            cli.playid(songid)
        elif(action =='d'):
            cli.deleteid(songid)
        else:
            return render(request, 'error.html', {'error_text': 'Unbekannter befehl'})
        return redirect("/control/")
    else:
        return redirect("/login/")


#returns the admin control site with several status information
def admin_site(request):
    global cli
    connect_mpd()
    if (request.user.is_authenticated):
        playlist = cli.playlistinfo()
        status = cli.status()
        stats = cli.stats()
        playlists = cli.listplaylists()
        try:
            current_song = playlist[int(status['song'])]["title"]
            current_artist = playlist[int(status['song'])]["artist"]
        except:
            current_song = ""
            current_artist = ""
        return render(request, 'trctl/admin.html', {"playlist": playlist, "status": status, "stats": stats, "song": current_song, "artist": current_artist, "playlists": playlists})
    else:
        return redirect("/login/")


#returns the search request form with a list of search results
def search(request, s_req):
    global cli
    connect_mpd()
    if (request.user.is_authenticated):
        if(request.method == 'POST'):
            #return results if the form is valid
            #sets the search text to the s_req value --> search result should stay after adding title
            if(s_req != ''):
                result = cli.search("any", request.POST["search_text"])
            else:
                result = cli.search("any", request.POST["search_text"])
            return render(request, 'trctl/search.html', {'result': result, 's_text': request.POST['search_text']})
        else:
            return render(request, 'trctl/search.html')

#adds a requested song to the playlist
def add(request):
    global cli
    connect_mpd()
    if(request.user.is_authenticated):
        try:
            cli.add(request.POST["add_song"])
            s_text = request.POST["search_text"]
        except:
            return render(request, 'error.html', {'error_text': 'Fehler beim Hinzufügen des Liedes'})
        return search(request, s_text)
    else:
        return redirect("/login/")

#loads a selected playlist --> Used method over url here because no backtrack of search text like in add() is necessary
def load_playlist(request, playlist_name):
    global cli
    connect_mpd()
    if(request.user.is_authenticated):
        try:
            cli.load(playlist_name)
        except:
            return render(request, 'error.html', {'error_text': 'Fehler beim Laden der Playlist'})
        return redirect("/control/")
    else:
        return redirect("/login/")

#tries to save a playlist
def save_playlist(request, playlist_name):
    global cli
    connect_mpd()
    if(request.user.is_authenticated):
        try:
            cli.save(playlist_name)
        except:
            return render(request, 'error.html', {'error_text': 'Fehler beim Speichern der Playlist'})
        return redirect("/control/")
    else:
        return redirect("/login/")

def playlist(request):
    cli2 = MPDClient()
    try:
        MPDClient.connect(cli2, settings.MPD_ADDRESS, settings.MPD_PORT)
    except:
        return render(request, 'error.html', {'error_text': 'Konnte leider keine Verbindung zum MPD herstellen'})

    playlist = cli2.playlistinfo()
    cli2.close()
    return render(request, 'trctl/playlist.html', {'playlist': playlist})
