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
from trctl import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    #Direct control urls that accept commands
    url(r'^ctl/(?P<cmd>\D{4})/$', views.cmd_handler),
    url(r'^vol=(?P<vol>\D{1})$', views.vol_handler),
    url(r'^id=(?P<action>\D{1})(?P<songid>\d{1,10})', views.id_handler),
    url(r'^add/$', views.add),
    url(r'^load=(?P<playlist_name>.+)=$', views.load_playlist),
    url(r'^save_playlist=(?P<playlist_name>.+)=$', views.save_playlist),

    #Login and admin page
    url(r'^login/', views.login_screen),
    url(r'^authenticate/', views.auth_handler),
    url(r'^logout/', auth_views.logout, {'next_page': '/login/'}),
    url(r'^control/search/', views.search, {'s_req': ''}),
    url(r'^control/', views.admin_site),
    url(r'^playlist/', views.playlist)
]
