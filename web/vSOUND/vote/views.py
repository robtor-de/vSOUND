from django.shortcuts import render, redirect
from django.http import HttpResponse

from vote.models import vote_option as o

# Create your views here.

def vote_view(request):

    return HttpResponse(o.is_active())
