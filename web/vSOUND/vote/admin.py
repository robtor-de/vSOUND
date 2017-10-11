from django.contrib import admin
from vote.models import votable_song, suspended_song, vote_option

class votable_admin(admin.ModelAdmin):
    list_display = ('song_title', 'song_artist')

class suspended_admin(admin.ModelAdmin):
    list_display = ('song_title', 'song_artist')

# Register your models here.
admin.site.register(votable_song, votable_admin)
admin.site.register(suspended_song, suspended_admin)
admin.site.register(vote_option)
