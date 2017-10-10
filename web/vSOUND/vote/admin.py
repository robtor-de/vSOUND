from django.contrib import admin
from vote.models import votable_song, suspended_song, vote_option, vote

class votable_admin(admin.ModelAdmin):
    list_display = ('r_num', 'song_title', 'song_artist', 'song_album')

class suspended_admin(admin.ModelAdmin):
    list_display = ('song_title', 'song_artist', 'song_album')

# Register your models here.
admin.site.register(votable_song, votable_admin)
admin.site.register(suspended_song, suspended_admin)
admin.site.register(vote_option)
admin.site.register(vote)
