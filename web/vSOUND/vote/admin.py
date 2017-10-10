from django.contrib import admin
from vote.models import votable_song, suspended_song, vote_option, vote

# Register your models here.
admin.site.register(votable_song)
admin.site.register(suspended_song)
admin.site.register(vote_option)
admin.site.register(vote)
