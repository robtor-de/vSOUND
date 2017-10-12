"""vSOUND URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from trctl import views as trctl_views
from vote import views as vote_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    #Direct control urls that accept commands
    url(r'^ctl/(?P<cmd>\D{4})/$', trctl_views.cmd_handler),
    url(r'^vol=(?P<vol>\D{1})$', trctl_views.vol_handler),
    url(r'^id=(?P<action>\D{1})(?P<songid>\d+)', trctl_views.id_handler),
    url(r'^add/$', trctl_views.add),
    url(r'^load=(?P<playlist_name>.+)=$', trctl_views.load_playlist),
    url(r'^save_playlist=(?P<playlist_name>.+)=$', trctl_views.save_playlist),
    url(r'^delete_playlist=(?P<playlist_name>.+)=$', trctl_views.delete_playlist),

    #Login and admin page
    url(r'^login/', trctl_views.login_screen),
    url(r'^authenticate/', trctl_views.auth_handler),
    url(r'^logout/', auth_views.logout, {'next_page': '/login/'}),
    url(r'^control/search/', trctl_views.search, {'s_req': ''}),
    url(r'^togglevote/', trctl_views.vote_toggle),
    url(r'^control/', trctl_views.admin_site),
    url(r'^playlist/', trctl_views.playlist),

    #vote functions, public for all unauthenticated users
    url(r'^vote/search/', vote_views.search),
    url(r'^vote/', vote_views.vote_view),
    url(r'^voteadd/', vote_views.add),
    url(r'^votefor/pk=(?P<pk_vote>\d+)/$', vote_views.vote_for),
    url(r'^update/', vote_views.update)
]
