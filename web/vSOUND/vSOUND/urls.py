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
    url(r'^ctl/(?P<cmd>\D{4})-(?P<token>\d{8})/$', views.cmd_handler),
    url(r'^vol=(?P<vol>\d{3})$', views.vol_handler),

    #Login and Control Page
    url(r'^login/', auth_views.login, {'template_name': 'trctl/admin_login.html', 'redirect_field_name': '/control/'}),
    url(r'^logout/', auth_views.logout, {'template_name': 'trctl/admin_logout.html', 'redirect_field_name': '/login/'}),
    url(r'^control/', views.admin_site),
]
