from django.shortcuts import render, redirect
from django.http import HttpResponse

from vote.models import vote_option as o

# Create your views here.

def vote_view(request):
    if(o.is_active()):
        options = o.objects.all()
        return render(request, "vote/vote.html", {"options": options})
    else:
        return render(request, "vote/vote_inactive.html")
