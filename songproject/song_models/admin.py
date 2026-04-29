from django.contrib import admin
from .models import Song, SongUser

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'artist', 'language', 'category', 'number_times_played')
    list_filter = ('language', 'category')
    search_fields = ('title', 'artist')
    readonly_fields = ('created_at',)

@admin.register(SongUser)
class SongUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'song', 'played_at', 'correct_guesses', 'wrong_guesses')
    list_filter = ('played_at',)
    search_fields = ('user__username', 'song__title')
    readonly_fields = ('played_at',)